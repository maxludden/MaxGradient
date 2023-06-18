"""Defines the Gradient class which is used to print text with a gradient. \
    It inherits from the Rich Text class."""
# pylint: disable=W0611,C0103, E0401, C0301
import re
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from functools import lru_cache
from multiprocessing import cpu_count
from typing import List, Optional, Tuple

import numpy as np
from cheap_repr import normal_repr, register_repr
from loguru import logger
from lorem_text import lorem
from numpy import ndarray
from rich import inspect
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
from maxgradient.log import Log, LogConsole

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False
console = LogConsole()
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

    __slots__ = ["colors", "_color_sample", "_hues", "_style"]

    # @snoop(watch=("gradient_spans", "substrings"))
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
        self.colors: List[Color] = []
        self.hues: int = hues or 3
        self.colors: List[Color] = self.get_colors(colors, rainbow, invert, verbose)

        gradient_substring: Text = self.generate_substrings(verbose)
        console.line(2)
        self._spans = gradient_substring.spans

    # @snoop(watch_explode=["colors", "self.colors"])
    def get_colors(
        self,
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        verbose: bool = VERBOSE,
    ) -> List[Color]:
        """Get the colors for the gradient.

        Args:
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            verbose(`bool`): Whether to print verbose output. Defaults to True.\n

        Returns:
            List[Color]: A list of colors for the gradient.
        """
        if colors is not None:
            colors_: List[Color] = []
            for index, color in enumerate(colors):
                try:
                    color = Color(color)
                    log.debug(f"Color {index}: {color}")
                    if verbose:
                        console.print(color)
                    colors_.append(color)
                except ColorParseError as error:
                    raise ColorParseError(f"Can't parse color: {color}") from error
            if self.validate_colors(colors_):
                return colors_
        else:
            color_list = ColorList(self.hues, invert).color_list
            if rainbow:
                colors_ = color_list
                if self.validate_colors(colors_):
                    return colors_
            else:
                colors_ = color_list[: self.hues]
                if self.validate_colors(colors_):
                    return colors_

    def get_text(self) -> str:
        """Get the gradient text.

        Returns:
            str: The gradient text.
        """
        if isinstance(self._text, str):
            return self._text
        elif isinstance(self._text, List):
            return "".join(self._text)
        else:
            raise TypeError("Text must be a string or a list of strings.")

    def validate_colors(self, colors: Optional[List[Color]]) -> bool:
        """Validate self.colors to ensure that it is a list of colors."""
        valid: bool = True
        for color in colors:
            if not isinstance(color, Color):
                return False
        if valid:
            return True

    def get_indexes(self, verbose: bool = False) -> List[List[int]]:
        """Generate the indexes for the gradient substring.

        Returns:
            List[List[int]]: The indexes for the gradient substring.
        """
        result: ndarray = np.array_split(np.arange(self._length), self.hues - 1)
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        for count, index in enumerate(indexes):
            msg = f"[b white]Index {count}:[/]{', '.join([str(i) for i in index])}\n\n"
            if verbose:
                log.success(msg)
            else:
                log.info(msg)
        return indexes

    def get_substrings(self, indexes: List[List[int]], text: str) -> List[str]:
        """Generate a list of substrings for the gradient.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.
        """
        substrings: List[str] = []
        for index in indexes:
            substring = self.get_substring(index, text)
            substrings.append(substring)
        return substrings

    def get_substring(self, index: List[int], text: str = VERBOSE) -> str:
        """Generate a string to make a GradientSubstring.

        Args:
            index (List[int]): The index of the substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.

        Returns:
            str: The substring.
        """
        substring_list: List[str] = []
        for num in index:
            substring_list.append(text[num])
        substring = "".join(substring_list)
        return substring

    def generate_substrings(self, verbose: bool = VERBOSE) -> List[Span]:
        """Generate gradient spans.

        Returns:
            List[Span]: The gradient spans.
        """
        text = self.get_text()
        gradient_string = Text()
        indexes: List[List[int]] = self.get_indexes()
        substrings: List[str] = self.get_substrings(indexes, text)
        for index, substring in enumerate(substrings):
            if verbose:
                log.success(f"\n\n[b #ffffff]Index[/]: [b #7FD6E8]{index}[/]")
                log.success(f"[b #ffffff]Substring:[/] [b #E3EC84]{substring}[/]")
            gradient_length = len(substring)
            if verbose:
                log.success(
                    f"[b #ffffff]Substring length:[/] [b #7FD6E8]{gradient_length}[/]"
                )
            substring = Text(substring)

            if index < self.hues - 1:
                if verbose:
                    msg1 = f"[bold #7FD6E8]{index}[/]"
                    msg2 = f"< [bold #7FD6E8]{self.hues-1}[/]"
                    msg3 = "[bold #af00ff]True[/]"
                    log.success(f"{msg1} {msg2} {msg3}")
                color1 = self.colors[index]
                if verbose:
                    log.success(
                        f"[b white]Color 1:[/][b {color1.hex}] {color1.name.capitalize()}[/]"
                    )
                r1, g1, b1 = color1.rgb_tuple
                if verbose:
                    log.success(
                        f"[b white]Color 1 RGB:[/][b {color1.hex}] rgb({r1}, {g1}, {b1})[/]"
                    )
                color2 = self.colors[index + 1]
                if verbose:
                    log.success(
                        f"[b white]Color 2:[/][b {color2.hex}] {color2.name.capitalize()}[/]"
                    )
                r2, g2, b2 = color2.rgb_tuple
                if verbose:
                    log.success(
                        f"[b white]Color 2 RGB:[/][b {color2.hex}] rgb({r2}, {g2}, {b2})[/]"
                    )
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for subindex in range(gradient_length):
                blend = subindex / gradient_length
                red = int(r1 + (blend * dr))
                green = int(g1 + (blend * dg))
                blue = int(b1 + (blend * db))
                color = f"#{red:02X}{green:02X}{blue:02X}"
                if verbose:
                    log.success(
                        f"SubIndex: {subindex} | Blend: {blend} | Color: {color}"
                    )
                substring.stylize(color, subindex, subindex + 1)

            gradient_string = Text.assemble(
                gradient_string,
                substring,
                style=self.style,
                justify=self.justify,
                overflow=self.overflow,
                no_wrap=self.no_wrap,
                end=self.end,
                tab_size=self.tab_size,
            )
        return gradient_string

    @snoop
    def get_start_indexes(self, indexes: List[List[int]]) -> List[int]:
        """Get the start indexes for the gradient substring.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.

        Returns:
            List[int]: The start indexes for the gradient substring.
        """
        start_indexes: List[int] = []
        for index in indexes:
            start_index = index[0]
            log.log("INFO", f"Start Index: {start_index}")
            start_indexes.append(start_index)
        return start_indexes

    @snoop
    def get_color_starts(self) -> List[Color]:
        """Generate the start colors for the gradient substring."""
        color_starts: List[Color] = []
        for index, color in enumerate(self.colors):
            if index < self.hues - 1:
                log.log("INFO", f"Color Start {index}: {color}")
                color_starts.append(color)
        return color_starts

    @snoop
    def get_color_ends(self) -> List[Color]:
        """Generate the end colors for the gradient substring."""
        color_ends: List[Color] = []
        for index, color in enumerate(self.colors):
            if index > 0:
                log.log("INFO", f"Color End {index}: {color}")
                color_ends.append(color)
        return color_ends

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


register_repr(Gradient)(normal_repr)

if __name__ == "__main__":
    TEXT = lorem.paragraphs(2)
    gradient = Gradient(TEXT)
    console.print(gradient, justify="center")
