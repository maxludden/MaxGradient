"""Defines the Gradient class which is used to print text with a gradient. \
    It inherits from the Rich Text class."""
# pylint: disable=W0611,C0103, E0401
import re
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from typing import List, Optional, Tuple

import numpy as np
from cheap_repr import normal_repr, register_repr
from loguru import logger
from lorem_text import lorem
from rich.console import JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.pretty import Pretty
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from snoop import snoop

from maxgradient._gradient_substring import GradientSubstring
from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.log import Console, Log

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False

console = Console()
log = Log(console=console)


register_repr(Pretty)(normal_repr)
register_repr(Text)(normal_repr)
register_repr(GradientSubstring)(normal_repr)
register_repr(Table)(normal_repr)


class Gradient(Text):
    """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to `""`.\n
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
            color_sample(`bool`): Replace text with characters with `"█" `. Defaults to False.\n
            style(`StyleType`) The style of the gradient text. Defaults to None.\n
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center", "full", \
                "right". Defaults to None.\n
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.\n

    """

    __slots__ = ["_colors", "_hues", "_style", "_color_sample"]

    @snoop(watch=("gradient_spans", "substrings"))
    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = Style.null(),
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Generate a gradient text object."""
        if isinstance(text, Text):
            self._spans: List[Span] = text.spans
            text = strip_control_codes(text.plain)
        else:
            self._spans = spans
        assert isinstance(text, str), f"Text must be a string or Text, not {type(text)}"
        self._text: str = text
        self._length: int = len(text)

        super().__init__(
            text=text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size,
            spans=spans,
        )

        self.color_sample: bool = color_sample
        self._colors: List[Color] = []
        self.hues: int = hues or 3

        # not rainbow
        if not rainbow:
            # colors
            if colors is not None:
                for color in colors:
                    try:
                        Color(color)
                        self.colors.append(color)
                    except ColorParseError as cpe:
                        log.error(cpe)
                    except ValueError as ve:
                        log.error(ve)

                if len(self.colors) < 2:
                    raise ValueError("Gradient must have at least two colors.")
                self.hues = len(self._colors)

                if invert:
                    self.colors = self.colors[::-1]

            # no colors
            elif color is None:
                color_list: List[Color] = ColorList(self.hues, invert).color_list
                self.colors: List[Color] = color_list[: self.hues]

        # rainbow
        else:
            self.hues = 10
            color_list: List = ColorList(self.hues, invert).color_list
            self.colors: List[Color] = color_list[: self.hues]

    def gradient_spans(self) -> List[Span]:
        """Generate gradient spans.

        Returns:
            List[Span]: The gradient spans.
        """
        indexes: List[List[int]] = np.array_split(
            np.arange(self._length), self.hues - 1
        ).tolist()
        spans: List[Span] = []
        for index in indexes:
            substring_length = len(index)
            color1: Tuple[int, int, int] = self.colors[index].rgb_tuple
            r1, g1, b1 = color1
            color2: Tuple[int, int, int] = self.colors[index + 1].rgb_tuple
            r2, g2, b2 = color2
            dr = r2 - r1
            dg = g2 - g1
            db = b2 - b1

            for char_index in range(substring_length):
                blend: float = char_index / substring_length
                span_start: int = index[char_index]
                span_end: int = index[char_index] + 1
                red = f"{int(r1 + dr * blend):02X}"
                green = f"{int(g1 + dg * blend):02X}"
                blue = f"{int(b1 + db * blend):02X}"
                span_color = f"#{red}{green}{blue}"
                color_style = Style(color=span_color)
                span_style = self.style + color_style
                span = Span(span_start, span_end, span_style)
                spans.append(span)
        return spans

    @property
    def text(self) -> str:
        """The text of the gradient."""
        log.debug(f"Getting gradient._text: {self._text}")
        return self._text

    @text.setter
    def text(self, text: Optional[str | Text]) -> None:
        """Set the text of the gradient."""
        log.debug(f"Setting gradient._text: {text}")
        if isinstance(text, Text):
            sanitized_text = strip_control_codes(text.plain)
            self._length = len(sanitized_text)
            self._text = [sanitized_text]
            self._spans: List[Span] = text.spans
        if isinstance(text, str):
            if text == "":
                raise ValueError("Text cannot be empty.")
            sanitized_text = strip_control_codes(text)
            self._length = len(sanitized_text)
            self._text = sanitized_text

    @property
    def colors(self) -> List[Color]:
        """The colors of the gradient."""
        log.debug(
            f"Retrieving gradient._colors: {[color.value for color in self._colors]}"
        )
        return self._colors

    @colors.setter
    def colors(self, colors: List[Color | Tuple | str]) -> None:
        """Set the colors of the gradient."""
        log.debug(f"Setting gradient._colors: {colors}")
        assert isinstance(colors, list), f"Colors must be a list, not {type(colors)}"
        for color in colors:
            assert isinstance(
                color, Color
            ), f"Colors must be a list of Color, not {type(color)}"
        self._colors = colors

    @property
    def hues(self) -> int:
        """The number of colors in the gradient."""
        log.debug(f"Retrieving gradient._hues: {self._hues}")
        return self._hues

    @hues.setter
    def hues(self, hues: int) -> None:
        """Set the number of colors in the gradient."""
        log.debug(f"Setting gradient._hues: {hues}")
        if hues < 2:
            raise ValueError("Gradient must have at least two colors.")
        self._hues = hues

    @property
    def color_sample(self) -> bool:
        """Whether the gradient is a color sample."""
        log.debug(f"Retrieving gradient._color_sample: {self._color_sample}")
        return self._color_sample

    @color_sample.setter
    def color_sample(self, color_sample: bool) -> None:
        """Set whether the gradient is a color sample."""
        log.debug(f"Setting gradient._color_sample: {color_sample}")
        if color_sample:
            self.text = "█" * self._length
        self._color_sample = color_sample

    @property
    def style(self) -> Style:
        """The style of the gradient."""
        log.debug(f"Retrieving gradient._style: {self._style}")
        return self._style

    @style.setter
    def style(self, style: StyleType) -> None:
        """Set the style of the gradient."""
        log.debug(f"Setting gradient._style: {style}")
        if isinstance(style, Style):
            self._style = Style.copy(style).without_color
        if style is None:
            self._style = Style.null()
        elif isinstance(style, str):
            if style == "" or style == "null":
                self._style = Style.null()
            if style == "none" or style == "None":
                self._style = Style.null()
            self._style = Style.parse(style)

    def generate_style(self, color: str) -> Style:
        """Generate a style for a color."""
        new_style = self.style + Style(color=color)
        log.debug(f"Generating style for `{color}`: {new_style}")
        return new_style


if __name__ == "__main__":
    TEXT = lorem.paragraphs(2)
    gradient = Gradient(TEXT,rainbow=True)
    console.print(gradient, justify='center')
