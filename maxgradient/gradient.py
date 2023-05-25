"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from typing import Any, Dict, List, Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from numpy import array_split
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.panel import Panel
from rich.repr import RichReprResult
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback
from snoop import pp, snoop

from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")


console = Console(theme=GradientTheme())
install_rich_traceback(console=console)


class NotEnoughColors(Exception):
    pass


class GradientSubstring:
    """A substring of Gradient's text. A substring is used to define a \
        gradient, when a gradient spans more than two colors.

        Args:
            substring(`str`): The substring to print. Defaults to empty string.
            start_index(`int`): The index of the substring's first character. \
                Defaults to None.
            color_start(`Color`): The color of the substring's first character. \
                Defaults to None.
            color_end(`Color`): The color of the substring's last character. \
                Defaults to None.
            style(`StyleType`): The style of the substring. Defaults to None.
            spans(`Optional[List[Span]]`): A list of predefined style spans. \
                Defaults to None.
    """

    @property
    def spans(self) -> List[Span]:
        """Return the substring's spans."""
        return self._spans

    @spans.setter
    def spans(self, spans: List[Span]) -> None:
        """Set the substring's spans."""
        self._spans = spans

    @snoop(watch_explode=('spans', 'text'))
    def __init__(
        self,
        text: str = "",
        start_index: int = None,
        color_start: Color = None,
        color_end: Color = None,
        style: StyleType = None,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Initialize a gradient's substring and calculate
        it's gradient spans."""
        if isinstance(text, List):
            text = ''.join(text)
        sanitized_text: str = strip_control_codes(text)
        self._length: int = len(sanitized_text)
        self.text: str = sanitized_text
        self.start_index: int = start_index
        self.color_start: Color = Color(color_start)
        self.color_end: Color = Color(color_end)
        if style:
            self.style: str = self.parse_style(style)
            end_style = Style.parse(f"{self.style} {self.color_end.hex}")
        else:
            self.style = Style()
            end_style = Style(color=self.color_end.hex)
        self._spans: List[Span] = [Span(0, self._length, end_style)]

        spans = self.calculate_spans_concurrently()
        self._spans = self.simplify_spans(spans)

    def __repr__(self) -> str:
        """Return the substring's representation."""
        return f"GradientSubstring(text={self.text}, start_index={self.start_index}, color_start={self.color_start}, color_end={self.color_end}, style={self.style}, spans={self.spans})"

    def __rich_repr__(self) -> Text:
        """Return the gradient's substring."""
        if len(self.text) > console.width / 2 - 2:
            text = self.text[: console.width / 2 - 5] + "..."
        else:
            text = self.text
        text = Text(f'"{text}"', style="bold white")
        hyphen = "[bold dim #cccccc] - [/]"
        colors = []
        for color in [self.start_color, self.end_color]:
            color = Color(color)
            colors.append(f"[bold {color.hex}]{color._original.capitalize()}[/]")
        color_string = Text.from_markup(hyphen.join(colors))
        table = Table(
            title="GradientSubstring", show_header=False, border_style="bold #666666"
        )
        table.add_column("Attribute", style="i #5f00ff", justify="right")
        table.add_column("Value", style="b #af00ff")
        table.add_row("Text", f"[bold #FDFDBD]{text}[/]")
        table.add_row("Start Index", f"[bold #00ffff]{self.start_index}[/]")
        table.add_row(
            "Color Start",
            Text(
                self.color_start._original.capitalize(),
                style=f"bold {self.color_start.hex}",
            ),
        )
        table.add_row(
            "Color End",
            Text(
                self.color_end._original.capitalize(),
                style=f"bold {self.color_end.hex}",
            ),
        )
        table.add_row("Style", str(self.style))
        return table

    @snoop
    def calculate_spans_concurrently(self) -> None:
        """Calculate the gradient's spans concurrently."""
        with ThreadPoolExecutor(max_workers=cpu_count() - 1) as executor:
            result = executor.map(self._calculate_span, range(self._length))
        return list(result)

    @snoop
    def _calculate_span(self, index: int) -> Span:
        """Calculate the gradient's span at the given index."""
        blend = index / self._length
        span_start = self.start_index + index
        r1, g1, b1 = self.color_start.rgb_tuple
        r2, g2, b2 = self.color_end.rgb_tuple
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1

        span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
        span_style = f"{self.style} {span_color}".strip()

        return Span(span_start, span_start + 1, span_style)

    @staticmethod
    def parse_style(style: StyleType) -> str:
        if isinstance(style, Style):
            style = style.without_color
            style = str(style)
            return style
        elif style is None:
            return ""
        else:
            try:
                style = Style.parse(style).without_color
                style = str(style)
                return style
            except:
                raise ValueError(
                    "Style must be a Style object or a string that can be parsed into a Style object."
                )

    def simplify_spans(self, spans: List[Span]) -> List[Span]:
        """Simplify the spans by combining spans with the same style."""
        simplified_spans: List[Span] = []
        for index, span in enumerate(spans):
            if index == 0:
                last_span = span
            else:
                if span.style == last_span.style:
                    start = last_span.start
                    last_span = Span(start, span.end, span.style)
                else:
                    simplified_spans.append(last_span)
                    last_span = span
        return simplified_spans
register_repr(GradientSubstring)(normal_repr)

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

    @snoop(watch=("gradient_spans", "substrings"))
    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = None,
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None
    ) -> None:
        """Initialize the Gradient class."""
        match = WHITESPACE_REGEX.match(text)
        if match:
            text = Text.from_markup(match.group(0))
            return

        # Text entered
        if isinstance(text, Text):
            spans = text._spans
            text = text.plain

        # Style
        self.style: str = self.parse_style(style)
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
                        parsed_color = Color(color)
                        self._colors.append(parsed_color)
                    except:
                        print(f"Unable to parse color: {color}")
            self.hues = len(self._colors)

        else:
            self.hues = 10
            self._colors = ColorList(self.hues, self.invert).color_list
            # self._colors = color_list.color_list

        if self._length < self.hues:
            msg = (
                "The entered text is to short to display the number of colors entered."
            )
            raise NotEnoughColors(f"{msg} Please enter more text or fewer colors.")

        # gradient_spans
        self._spans = self.generate_gradient_spans()

        # text substring

    def generate_gradient_spans(self) -> List[Span]:
        """Separate the Gradient into substrings for each color gradient."""
        num_of_substrings = len(self._colors) - 1
        substring_sizes = array_split(range(self._length), num_of_substrings)

        spans: List[Span] = []
        for index, substring_size in enumerate(substring_sizes):
            start: int = substring_size[0]
            end: int = substring_size[-1]
            substring = self._text[start:end]
            color1 = self._colors[index]
            color2 = self._colors[index + 1]
            substring_spans = GradientSubstring(
                text=substring,
                start_index=start,
                color_start = color1,
                color_end = color2,
                style = self.style).spans
            if index == 0:
                spans = substring_spans
            else:
                spans += substring_spans
        return self.simplify_spans(spans)

    def simplify_spans(self, spans: List[Span]) -> List[Span]:
        """Simplify the spans by combining spans with the same style."""
        simplified_spans: List[Span] = []
        for index, span in enumerate(spans):

            if index == 0:
                start = span.start
                end = span.end
                style = span.style
                last_span = Span(start, end, style)
            else:
                if span.style == last_span.style:
                    start = last_span.start
                    last_span = Span(start, span.end, span.style)
                else:
                    simplified_spans.append(last_span)
                    last_span = span
        return simplified_spans

    @staticmethod
    def parse_style(style: StyleType) -> str:
        if isinstance(style, Style):
            style = style.without_color
            style = str(style)
            if 'none ' in style:
                style = style.replace('none ', '')
        elif style is None:
            if 'none ' in style:
                style = style.replace('none ', '')
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
        width = console.width * 0.8 - 2
        if len(self.plain) > width:
            text = f"{self.plain[:width-3]}..."
        else:
            text = self.plain

        colors = [
            f"[bold {color.hex}]{color._original.capitalize()}[/]"
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
    console.print(random_gradient, justify="center")
