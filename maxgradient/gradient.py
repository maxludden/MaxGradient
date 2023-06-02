"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from itertools import repeat
from multiprocessing import cpu_count
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from numpy import arange, array_split, ndarray
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.panel import Panel
from rich.pretty import Pretty
from rich.repr import RichReprResult
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback
from snoop import pp, snoop

from examples.color import Color, ColorParseError
from maxgradient._gradient_substring import GradientSubstring
from maxgradient._utilities import debug
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False

console = Console(theme=GradientTheme())
install_rich_traceback(console=console)
register_repr(Pretty)(normal_repr)
register_repr(Text)(normal_repr)
register_repr(GradientSubstring)(normal_repr)
register_repr(Table)(normal_repr)


class NotEnoughColors(Exception):
    pass


class Gradient(Text):
    """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to empty string.
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. If `colors` has at least two parsable colors, `colors_start`\
                    and `end_color`'s arguments are ignored and those values are parsed from \
                        `colors`.Defaults to []
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.
            invert(`bool): Reverse the color gradient. Defaults to False.
            hues(`int`): The number of colors in the gradient. Defaults to `3`.
            color_sample(`bool`): Whether to print the gradient on identically colored background. \
                This makes the gradient's text invisible, but it useful for printing gradient \
                samples. Defaults to False.
            style(`StyleType`) The style of the gradient text. Defaults to None.
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center", "full", \
                "right". Defaults to None.
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.
            end (str, optional): Character to end text with. Defaults to "\\\\n".
            no_wrap (bool, optional): Disable text wrapping, or None for default. Defaults to None.
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.
            verbose(`bool`): Whether to print verbose output. Defaults to False.
    """

    __slots__ = ["_text""_colors", "invert", "hues", "style"]

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
        verbose: bool = VERBOSE,
    ) -> None:
        """Initialize the Gradient class."""
        self.parse_text(text)
        self.style = style

        # Initialize Text
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

        self.invert: bool = invert
        self.parse_color_sample(color_sample)
        self.parse_colors(colors, rainbow)
        self.parse_hues(hues)


        

        self._spans = self.calculate_spans()

    @debug()
    def calculate_spans(self) -> List[Span]:
        """Calculate the spans to generate the gradient colored text.

        Raises:
            ValueError: If the number of colors is less than 2.

        Returns:
            List[Span]: The gradient spans.
        """
        assert len(self._colors) > 1, "Gradient must have at least two colors."
        assert (
            self._length > self.hues
        ), "Text must be longer than the number of colors."
        text_length = self._length
        gradient_size = text_length // len(self._colors)
        sub_lists: List[List[int]] = [
            array.tolist()
            for array in array_split(range(text_length), len(self._colors) - 1)
        ]
        console.log(sub_lists)
        spans: List[Span] = []

        gradient_substrings: List[GradientSubstring] = []
        for main_index, list in enumerate(sub_lists):
            start_index: int = list[0]
            end_index: int = list[-1]
            substring: str = self._text[start_index:end_index]
            color_1: Color = self._colors[main_index]
            color_2: Color = self._colors[main_index + 1]
            gradient_substring = GradientSubstring(
                substring, start_index, color_1, color_2, self.style
            )
            # console.log([span for span in gradient_substring.spans])
            # spans.extend(gradient_substring.spans)
            gradient_substrings.append(gradient_substring)
            console.log(gradient_substring)


        return spans

    @property
    def style(self) -> Style:
        """Return the gradient style."""
        return self.style

    @style.setter
    def style(self, style: StyleType) -> None:
        """Set the gradient style.

        Args:
            style (StyleType): The style to apply to the gradient.
        """
        if style is None:
            self.style = Style.null()
        elif isinstance(style, Style):
            self.style = style
        elif isinstance(style, str):
            if style is None or style == "none":
                self.style = Style.null()
            else:
                self.style = Style(style)

    @snoop
    def parse_text(self, text: str|Text) -> None:
        """Parse the gradient text."""
        if text is None:
            raise ValueError("Text cannot be None.")

        if isinstance(text, Text):
            self._text = [text.plain]
            self._length = len(text.plain)
            self._spans = text._spans

        elif isinstance(text, str):
            if text == "":
                raise ValueError("Text cannot be empty.")
            else:
                sanitized_text = strip_control_codes(text)
                self._length = len(sanitized_text)
                self._text = [sanitized_text]

    @debug()
    def parse_style(self, color: Optional[str]) -> Style:
        """Parse the gradient style."""
        if self.style == Style.null() or self.style is None:
            return Style(color)
        elif "none" in str(Style(self.style)):
            return Style(color)
        else:
            style_str = str(Style(self.style))
            if "none" in style_str:
                style_str = style_str.replace("none", "").strip()
                if style_str == "":
                    return Style(color)
                else:
                    return Style.parse(f"{style_str} {color}")
            else:
                return Style.parse(f"{style_str} {color}")

    def parse_color_sample(self, color_sample: bool) -> None:
        """Parse the color sample."""
        if color_sample:
            self._text = "█" * self._length

    def parse_colors(self, colors: Optional[List[Color | Tuple | str]], rainbow: bool) -> None:
        """Parse the gradient colors."""
        self._colors: List[Color] = []
        if not rainbow:
            if colors is None:
                self._colors = ColorList(self.hues, self.invert).color_list
            else:
                for color in colors:
                    try:
                        parsed_color = Color(color)
                        self._colors.append(parsed_color)
                    except:
                        print(f"Unable to parse color: {color}")
            assert len(self._colors) > 1, "Gradient must have at least two colors."
            assert (self._length > self.hues), "Text must be longer than the number of colors."
            self.hues = len(self._colors)

        else:
            assert len(self._colors) < self._length, "Text must be longer than the number of colors."
            self.hues = 10
            self._colors = ColorList(self.hues, self.invert).color_list

    def parse_hues(self, hues: int) -> None:
        """Parse the gradient hues."""
        if hues is None:
            self.hues = len(self._colors)
        else:
            self.hues = hues

if __name__ == "__main__":
    from lorem_text import lorem
    from rich.console import Console
    from rich.traceback import install as install_rich_traceback

    from maxgradient.theme import GradientTheme

    console = Console(theme=GradientTheme())
    install_rich_traceback(console=console)
    random_gradient = Gradient(lorem.paragraph())
    random_gradient_text: str = "Gradient is a Python library for creating \
beautiful color gradients."
    random_gradient: Gradient = Gradient(random_gradient_text)
    console.print(random_gradient, justify="center")
