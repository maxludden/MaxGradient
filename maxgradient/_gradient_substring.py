"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from typing import Any, Dict, List, Optional, Tuple
from random import choice, randint

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


class GradientSubstring(Text):
    """A substring of Gradient's text. A substring is used to define a \
        gradient, when a gradient spans more than two colors.

        Args:
            text(`str`): The substring to print. Defaults to empty string.\n\n
            start_index(`int`): The index of the substring's first character. \
                Defaults to None.\n\n
            color_start(`Color`): The color of the substring's first character. \
                Defaults to None.\n\n
            color_end(`Color`): The color of the substring's last character. \
                Defaults to None.\n\n
            style(`StyleType`): The style of the substring. Defaults to None.
            spans(`Optional[List[Span]]`): A list of predefined style spans. \
                Defaults to None.\n\n
    """

    @property
    def spans(self) -> List[Span]:
        """Return the substring's spans."""
        return self._spans

    def spans(self, spans: List[Span]) -> None:
        """Set the substring's spans."""
        self._spans = spans

    @snoop(watch=("end_style"))
    def __init__(
        self,
        text: str = "",
        start_index: int = None,
        color_start: Color = None,
        color_end: Color = None,
        style: StyleType = None,
        spans: Optional[List[Span]] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        no_wrap: bool = False,
        end: str = "\n",
        tab_size: int = 8,
    ) -> None:
        """Initialize a gradient's substring and calculate
        it's gradient spans."""
        super().__init__(
            text=text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size
        )
        if isinstance(text, List):
            text = ''.join(text)
        sanitized_text: str = strip_control_codes(text)
        self._length: int = len(sanitized_text)
        self.text: str = sanitized_text
        self.start_index: int = start_index
        self.color_start: Color = Color(color_start)
        self.color_end: Color = Color(color_end)
        if style:
            console.log("if style:\n\n")
            self.style: str = self.parse_style(style)
            end_style = Style.parse(f"{self.style} {self.color_end.hex}")
            console.log("end_style:", end_style)
        else:
            console.log("if not style:\n\n")
            self.style = Style.null()
            end_style = Style(color=self.color_end.hex)
            console.log("end_style:", end_style)
        self._spans: List[Span] = [Span(0, self._length-1, end_style)]

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

    # @snoop
    def calculate_spans_concurrently(self) -> None:
        """Calculate the gradient's spans concurrently."""
        with ThreadPoolExecutor(max_workers=cpu_count() - 1) as executor:
            result = executor.map(self._calculate_span, range(self._length))
        return list(result)

    # @snoop
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


if __name__ == "__main__":
    console = Console(theme=GradientTheme())
    colors = Color.COLORS
    TEXT = lorem.paragraphs(2)
    gradient = GradientSubstring(
        text=TEXT,
        start_index=0,
        color_start=Color(choice(colors)),
        color_end=Color(choice(colors)),
        style="bold italic"
    )
    console.print(gradient)