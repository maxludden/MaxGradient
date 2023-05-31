"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from itertools import repeat
from multiprocessing import cpu_count
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from numpy import array_split, ndarray
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

    __slots__ = ["_colors", "invert", "color_sample", "hues"]

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
        """Initialize the Gradient class."""
        text = str(text)
        match = WHITESPACE_REGEX.match(text)
        if match:
            text = Text.from_markup(match.group(0))
            return
        if not text:
            return

        # Text entered
        if isinstance(text, Text):
            spans = text._spans
            text = text.plain

        # Style
        if isinstance(style, Style):
            style = str(style)
        self.style: str = style
        # self.style = style

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

        # text
        sanitized_text: str = strip_control_codes(text)
        self._length: int = len(sanitized_text)

        # invert
        self.invert: bool = invert

        # Color Sample
        self.color_sample: bool = color_sample
        if self.color_sample:
            self._text = "█" * self._length

        # hues
        if hues is not None:
            self.hues = hues
        else:
            self.hues = 3

        # colors
        self._colors: List[Color] = []
        if not rainbow:
            if colors is None:
                self._colors = ColorList(self.hues, self.invert).color_list
                # self._colors = color_list.color_list
            else:
                for color in colors:
                    try:
                        parsed_color = Color(color)  # type: ignore
                        self._colors.append(parsed_color)
                    except:
                        print(f"Unable to parse color: {color}")
            self.hues = len(self._colors)

        else:
            self.hues = 10
            self._colors = ColorList(self.hues, self.invert).color_list
            # self._colors = color_list.color_list

        assert (
            self._length > self.hues
        ), "Text must be longer than the number of colors."
        self._spans = self.calculate_spans_concurrently()

        # substrings

    def calculate_spans_concurrently(self) -> List[Span]:
        num_of_gradients = self.hues - 1
        substring_arrays: List[ndarray] = array_split(
            range(self._length), num_of_gradients
        )
        substring_lists: List[List[int]] = [
            array.tolist() for array in substring_arrays
        ]
        spans: List[Span] = []
        for main_index, substring_list in enumerate(substring_lists):
            color_1 = self._colors[main_index]
            color_2 = self._colors[main_index + 1]
            styles = self.style
            args = zip(
                substring_list,
                repeat(self._length),
                repeat(color_1),
                repeat(color_2),
                repeat(styles),
            )

            with ThreadPoolExecutor(max_workers=cpu_count() - 1) as executor:
                future_results = executor.submit(self._calculate_span, *args)

                for result in future_results:
                    spans.append(result)
        return spans

    def _calculate_span(
        self, index: int, length: int, color_1: Color, color_2: Color, style: str
    ) -> Span:
        """Calculate a span."""
        blend = index / length
        r1, g1, b1 = color_1.rgb_tuple
        r2, g2, b2 = color_2.rgb_tuple
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1

        span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
        span_style = f"{style} {span_color}".strip()

        return Span(index, index + 1, span_style)

    @staticmethod
    def parse_style(style: StyleType) -> str:  # type: ignore
        if isinstance(style, Style):
            style = style.without_color
            style = str(style)
            if "none " in style:
                style = style.replace("none ", "")
        elif style is None:
            if "none " in style:
                style = style.replace("none ", "")
            style = Style.null()
        else:
            try:
                style = Style.parse(style).without_color
                style = str(style)
                return style
            except:
                raise ValueError(
                    "Style must be a Style object or a string that can be parsed into a Style object."
                )

    def __repr__(self) -> str:
        """Return the representation of the Gradient class."""
        width = console.width * 0.8 - 2
        if len(self.plain) > width:
            text = f"{self.plain[:width-3]}..."
        else:
            text = self.plain
        colors = [str(color) for color in self._colors]
        color_strings = ", ".join(colors)
        return f"Gradient({text}, colors=[{color_strings}])"

    def __rich_repr__(self) -> Table:
        """Return the rich representation of the Gradient class."""
        width = int(console.width * 0.8 - 2)
        if len(self.plain) > width:
            text = f"{self.plain[:width-3]}..."
        else:
            text = self.plain

        colors = [
            f"[bold {color.hex}]{str(color._original).capitalize()}[/]"
            for color in self._colors
        ]
        comma = "[dim #ffffff], [/]"
        colors = Text.from_markup(comma.join(colors))

        table = Table(
            title="[b i #5f00ff]Gradient[/]",
            show_header=False,
            border_style="b dim #5f00ff",
            width=width,
        )
        table.add_column("Attribute", style="italic #5f00ff", justify="center")
        table.add_column("Value", style="bold", justify="left")
        table.add_row("Text", text)
        table.add_row("Colors", colors)
        return table


register_repr(Gradient)(normal_repr)
register_repr(GradientSubstring)(normal_repr)

if __name__ == "__main__":
    from rich.console import Console
    from rich.traceback import install as install_rich_traceback

    from maxgradient.theme import GradientTheme

    console = Console(theme=GradientTheme())
    install_rich_traceback(console=console)

    random_gradient_text: str = "Gradient is a Python library for creating \
beautiful color gradients."
    random_gradient: Gradient = Gradient(random_gradient_text)
    console.print(random_gradient, justify="center")
