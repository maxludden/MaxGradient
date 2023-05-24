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
from rich.style import Style, StyleType
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback

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
        spans: Optional[List[Span]] = None,
        concurrent: bool = True
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
        self.style = style

        # Initialize Text
        super().__init__(
            text=text,  #        #   self._text: List[str]
            style=style,  #      #   self.style: StyleType
            justify=justify,  #  #   self.justify: Optional[JustifyMethod]
            overflow=overflow,  ##   self.overflow: Optional[OverflowMethod]
            no_wrap=no_wrap,  #  #   self.no_wrap: Optional[bool]
            end=end,  #          #   self.end: str
            tab_size=tab_size,  ##   self.tab_size: Optional[int]
            spans=spans,  #      #   self._spans: Optional[List[Span]]
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
                color_list = ColorList(self.hues, self.invert)
                self._colors = color_list.color_list
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
            color_list = ColorList(self.hues, self.invert)
            self._colors = color_list.color_list

        # ensure that the gradient renderable is sufficiently long\
        # to display the gradient correctly.
        if self._length < self.hues:
            msg = (
                "The entered text is to short to display the number of colors entered."
            )
            raise NotEnoughColors(f"{msg} Please enter more text or fewer colors.")

        if concurrent:
            spans = self.concurrent_gradient_spans()
        else:
            spans = []
            for tuple in self.gradient.spans():
                start: int = tuple[0]
                substring: str = tuple[1]
                color1: Color = tuple[2]
                color2: Color = tuple[3]
                spans.append(self.gradient_spans(start, substring, color1, color2))
        self._spans = self.simplify_spans(spans)

    def substring_indexes(self) -> List[Tuple[int, int]]:
        """Determine the indexes of the text to split the into \
            substrings for multi-colored gradients."""
        num_of_substrings = len(self._colors) - 1
        substring_sizes = array_split(range(self._length), num_of_substrings)
        substring_indexes: List[Tuple[int, int]] = []
        for substring_size in substring_sizes:
            start = substring_size[0]
            end = substring_size[-1]
            substring_indexes.append((start, end))
        return substring_indexes

    def substrings(self) -> List[str]:
        """Split the text into substrings for multi-colored gradients."""
        substring_indexes = self.substring_indexes()
        substrings: List[str] = []
        for start, end in substring_indexes:
            substrings.append(self._text[start:end])
        return substrings

    def gradient_tuples(self) -> List[Tuple[str, Color, Color]]:
        """Generate a list of tuples that contain chunked strings and \
            their corresponding colors."""
        indexes = self.substring_indexes()
        substrings = self.substrings()
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

    @staticmethod
    def gradient_spans(gradient_tuple: Tuple[int, str, Color, Color]
    ) -> List[Span]:
        """Generate a list of spans for a substring."""
        start = gradient_tuple[1]
        substring = gradient_tuple[2]
        color1 = gradient_tuple[3]
        color2 = gradient_tuple[4]
        spans: List[Span] = []
        length = len(substring)

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
            span_style = generate_span_style(span_color)
            root_span_start = start + span_start
            current_span = Span(span_start, span_start + 1, span_style)
            spans.append(current_span)

        return spans

    def concurrent_gradient_spans(self) -> List[Span]:
        """Generate the spans for the gradient concurrently.

        Returns:
            List[Span]: The gradient spans.
        """
        workers = cpu_count() - 1
        _gradient_tuples = self.gradient_tuples()

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future = executor.submit(
                self.gradient_spans,
                _gradient_tuples
            )
            return future.result()

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