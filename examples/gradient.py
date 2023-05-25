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


class fakeGradient:
    def __init__(
        self,
        text: str = "",
        colors: List[Optional[Color]] = [],
        concurrent: bool = True) -> None:

        substring_indexes: List[Tuple[int, int]] = self.substring_indexes()
        substring_start_indexes: List[int] = [i[0] for i in substring_indexes]
        substrings: List[str] = self.substrings(substring_indexes)
        color_tuples: List[Tuple[Color, Color]] = self.color_tuples()
        substring_start_colors: List[Color] = [
            color_tuple[0] for color_tuple in color_tuples
        ]
        substring_end_colors: List[Color] = [
            color_tuple[1] for color_tuple in color_tuples
        ]

        if concurrent:
            spans = self.concurrent_gradient_spans(
                start_indexes=substring_start_indexes,
                substrings=substrings,
                start_colors=substring_start_colors,
                end_colors=substring_end_colors,
            )
        else:
            spans = []
            for index in range(len(substrings)):
                spans.append(
                    self.gradient_spans(
                        substring_start_indexes[index],
                        substrings[index],
                        substring_start_colors[index],
                        substring_end_colors[index]
                    )
                )
        self._spans = self.simplify_spans(spans)


    # @snoop
    # def substring_indexes(self) -> List[Tuple[int, int]]:
    #     """Determine the indexes of the text to split the into \
    #         substrings for multi-colored gradients."""
    #     num_of_substrings = len(self._colors) - 1
    #     substring_sizes = array_split(range(self._length), num_of_substrings)
    #     substring_indexes: List[Tuple[int, int]] = []
    #     for substring_size in substring_sizes:
    #         start = substring_size[0]
    #         end = substring_size[-1]
    #         substring_indexes.append((start, end))
    #     return substring_indexes

    @snoop(watch=("substring_indexes", "substrings"))
    def substrings(self, indexes: List[Tuple[int,int]]) -> List[str]:
        """Split the text into substrings for multi-colored gradients."""
        text = self.plain
        substrings: List[str] = []
        for start, end in indexes:
            substrings.append(text[start:end])
        return substrings

    def color_tuples(self) -> List[Tuple[Color, Color]]:
        """Return the start and end color for each substring of the gradient.

        Raises:
            IndexError: If there is not enough colors to display the gradient.

        Returns:
            List[Tuple[Color, Color]]: A list of tuples containing the start and end colors for each substring.
        """
        num_of_gradients = len(self._colors) - 1
        color_tuples: List[Tuple[Color, Color]] = []
        for index in range(num_of_gradients):
            color1 = self._colors[index]
            color2 = self._colors[index + 1]
            color_tuples.append((color1, color2))
        return color_tuples

    @snoop
    def gradient_tuples(self) -> List[Tuple[str, Color, Color]]:
        """Generate a list of tuples that contain chunked strings and \
            their corresponding colors."""
        indexes = self.substring_indexes()
        substrings = self.substrings(indexes)
        gradient_tuples: List[Tuple[int, str, Color, Color]] = []

        for (
            index,
            substring,
        ) in enumerate(substrings):
            start = indexes[index][0]
            color = self._colors[index]
            next_color = self._colors[index + 1]
            gradient_tuples.append((start, substring, color, next_color))
        return gradient_tuples

    def generate_span_style(self, color: Color) -> Style:
        """Generate a style with the specified color."""
        if self.style is None or self.style == "_null":
            self.style = Style(color=color)
            return self.style
        if not isinstance(color, Color):
            color = Color(color)
        if isinstance(self.style, str):
            self.style = Style.parse(self.style)
        elif isinstance(self.style, Style):
            style_def = str(self.style)
            self.style = Style.parse(f"{style_def} {str(color)}")
            return self.style
        else:
            raise TypeError(
                f"Unable to combine style (`{self.style}`) and color (`{color})`)"
            )

    @snoop
    def gradient_spans(self, start: int, substring: str, color1: Color, color2: Color
    ) -> List[Span]:
        """Generate a list of spans for a substring."""
        spans: List[Span] = []
        length = len(substring)

        r1, g1, b1 = color1.rgb
        r2, g2, b2 = color2.rgb
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1

        span_start = 0
        for index, char in enumerate(substring):
            blend = index / length
            span_start = start + span_start + index
            span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
            span_style = self.generate_span_style(span_color)
            current_span = Span(span_start, span_start + 1, span_style)
            spans.append(current_span)

        return spans

    @snoop
    def concurrent_gradient_spans(
        self,
        start_indexes: List[int],
        substrings: List[str],
        start_colors: List[Color],
        end_colors: List[Color]) -> List[Span]:
        """Generate the spans for the gradient concurrently.

        Returns:
            List[Span]: The gradient spans.
        """
        workers = cpu_count() - 1
        gradient_tuples = self.gradient_tuples()

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future = executor.submit(
                self.gradient_spans,
                start_indexes,
                substrings,
                start_colors,
                end_colors,
            )
            return pp(future.result())

    def simplify_spans(self) -> List[Span]:
        """Simplify the spans by combining spans with the same style."""
        simplified_spans: List[Span] = []
        for span in self._spans:
            if simplified_spans:
                last_span = simplified_spans[-1]
                if span.style == last_span.style:
                    last_span.end += 1
                    continue
            simplified_spans.append(span)
        return simplified_spans
