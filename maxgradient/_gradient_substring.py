"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from random import choice, randint
from typing import Any, Dict, List, Optional, Tuple

from cheap_repr import normal_repr, register_repr
# from lorem_text import lorem

from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback
from snoop import pp, snoop

from examples.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False


console = Console(theme=GradientTheme())
install_rich_traceback(console=console)


class NotEnoughColors(IndexError):
    """Custom exceptions raised when there are not enough characters to \
        create a gradient."""

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
            style(`StyleType`): The style of the substring. Defaults to None.\n\n
            spans(`Optional[List[Span]]`): A list of predefined style spans. \
                Defaults to None.\n\n
    """

    def __init__(
        self,
        text: str,
        start_index: int,
        color_start: Color,
        color_end: Color,
        style: str,
        spans: Optional[List[Span]] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        overflow: OverflowMethod = DEFAULT_OVERFLOW,
        no_wrap: bool = False,
        end: str = "",
        tab_size: int = 8,
    ) -> None:
        """Initialize a gradient's substring and calculate
        it's gradient spans."""

        # Text
        if isinstance(text, List):
            text = "".join(text)
        sanitized_text: str = strip_control_codes(text)
        self._length: int = len(sanitized_text)
        self.text: str = sanitized_text

        super().__init__(
            text=text,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size,
        )

        # Start index
        self.start_index: int = int(start_index)

        # Colors
        self.color_start: Color = color_start
        self.color_end: Color = color_end

        # Style
        end_style: Style = Style.null()
        if style:
            if isinstance(style, str):
                self.style: str = self.parse_style(style)  # type: ignore
                end_style = Style.parse(f"{self.style} {self.color_end.hex}")
            elif isinstance(style, Style):
                self.style: str = style
                end_style = Style.parse(f"{self.style} {self.color_end.hex}")
        else:
            self.style = Style.null()  # type: ignore
            end_style = Style(color=self.color_end.hex)

        # Spans
        initial_spans: List[Span] = [Span(0, self._length - 1, end_style)]
        initial_spans.extend(self.calculate_spans_concurrently())  # type: ignore
        simplified_spans = self.simplify_spans(initial_spans)
        self._spans = simplified_spans

    @property
    def spans(self) -> List[Span]:
        """Return the substring's spans."""
        return self._spans

    @spans.setter
    def spans(self, spans: List[Span]) -> None:
        """Set the substring's spans."""
        self._spans = spans

    @property
    def start_color(self) -> Color:
        """Return the substring's start color."""
        return self.color_start

    @start_color.setter
    def start_color(self, color: Color) -> None:
        """Set the substring's start color."""
        self.color_start = color

    @property
    def end_color(self) -> Color:
        """Return the substring's end color."""
        return self.color_end

    @end_color.setter
    def end_color(self, color: Color) -> None:
        """Set the substring's end color."""
        self.color_end = color

    def __repr__(self) -> str:
        """Return the substring's representation."""
        strings = [
            f"GradientSubstring",
            f"<text={self.text}",
            f"start_index={self.start_index}",
            f"color_start={self.color_start}",
            f"color_end={self.color_end}",
            f"style={self.style}",
            f"spans={self.spans}>",
        ]
        return str(", ").join(strings)

    def __rich_repr__(self) -> Table:
        """Return the gradient's substring."""

        # Text (truncated if too long)
        if len(self.text) > console.width / 2 - 2:
            text = self.text[: console.width / 2 - 5] + "..."
        else:
            text = self.text
        text = Text(f'"{text}"', style="bold white")

        # Colors
        hyphen = "[bold dim #cccccc] - [/]"
        colors = []
        for color in [self.start_color, self.end_color]:
            # color = Color(color)
            colors.append(f"[bold {color.hex}]{str(color._original).capitalize()}[/]")
        color_string = Text.from_markup(hyphen.join(colors))

        # Repr Table
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
                str(self.color_start._original).capitalize(),
                style=f"bold {self.color_start.hex}",
            ),
        )
        table.add_row(
            "Color End",
            Text(
                str(self.color_end._original).capitalize(),
                style=f"bold {self.color_end.hex}",
            ),
        )
        table.add_row("Style", str(self.style))
        return table

    def calculate_spans_concurrently(self) -> None:
        """Calculate the gradient's spans concurrently."""
        with ThreadPoolExecutor(max_workers=3) as executor:
            result = executor.map(self._calculate_span, range(self._length))
        return list(result)  # type: ignore

    def _calculate_span(self, index: int) -> Span:
        """Calculate the gradient's span at the given index."""
        blend = index / self._length
        span_start: int = self.start_index + index
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
                last_span: Span = span
            else:
                if span.style == last_span.style:  # type: ignore
                    start = last_span.start  # type: ignore
                    last_span = Span(start, span.end, span.style)
                else:
                    simplified_spans.append(last_span)  # type: ignore
                    last_span = span
        simplified_spans.append(last_span)  # type: ignore
        return simplified_spans


def example() -> None:
    from lorem_text import lorem
    console = Console(theme=GradientTheme())
    width = console.width
    TEXT = lorem.paragraph()
    console.clear()
    console.line(2)
    # console.print(Text(TEXT), justify="center", width=int(width * 0.8))

    console.print(
        GradientSubstring(
            text=TEXT,
            start_index=0,
            color_start=Color("magenta"),
            color_end=Color("purple"),
            style="bold italic",
        ),
        justify="center",
    )


if __name__ == "__main__":
    example()
