# ruff: noqa: F401
import re
from functools import partial
from operator import itemgetter
from timeit import timeit
from typing import Any, Dict, Generator, Iterable, List, Literal, Optional, Tuple

import numpy as np
import rich.style
from cheap_repr import normal_repr, register_repr
from pydantic_core import PydanticCustomError
from pydantic_extra_types.color import ColorType
from rich import inspect
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
from snoop import pp, snoop

from maxgradient._simple_gradient import SimpleGradient
from maxgradient.color import Color
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

GradientMethod = Literal["default", "list", "mono", "rainbow"]
DEFAULT_JUSTIFY: JustifyMethod = "default"
DEFAULT_OVERFLOW: OverflowMethod = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")

console = Console(theme=GradientTheme().theme)
tr_install(console=console, show_locals=True)
VERBOSE: bool = True


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
        "_end",
        "_hues",
        "_justify",
        "_no_wrap",
        "_overflow",
        "_style",
        "_spans",
        "_rainbow",
        "verbose",
    ]

    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[ColorType | Color]] = None,
        *,
        rainbow: bool = False,
        hues: int = 4,
        style: StyleType = Style.null(),
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: Optional[str] = "\n",
        tab_size: Optional[int] = 4,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """
        Text styled with gradient color.

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
        self.justify = justify or DEFAULT_JUSTIFY
        self.overflow = overflow or DEFAULT_OVERFLOW

        self.style = Style.parse(style) if isinstance(style, str) else style
        self.colors = self.validate_colors(colors, rainbow=rainbow)
        
        super().__init__(
            text=self.text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=self.end or "\n",
            tab_size=tab_size,
            spans=spans,
        )
        subgradients = self.generate_subgradients()
        self._spans = self.join_subgradients(subgradients).spans


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
            # if value == "":
            #     raise ValueError("Text cannot be empty.")
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
    def justify(self) -> str:
        """The justify method of the gradient."""
        if self._justify is not None:
            return self._justify
        return DEFAULT_JUSTIFY

    @justify.setter
    def justify(self, justify: JustifyMethod) -> None:
        """Set the justify method of the gradient.

        Args:
            justify (JustifyMethod): The justify method of the gradient.
        """
        self._justify = justify

    @property
    def overflow(self) -> str:
        """The overflow method of the gradient."""
        if self._overflow is not None:
            return self._overflow
        return DEFAULT_OVERFLOW

    @overflow.setter
    def overflow(self, overflow: OverflowMethod) -> None:
        """Set the overflow method of the gradient.

        Args:
            overflow (OverflowMethod): The overflow method of the gradient.
        """
        self._overflow = overflow

    @property
    def no_wrap(self) -> Optional[bool]:
        """Whether to wrap the gradient text."""
        try:
            return self._no_wrap
        except AttributeError:
            return None

    @no_wrap.setter
    def no_wrap(self, no_wrap: Optional[bool]) -> None:
        """Set whether to wrap the gradient text.

        Args:
            no_wrap (bool): Whether to wrap the gradient text.
        """
        self._no_wrap = no_wrap

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

    @property
    def end(self) -> Optional[str]:
        """The end character of the gradient."""
        try:
            return self._end
        except AttributeError:
            return "\n"

    @end.setter
    def end(self, end: Optional[str]) -> None:
        """Set the end character of the gradient.

        Args:
            end (str): The end character of the gradient.
        """
        self._end = end

    @property
    def colors(self) -> List[Color]:
        """The colors in the gradient."""
        return self._colors

    @colors.setter
    def colors(self, colors: Optional[List[ColorType]] | Optional[List[Color]]) -> None:
        """Set the colors in the gradient.

        Args:
            colors (List[Color]): The colors in the gradient.
        """
        _colors = self.validate_colors(colors)
        console.log(f"Gradient with {self.hues} colors:", _colors)
        self._colors: List[Color] = _colors

    def validate_colors(
        self,
        colors: Optional[List[ColorType]] | Optional[List[Color]],
        rainbow: bool = False,
    ) -> List[Color]:
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
        _colors: List[Color] = []
        if colors is None:
            color_list = ColorList(hues=self.hues)
            for color in color_list:
                _colors.append(color)
            console.log(f"[green]Generated {self.hues} colors:[/]", _colors)
            return _colors
        elif rainbow:
            _colors = ColorList(hues=20)
            console.log(f"Rainbow gradient with {self.hues} colors:", _colors)
            return _colors
        elif isinstance(colors, (List, Tuple)):
            for color in colors:
                try:
                    color = Color(color)
                except PydanticCustomError as pce:
                    raise pce
                else:
                    _colors.append(color)
            console.log(
                f"[green]Validated [/][b i #00ff00]{len(colors)}[/][greeen] colors:[/]",
                _colors,
            )
            assert len(_colors) >= 2, "Gradient must have at least two colors."
            return _colors
        raise TypeError(f"Colors must be a list or tuple, not {type(colors)}.")

    def _base_span(self) -> None:
        if not hasattr(self, "_spans"):
            self._spans = [Span(0, self._length - 1, self.style)]

    @property
    def spans(self) -> List[Span]:
        """The spans of the gradient."""
        self._base_span()
        return self._spans

    @spans.setter
    def spans(self, spans: List[Span]) -> None:
        """Set the spans of the gradient.

        Args:
            spans (List[Span]): The spans of the gradient.
        """
        self._spans = spans

    def get_substrings(self) -> List[str]:
        """Chunk the text into a list of strings.

        Returns:
            List[str]: The list of strings.
        """
        result = np.array_split(np.arange(self._length), self.hues - 2)  # noqa: F722
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        substrings: List[str] = []
        for index in indexes:
            start = index[0]
            end = index[-1]
            substring: str = self._text[start : end + 1]
            substrings.append(substring)
        return substrings

    def generate_subgradients(self) -> List[SimpleGradient]:
        """Generate simple gradients.

        Returns:
            List[SimpleGradient]: The list of simple gradients.
        """
        substrings: List[str] = self.get_substrings()
        colors = self.colors
        if VERBOSE:
            for index, substring in enumerate(substrings):
                console.log(f"Substring {index}: {substring}")
            console.log(f"Colors: {colors}")
        assert len(substrings) + 1 == len(
            colors
        ), "Number of indexes and colors must match."
        subgradients: List[SimpleGradient] = []
        for index, substring in enumerate(substrings):
            color1 = colors[index]
            color2 = colors[index + 1]
            gradient = SimpleGradient(
                substring, # type: ignore
                color1=color1,
                color2=color2,
                justify=self.justify,  # type: ignore
                overflow=self.overflow,  # type: ignore
                style=self.style,
                no_wrap=self.no_wrap or False,
                end=self.end or "\n",
                spans=self.spans,
            )
            console.print(
                Text.assemble(
                    *[Text.from_markup(f"[dim italic]{index}: [/]", end=""), gradient]
                )
            )
            subgradients.append(gradient)
        return subgradients

    @classmethod
    def join_subgradients(cls, subgradients: List[SimpleGradient]) -> Text:
        """Join the subgradients into a single gradient.

        Args:
            subgradients (List[SimpleGradient]): The list of subgradients.

        Returns:
            Text: The joined gradient.
        """
        gradient = cls.assemble(*[gradient for gradient in subgradients])
        return gradient

    def as_text(self) -> Text:
        """Convert the gradient to a `Text`.

        Returns:
            Text: The gradient as a `rich.text.Text` object.
        """
        overflow: OverflowMethod = DEFAULT_OVERFLOW
        justify: JustifyMethod = DEFAULT_JUSTIFY
        if self.justify is None:
            justify = DEFAULT_JUSTIFY
        if self.overflow is None:
            overflow = DEFAULT_OVERFLOW
        return Text(
            text=self.text,
            style=self.style,
            justify=justify,
            overflow=overflow,
            no_wrap=self.no_wrap,
            end=self.end or "\n",
            tab_size=self.tab_size,
            spans=self._spans,
        )


if __name__ == "__main__":
    from lorem_text import lorem
    from rich.console import Console
    from rich.traceback import install as tr_install

    tr_install(console=Console())
    console.line(2)
    text = str(lorem.paragraphs(2))
    console.print(Gradient(text, colors=["red", "orange", "yellow"]))
