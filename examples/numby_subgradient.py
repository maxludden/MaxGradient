
from typing import List, Optional, Tuple

import numpy as np
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

        r1, g1, b1 = self.color_start.rgb
        r2, g2, b2 = self.color_end.rgb
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1
        indexes = np.arange(self._length)
        blends = indexes / self._length
        colors = np.array([
            r1 + dr * blends,
            g1 + dg * blends,
            b1 + db * blends
        ]).T.astype(int)
        span_starts = np.full((self._length,), index_start)
        span_ends = span_starts + 1
        span_styles = np.char.strip(np.char.add(f"{self.style} ", np.char.mod("%02X%02X%02X", tuple(colors.T))))
        self.spans = self.simplify_spans(
            [Span(start, end, style) for start, end, style in
             zip(span_starts, span_ends, span_styles)]
        )
class BaseGradient(Text):
    def __init__(
        self,
        text: str = "",
        index_start: int = None,
        color_start: Color = None,
        color_end: Color = None,
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

        r1, g1, b1 = self.color_start.rgb_tuple
        r2, g2, b2 = self.color_end.rgb_tuple
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1
        indexes = np.arange(self._length)
        blends = indexes / self._length
        colors = np.array([
            r1 + dr * blends,
            g1 + dg * blends,
            b1 + db * blends
        ]).T.astype(int)
        span_starts = np.full((self._length,), index_start)
        span_ends = span_starts + 1
        span_styles = np.char.strip(np.char.add(f"{self.style} ", np.char.mod("%02X%02X%02X", tuple(colors.T))))
        self.spans = self.simplify_spans(
            [Span(start, end, style) for start, end, style in
             zip(span_starts, span_ends, span_styles)]
        )

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

    @staticmethod
    def simplify_spans(spans: List[Span]) -> List[Span]:
        """Combine continuous spans with the same style."""
        simplified_spans: List[Span] = []
        for span in spans:
            if simplified_spans and simplified_spans[-1].end == span.start and simplified_spans[-1].style == span.style:
                simplified_spans[-1].end = span.end
            else:
                simplified_spans.append(span)
        return simplified_spans

text = lorem.paragraph()
gradient = BaseGradient(text=text, index_start=0, color_start=Color("red"), color_end=Color("blue"), style="bold")
console.print(gradient)