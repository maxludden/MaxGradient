"""Defines the Gradient class which is used to print text with a gradient. \
    It inherits from the Rich Text class."""
# pylint: disable=W0611,C0103, E0401
import re
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from typing import List, Optional, Tuple
from functools import lru_cache

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
from maxgradient.log import LogConsole, Log

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

        gradient_substrings: List[GradientSubstring] = self.generate_substrings(verbose)
        console.line(2)
        for substring in gradient_substrings:
            console.print(substring)

    @snoop(watch_explode=["colors", "self.colors"])
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
                colors_ = color_list[:self.hues]
                if self.validate_colors(colors_):
                    return colors_

    def validate_colors(self, colors: Optional[List[Color]]) -> bool:
        """Validate self.colors to ensure that it is a list of colors."""
        valid: bool = True
        for color in colors:
            if not isinstance(color, Color):
                return False
        if valid:
            return True


    def get_indexes(self, verbose: bool = VERBOSE) -> List[List[int]]:
        """Generate the indexes for the gradient substring.

        Returns:
            List[List[int]]: The indexes for the gradient substring.
        """
        result: ndarray = np.array_split(np.arange(self._length), self.hues - 1)
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        for count, index in enumerate(indexes):
            msg = f"[b white]Index {count}:[/]{', '.join([str(i) for i in index])}"
            if verbose:
                log.success(msg)
            else:
                log.info(msg)
        return indexes

    def get_substrings(
        self, indexes: List[List[int]], text: str, verbose: bool = VERBOSE
    ) -> List[str]:
        """Generate a list of substrings for the gradient.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.
        """
        substrings: List[str] = []
        for index in indexes:
            substring = self.get_substring(index, text, verbose=verbose)
            substrings.append(substring)
        return substrings

    def get_substring(
        self, index: List[int], text: str, verbose: bool = VERBOSE
    ) -> str:
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
        msg1 = f"[b white]Substring:[/]{substring}"
        msg2 = f"[b white]Substring length:[/]{len(substring)}"
        if verbose:
            log.success(msg1)
            log.success(msg2)
        else:
            log.info(msg1)
            log.info(msg2)
        return substring

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

    def generate_substrings(self, verbose: bool = VERBOSE) -> List[Span]:
        """Generate gradient spans.

        Returns:
            List[Span]: The gradient spans.
        """
        text = self.get_text()
        indexes: List[List[int]] = self.get_indexes(verbose)
        substrings: List[str] = self.get_substrings(indexes, text, verbose)
        start_indexes: List[int] = self.get_start_indexes(indexes, verbose)
        color_starts: List[Color] = self.get_color_starts()
        color_ends: List[Color] = self.get_color_ends()
        style = self.style
        if verbose:
            sub_verbose: bool = True
            self.log_substring_gradient(
                substrings, start_indexes, color_starts, color_ends, style, verbose
            )
        else:
            sub_verbose: bool = False
        gradient_substrings: List[GradientSubstring] = []
        for index in range(self.hues - 1):
            substring = GradientSubstring(
                substrings[index],
                start_indexes[index],
                color_starts[index],
                color_ends[index],
                style,
                verbose=sub_verbose,
            )
            if verbose:
                log.success(
                    f"[b white]GradientSubstring[/] [b #7FD6E8]{index}[/][white]:[/]"
                )
                console.print(substring)
            else:
                log.debug(f"GradientSubstring {index}: {substring}")
            gradient_substrings.append(substring)
        return gradient_substrings

    def get_start_indexes(
        self, indexes: List[List[int]], verbose: bool = VERBOSE
    ) -> List[int]:
        """Generate the index of the start of each substring of the text.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.

        Returns:
            List[int]: _description_
        """
        substring_starts: List[int] = []
        for index in indexes:
            start_index = index[0]
            msg: str = f"[b white]Start index:[/][b #7FD6E8]{start_index}[/]"
            if verbose:
                log.success(msg)
            else:
                log.debug(msg)
            substring_starts.append(start_index)
        return substring_starts

    def get_color_starts(self, verbose: bool = VERBOSE) -> List[Color]:
        """Generate a list of Color instances from which the gradients will start.

        Returns:
            List[Color]: A list of Color instances.
        """
        color_starts: List[Color] = []
        for index in range(self.hues):
            color1 = self.get_color1(index, self.colors)
            msg = f"[b white]Color1 {index}:[/][b {color1.hex}]{color1.name.capitalize()}[/]"
            if verbose:
                log.success(msg)
            else:
                log.debug(msg)
            color_starts.append(color1)
        return color_starts

    @snoop
    def get_color1(self, index: int, colors: List[Color]) -> Color:
        """Get the first color for the gradient substring.

        Args:
            index (int): The index of the substring.
        """
        color1: Color = colors[index]
        log.debug(f"Called get_color1() -> {color1}")
        return color1

    def get_color_ends(self, verbose: bool = VERBOSE) -> List[Color]:
        """Generate a list of Color instances from which the gradients will end.

        Returns:
            List[Color]: A list of Color instances.
        """
        color_ends = self.colors[1:-1]
        msg = f"Called get_color_ends() -> {color_ends}"
        if verbose:
            log.success(msg)
        else:
            log.debug(msg)
        return color_ends

    def get_color2(self, index: int, colors: List[Color]) -> Color:
        """Get the second color for the gradient substring.

        Args:
            index (int): The index of the substring.
        """
        return colors[index + 1]

    def get_start_index(self, index: int, indexes: List[List[int]]) -> int:
        """Get the start index of the gradient substring.

        Args:
            index (int): The index of the substring.
        """
        return indexes[index][0]

    def log_substring_gradient(
        self,
        substring: str,
        start_index: int,
        color1: Color,
        color2: Color,
        style: Style,
        verbose: bool = VERBOSE,
    ) -> None:
        """Log the gradient substring.

        Args:
            substring (str): The substring to log.
            start_index (int): The start_index of the substring.center()
            color1 (Color): The first color of the substring.
            color2 (Color): The second color of the substring.
        """
        msg1 = f"[b white]Substring:[/][i #E3EC84]{substring}[/]"
        msg2 = f"[b white]Start_index:[/][b #7FD6E8]{start_index}[/]"
        msg3 = f"[b white]Color 1:[/][i {color1.hex}]{color1.name.capitalize()}[/]"
        msg4 = f"[b white]Color 2:[/][i {color2.hex}]{color2.name.capitalize()}[/]"
        msg5 = f"[b white]Style:[/][i {style.color}]{str(style)}[/]"
        for msg in [msg1, msg2, msg3, msg4, msg5]:
            if verbose:
                log.success(msg)
            else:
                log.info(msg)

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

    # @property
    # @lru_cache(maxsize=1)
    # def colors(self) -> List[Color]:
    #     """The colors of the gradient."""
    #     log.debug(
    #         f"Retrieving gradient._colors: {[color.value for color in self._colors]}"
    #     )
    #     return self._colors

    # @colors.setter
    # def colors(self, colors: List[Color | Tuple | str]) -> None:
    #     """Set the colors of the gradient."""
    #     log.debug(f"Setting gradient._colors: {colors}")
    #     assert isinstance(colors, list), f"Colors must be a list, not {type(colors)}"
    #     self._colors = colors

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
    gradient = Gradient(TEXT, verbose=True)
    console.print(gradient, justify="center")
