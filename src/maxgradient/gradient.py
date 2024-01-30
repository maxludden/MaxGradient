# ruff: noqa: F401
import re
from pathlib import Path
from typing import List, Literal, Optional, Tuple

import numpy as np
import rich.style
from pydantic_core import PydanticCustomError
from pydantic_extra_types.color import ColorType
from rich import get_console
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.style import Style, StyleType
from rich.panel import Panel
from rich.text import Span, Text
from rich.traceback import install as tr_install

from maxgradient._simple_gradient import SimpleGradient
from maxgradient.color import Color
from maxgradient.color_list import ColorList
from maxgradient.theme import GRADIENT_TERMINAL_THEME, GradientTheme


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
        verbose: bool = False,
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
            hues (int): The number of colors in the gradient. Defaults to `4`.\n
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

        self.verbose = verbose or False
        self.text = text
        self.hues = hues
        self.justify = justify or DEFAULT_JUSTIFY
        self.overflow = overflow or DEFAULT_OVERFLOW
        self.style = Style.parse(style) if isinstance(style, str) else style
        self.colors = self.validate_colors(colors, rainbow=rainbow)
        if len(self.colors) > 2:
            self.hues = len(self.colors)
        else:
            self.hues = hues
        self.verbose: bool = verbose

        super().__init__(
            text=self.text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end or "\n",
            tab_size=tab_size or 4,
            spans=spans,
        )
        indexes = self.generate_indexes()
        substrings = self.generate_substrings(indexes)
        subgradients = self.generate_subgradients(substrings)
        self._spans = self.join_subgradients(subgradients).spans

    @property
    def text(self) -> str:
        """
        Returns the concatenated string representation of the `_text` attribute.

        Returns:
            str: The concatenated string representation of the `_text` attribute.
        """
        return "".join(self._text) if isinstance(self._text, list) else self._text

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
        if self.verbose:
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
            if not rainbow:
                color_list = ColorList(self.hues)
                for index, color in enumerate(color_list):
                    if self.verbose:
                        console.rule(
                            f"[b i #ffffff]Generated color[/] [b #ff00ff]{index + 1}[/]"
                        )
                        console.print(
                            Text(color.as_named(), style=color.as_named()),
                            justify="center",
                        )
                    _colors.append(color)
                    if index == self.hues - 1:
                        break
                if self.verbose:
                    console.log(f"[green]Generated {self.hues} colors:[/]", _colors)
                return _colors
            else:
                self.hues = 20
                if self._length < 20:
                    self.hues = self._length
                color_list = ColorList(self.hues)
                for index, color in enumerate(color_list):
                    if self.verbose:
                        console.rule(
                            f"[b i #ffffff]Generated color[/] [b #ff00ff]{index + 1}[/]"
                        )
                        console.print(
                            Text(color.as_named(fallback=True), style=color.as_named()),
                            justify="center",
                        )
                    _colors.append(color)
                    if index == self.hues - 1:
                        break
                if self.verbose:
                    console.log(f"[green]Generated {self.hues} colors:[/]", _colors)
                return _colors
        elif isinstance(colors, (List, Tuple)):
            for color in colors:
                try:
                    color = Color(color)
                except PydanticCustomError as pce:
                    raise pce
                else:
                    _colors.append(color)
            if self.verbose:
                console.log(
                    f"[green]Validated [/][b i #00ff00]{len(colors)}[/][green] colors:[/]",
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

    def generate_indexes(self) -> List[List[int]]:
        """Chunk the text into a list of strings.

        Returns:
            List[str]: The list of strings.
        """
        if self.verbose:
            console.log(f"Text: {self.text}")
            console.log(f"Length: {self._length}")
            console.log(f"Hues: {self.hues}")
        result = np.array_split(np.arange(self._length), self.hues - 1)  # noqa: F722

        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        if self.verbose:
            index_text = Text(" ".join([f"{index}" for index in indexes]))
            console.print(index_text)
        return indexes

    def generate_substrings(self, indexes: List[List[int]]) -> List[str]:
        substrings: List[str] = []
        slices: List[Tuple[int, int]] = []
        for index in indexes:
            start = index[0]
            end = index[-1] + 1
            slices.append((start, end))
            if self.verbose:
                console.log(f"Start: {start}", f"End: {end}")

        if isinstance(self.text, list):
            text = " ".join(self.text)
        elif isinstance(self.text, str):
            text = self.text
        else:
            raise TypeError(f"Text must be a string or list, not {type(self.text)}")
        for index, (start, end) in enumerate(slices, 1):
            substring = text[start:end]
            substrings.append(substring)
            if self.verbose:
                console.rule(f"Substring {index}")
                console.print(substring)
        return substrings

    def generate_subgradients(self, substrings: List[str]) -> List[SimpleGradient]:
        """Generate simple gradients.

        Returns:
            List[SimpleGradient]: The list of simple gradients.
        """
        subgradients: List[SimpleGradient] = []

        for index, substring in enumerate(substrings):
            color1 = self.colors[index]
            color2 = self.colors[index + 1]
            gradient = SimpleGradient(
                substring,  # type: ignore
                color1=color1,
                color2=color2,
                justify=self.justify,  # type: ignore
                overflow=self.overflow,  # type: ignore
                style=self.style,
                no_wrap=self.no_wrap or False,
                end=self.end or "\n",
                spans=self.spans,
            )
            if self.verbose:
                console.print(f"[b i dim]Index {index}[/]")
                console.print(gradient)
            subgradients.append(gradient)
        return subgradients

    def join_subgradients(self, subgradients: List[SimpleGradient]) -> Text:
        """Join the subgradients into a single gradient.

        Args:
            subgradients (List[SimpleGradient]): The list of subgradients.

        Returns:
            Text: The joined gradient.
        """
        result = Text()
        for gradient in subgradients:
            if self.verbose:
                console.print(gradient)
            result.append(gradient)

        return result

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

    @classmethod
    def named_gradient_example(
        cls,
        save: bool = False,
        path: str = str(Path.cwd() / "docs" / "img" / "named_gradient_example.svg"),
    ) -> None:
        """
        Generate an example of a gradient with defined colors.
    
        Args:
            save (bool, optional): Whether to save the gradient to a file. Defaults to False.
            filename (Optional[Path], optional): The filename to save the gradient to. Defaults \
        to Path("/Users/maxludden/dev/py/MaxGradient/docs/img/named_gradient_example.svg").
                console (Console, optional): The console to print the gradient to. Defaults to console.
        """
        if save:
            console = Console(width=60, record=True)
        else:
            console = Console(width=60)
        gradient = Gradient(
            "The quick brown fox jumps over the lazy dog.",
            colors=["magenta", "purple", "blueviolet"],
        )
        panel_content = Text.assemble(
            gradient,
            Text("\n\nThis gradient starts with "),
            Text("magenta", style = "b #ff00ff"),
            Text(". It fades to "),
            Text("purple", style = "b #af00ff"),
            Text(", and ends in "), 
            Text("blueviolet", style = "b #5f00ff"),
            Text("."),
            justify="center"
        )
        console.line(2)
        console.print(
            Panel(
                panel_content,
                title="[b #ffffff]Named Gradient[/]",
                padding=(1,4),
            ),
            justify="center",
        )
        if save:
            console.save_svg(path, title="MaxGradient", theme=GRADIENT_TERMINAL_THEME)

    @classmethod
    def random_gradient_example(
        cls,
        save: bool = False,
        path: str = str(Path.cwd() / "docs" / "img" / "random_gradient_example.svg"),
    ) -> None:
        """
        Generate an example of a gradient with random adjacent colors.
    
        Args:
            save (bool, optional): Whether to save the gradient to a file. Defaults to False.
            filename (Optional[Path], optional): The filename to save the gradient to. Defaults \
        to Path("/Users/maxludden/dev/py/MaxGradient/docs/img/named_gradient_example.svg").
                console (Console, optional): The console to print the gradient to. Defaults to console.
        """
        if save:
            console = Console(width=60, record=True)
        else:
            console = Console(width=60)
        console.line(2)
        console.print(
            Panel(
                Gradient(
                    text="The quick brown fox jumps over the lazy dog.",
                    justify="center",
                ),
                title="[b #ffffff]Random Gradient[/b #ffffff]",
                padding=(1,4)
            ),
            justify="center",
        )
        console.line(2)
        if save:
            console.save_svg(path, title="MaxGradient", theme=GRADIENT_TERMINAL_THEME)

    @classmethod
    def rainbow_gradient_example(
        cls,
        save: bool = False,
        path: str = str(Path.cwd() / "docs" / "img" / "rainbow_gradient_example.svg"),
    ) -> None:
        """
        Generate an example of a gradient with the whole spectrum of colors.
    
        Args:
            save (bool, optional): Whether to save the gradient to a file. Defaults to False.
            filename (Optional[Path], optional): The filename to save the gradient to. Defaults \
        to Path("/Users/maxludden/dev/py/MaxGradient/docs/img/named_gradient_example.svg").
                console (Console, optional): The console to print the gradient to. Defaults to console.
        """
        if save:
            console = Console(width=60, record=True)
        else:
            console = Console(width=60)

        console.line(2)
        console.print(
            Panel(
                Gradient(
                    text="The quick brown fox jumps over the lazy dog.",
                    rainbow=True,
                    justify="center",
                ),
                title=Gradient("Rainbow Gradient", rainbow=True),
                padding=(1,4)
            ),
            justify="center",
        )
        console.line(2)
        if save:
            console.save_svg(path, title="MaxGradient", theme=GRADIENT_TERMINAL_THEME)

    @classmethod
    def example(cls) -> None:
        Gradient.named_gradient_example()
        Gradient.random_gradient_example()
        Gradient.rainbow_gradient_example()


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console
    from rich.traceback import install as tr_install

    from lorem_text import lorem

    Gradient.example()
