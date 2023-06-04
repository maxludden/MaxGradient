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
from rich.style import Style, StyleType, NULL_STYLE
from rich.table import Table
from rich.text import Span, Text
from rich.highlighter import ReprHighlighter
from rich.traceback import install as install_rich_traceback
from snoop import pp, snoop
from loguru import logger

from maxgradient.log import Log
from maxgradient._gradient_substring import GradientSubstring
from maxgradient.old_color import Color
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False

console = Console(
    theme=GradientTheme(),
    highlighter=ReprHighlighter()
)
install_rich_traceback(console=console)
log = Log(console)
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
            no_wrap (bool, optional): Disable text wrapping, or None for default. Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.\n

    """

    __slots__ = ["_text","_colors", "invert", "hues", "style"]

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
        verbose: bool = VERBOSE) -> None:
        """Generate a gradient text object."""
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


    @property
    def text(self) ->  str:
        """The text of the gradient."""
        log.debug(f"Getting gradient._text: {self._text}")
        return self._text

    @text.setter
    def text(self, text: Optional[str | Text]) -> None:
        """Set the text of the gradient."""
        log.debug(f"Setting gradient._text: {text}")
        if isinstance(text, Text):
            sanitized_text = strip_control_codes(text.plain)
            self.length = len(sanitized_text)
            self._text = [sanitized_text]
            self._spans: List[Span] = text.spans
        if isinstance(text, str):
            if text == "":
                raise(ValueError("Text cannot be empty."))
            sanitized_text = strip_control_codes(text)
            self.length = len(sanitized_text)
            self._text = sanitized_text

    @property
    def colors(self) -> List[Color]:
        """The colors of the gradient."""
        log.debug(f"Retrieving gradient._colors: {[color.value for color in self._colors]}")
        return self._colors

    @colors.setter
    def colors(self, colors: Optional[List[Color | Tuple | str]]) -> None:
        """Set the colors of the gradient."""
        log.debug(f"Setting gradient._colors: {colors}")
        if colors is None:
            self._colors = ColorList(
                hues=self.hues, invert=self.invert).color_list[:self.hues]
        elif self.rainbow:
            if self._length < 10:
                self.hues = self._length
            else:
                self.hues = 10
            self._colors = ColorList(
                hues=self.hues, invert=self.invert).color_list
        else:
            for color in colors:
                parsed_color = Color(color)
                self._colors.append(parsed_color)
            self.hues = len(self._colors)

    @property
    def rainbow(self) -> bool:
        """Whether the gradient is rainbow."""
        log.debug(f"Retrieving gradient._rainbow: {self._rainbow}")
        return self._rainbow

    @rainbow.setter
    def rainbow(self, rainbow: bool) -> None:
        """Set whether the gradient is rainbow."""
        log.debug(f"Setting gradient._rainbow: {rainbow}")
        self._rainbow = rainbow

    @property
    def invert(self) -> bool:
        """Whether the gradient is inverted."""
        log.debug(f"Retrieving gradient._invert: {self._invert}")
        return self._invert

    @invert.setter
    def invert(self, invert: bool) -> None:
        """Set whether the gradient is inverted."""
        log.debug(f"Setting gradient._invert: {invert}")
        self._invert = invert

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
            self.text =  "█" * self._length
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
            if style == "" or style == 'null':
                self._style = Style.null()
            if style == 'none' or style == 'None':
                self._style = Style.null()
            self._style = Style.parse(style)

    def generate_style(self, color: str) -> Style:
        """Generate a style for a color."""
        new_style = self.style + Style(color=color)
        log.debug(f"Generating style for `{color}`: {new_style}")
        return new_style
