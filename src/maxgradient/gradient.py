# ruff: noqa: F401
import re
from functools import partial
from operator import itemgetter
from timeit import timeit
from typing import Any, Dict, Generator, Iterable, List, Literal, Optional, Tuple

import numpy as np
import rich.style
from maxgradient._simple_gradient import SimpleGradient
from maxgradient.color import Color, PyColorType
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme
from rich._pick import pick_bool
from rich.cells import cell_len
from rich.console import Console, ConsoleOptions, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as tr_install

GradientMethod = Literal["default", "list", "mono", "rainbow"]
DEFAULT_JUSTIFY: JustifyMethod = "default"
DEFAULT_OVERFLOW: OverflowMethod = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")

console = Console(theme=GradientTheme().theme)
tr_install(console=console, show_locals=True)
VERBOSE: bool = False


class Gradient(Text):
    """Text styled with gradient color.

        Args:
            text (text): The text to print. Defaults to `""`.\n
            colors (List[Optional[Color|Tuple|str|int]]): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow (bool): Whether to print the gradient text in rainbow colors\
                  across the spectrum. Defaults to False.\n
            hues (int): The number of colors in the gradient. Defaults to `3`.\n
            style (StyleType): The style of the gradient text. Defaults to None.\n
            verbose (bool): Whether to print verbose output. Defaults to False.
            justify (Optional[JustifyMethod]): Justify method: "left", "center",\
                "full", "right". Defaults to None.\n
            overflow (Optional[OverflowMethod]):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use\
                `console.tab_size`. Defaults to 4.\n
            spans (List[Span], optional): A list of predefined style spans.\
                Defaults to None.\n
    """

    __slots__ = [
        "_colors",
        "_text",
        "_length",
        "length",
        "_hues",
        "_style",
        "_spans",
        "_rainbow",
        "verbose",
    ]

    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[PyColorType]] = None,
        *,
        rainbow: bool = False,
        hues: int = 4,
        style: StyleType = Style.null(),
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 4,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Text styled with gradient color.

        Args:
            text (text): The text to print. Defaults to `""`.\n
            colors (List[Optional[Color|Tuple|str|int]]): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow (bool): Whether to print the gradient text in rainbow colors\
                  across the spectrum. Defaults to False.\n
            hues (int): The number of colors in the gradient. Defaults to `3`.\n
            style (StyleType): The style of the gradient text. Defaults to None.\n
            verbose (bool): Whether to print verbose output. Defaults to False.
            justify (Optional[JustifyMethod]): Justify method: "left", "center",\
                "full", "right". Defaults to None.\n
            overflow (Optional[OverflowMethod]):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use\
                `console.tab_size`. Defaults to 4.\n
            spans (List[Span], optional): A list of predefined style spans.\
                Defaults to None.\n

        """
        self.text = text
        self.hues = hues
        if rainbow:
            self.hues = 18
        self.style = Style.parse(style) if isinstance(style, str) else style

        super().__init__(
            text=self.text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size,
            spans=spans,
        )

        self._colors = self.validate_colors(colors)

        self._spans = list(self.generate_spans())

    @property
    def text(self) -> str:
        """
        Returns the concatenated string representation of the `_text` attribute.

        Returns:
            str: The concatenated string representation of the `_text` attribute.
        """
        return "".join(self._text)

    @text.setter
    def text(self, value: Optional[str] | Optional[Text]) -> None:
        """
        Setter for the text attribute.

        Args:
            value (str|Text): The value to set for the text attribute.

        Returns:
            None
        """
        if isinstance(value, Text):
            sanitized_text = strip_control_codes(value.plain)
            self._length = len(sanitized_text)
            self._text = sanitized_text
            self._spans = value.spans
        elif isinstance(value, str):
            if value == "":
                raise ValueError("Text cannot be empty.")
            sanitized_text = strip_control_codes(value)
            self._length = len(sanitized_text)
            self._text = sanitized_text
        elif value is None:
            raise ValueError("Text cannot be None.")
        else:
            raise TypeError(f"Text must be a string or Text, not {type(value)}")

    @property
    def hues(self) -> int:
        """The number of colors in the gradient."""
        return self._hues

    @hues.setter
    def hues(self, hues: int) -> None:
        """Set the number of colors in the gradient.

        Args:
            hues (int): The number of colors in the gradient. Defaults to `4`.
        """

        if hues < 2:
            raise ValueError("Gradient must have at least two colors.")
        self._hues = hues

    @property
    def style(self) -> Style:
        """The style of the gradient."""
        return self._style

    @style.setter
    def style(self, style: StyleType) -> None:
        """
        Setter for the style attribute.

        Args:
            style (StyleType): The value to set for the style attribute.
        """
        if style is None:
            self._style = Style.null()
        elif isinstance(style, rich.style.Style):
            self._style = style
        else:
            self._style = Style.parse(style)

    def validate_colors(self, colors: Optional[List[PyColorType]]) -> List[Color]:
        """Validate input colors, and convert them into `Color` objects.

        Colors may be passed in as strings or tuples, names, or Color objects.
        If no colors are provided, a random gradient will be generated.

        Args:
            colors (List[ColorType]): The colors to validate and convert

        Returns:
            List[Color]: The validated colors.

        Raises:
            PydanticCustomError: If any of the colors are invalid.
        """
        if colors is None:
            for color in ColorList(hues=self.hues):
                
