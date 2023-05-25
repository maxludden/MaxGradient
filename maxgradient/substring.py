
from typing import List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from time import perf_counter
from functools import wraps
from random import choice
from io import StringIO
from pathlib import Path

# import numpy as np
from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.style import Style, StyleType
from rich.text import Span, Text
from rich.traceback import install
from snoop import snoop

from maxgradient.color import Color
from maxgradient.theme import GradientTheme

console = Console(theme=GradientTheme())
install(console=console)
register_repr(Text)(normal_repr)
register_repr(Span)(normal_repr)
register_repr(Style)(normal_repr)
register_repr(Color)(normal_repr)

class BaseGradient(Text):

    def __init__(
        self,
        text: str = "",
        index_start: int = None,
        color_start: Color = None,
        color_end: Color = None,
        concurrent: bool = False,
        style: StyleType = None,
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None) -> None:
        """Initialize the GradientSpan class."""
        super().__init__(
            text=text,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            end=end,
            tab_size=tab_size,
            spans=spans
        )
        sanitized_text = strip_control_codes(text)
        self._length: int = len(sanitized_text)

        assert index_start is not None, "Index_start must be provided."
        assert isinstance(index_start, int), "Index_start must be an integer."
        self.index_start: int = index_start

        assert isinstance(color_start, Color), "Color_start must be a Color object."
        self.color_start: Color = color_start

        assert isinstance(color_end, Color), "Color_end must be a Color object."
        self.color_end: Color = color_end

        if style:
            self.style = self.parse_style(style)
        end_style = Style.parse(f"{self.style} {self.color_end.hex}")
        spans: List[Span] = [Span(0, self._length, end_style)]

        if not concurrent:
            r1, g1, b1 = self.color_start.rgb_tuple
            r2, g2, b2 = self.color_end.rgb_tuple
            dr = r2 - r1
            dg = g2 - g1
            db = b2 - b1


            for index in range(self._length):
                blend = index / self._length
                span_start = index_start + index
                span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
                span_style = f"{self.style} {span_color}".strip()
                current_span = Span(span_start, span_start + 1, span_style)
                spans.append(current_span)

        else:
            spans = self.calculate_spans_concurrent()

        self.spans = self.simplify_spans(spans)

    def calculate_spans_concurrent(self) -> None:
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            result = executor.map(
                self._calculate_span, range(self._length)
            )
        return list(result)

    def _calculate_span(self, index: int) -> Span:
        blend = index / self._length
        span_start = self.index_start + index
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
        else:
            try:
                style = Style.parse(style).without_color
                style = str(style)
            except:
                raise ValueError("Style must be a Style object or a string that can be parsed into a Style object.")
        return style

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

CWD = Path.cwd()
timer = CWD / 'timer.txt'
buffer = StringIO()
timer_console = Console(file=buffer, force_terminal=True, color_system='truecolor')


def time(num_times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            durations = []
            for _ in range(num_times):
                start_time = perf_counter()
                result = func(*args, **kwargs)
                end_time = perf_counter()
                duration = end_time - start_time
                durations.append(duration)

            average_duration = sum(durations) / len(durations)
            print(f"Average duration: {average_duration:.6f} seconds")

            return result

        return wrapper

    return decorator

@time(20)
def gradient_test(concurrent: bool, text: str):
    console=Console(theme=GradientTheme())
    color_start = Color(choice(colors))
    color_end = Color(choice(colors))
    gradient = BaseGradient(
        text=text,
        index_start=0,
        color_start=color_start,
        color_end=color_end,
        concurrent=False
    )
    console.print(gradient)



def without(text:str):
    console.rule("Loop")
    for x in range(10):
        gradient_test(concurrent=False, text=text)


def concurrent(text:str):
    console.rule("Concurrent")
    for x in range(10):
        gradient_test(concurrent=True, text=text)


if __name__ == "__main__":
    from timeit import timeit
    text = lorem.paragraphs(5)
    colors = Color.COLORS
    without(text)
    concurrent(text)