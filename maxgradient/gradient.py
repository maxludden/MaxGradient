"""Streamline Gradient class"""
# pylint: disable=W0621,C0103,W0622,E0401,E0611,C0412, w1203
import re
from functools import partial

# from itertools import groupby
from operator import itemgetter
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, Union

import numpy as np
from nptyping import NDArray, Shape
from rich.box import Box
from rich.cells import cell_len
from rich.console import Console, ConsoleOptions
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback

from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.log import Log
from maxgradient.theme import GradientTheme

JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]
GradientMethod = Literal["default", "list", "mono", "rainbow"]

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False
console = Console(theme=GradientTheme(), highlighter=ColorReprHighlighter())
install_rich_traceback(console=console, show_locals=True)
log = Log()


DEFAULT_JUSTIFY = "left"
DEFAULT_OVERFLOW = "crop"
VERBOSE = True


class Gradient(Text):
    """Text with gradient color / style.

    Args:
        text(`text): The text to print. Defaults to `""`.\n
        colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
            for the gradient. Defaults to None.\n
        rainbow(`bool`): Whether to print the gradient text in rainbow colors\
              across the spectrum. Defaults to False.\n
        invert(`bool`): Reverse the color gradient. Defaults to False.\n
        hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
        color_sample(`bool`): Replace text characters with `"█" `. Defaults\
              to False.\n
        style(`StyleType`) The style of the gradient text. Defaults to None.\n
        justify(`Optional[JustifyMethod]`): Justify method: "left", "center",\
              "full", "right". Defaults to None.\n
        overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
            "ellipsis". Defaults to None.\n
        end (str, optional): Character to end text with. Defaults to "\\\\n".\n
        no_wrap (bool, optional): Disable text wrapping, or None for default.\
            Defaults to None.\n
        tab_size (int): Number of spaces per tab, or `None` to use\
              `console.tab_size`. Defaults to 8.\n
        spans (List[Span], optional). A list of predefined style spans.\
            Defaults to None.\n

    """

    __slots__ = ["colors", "_color_sample", "_hues", "_style", "_color_sample"]

    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str] | str] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: Style = Style.null(),
        *,
        justify: Optional[str] = None,
        overflow: Optional[str] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to `""`.\n
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors\
                  across the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
            color_sample(`bool`): Replace text characters with `"█" `. Defaults\
                  to False.\n
            style(`StyleType`) The style of the gradient text. Defaults to None.\n
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center",\
                  "full", "right". Defaults to None.\n
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use\
                  `console.tab_size`. Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans.\
                Defaults to None.\n

        """
        # Parse text input
        if isinstance(text, Text):
            self._spans: List[Span] = text.spans
            text = strip_control_codes(text.plain)
        else:
            self._spans: List[Span] = spans or []
        # assert isinstance(text, str), f"Text must be a string or Text, not {type(text)}"
        self.text: str = text
        self._length: int = len(text)

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

        self.color_sample: bool = color_sample
        self.colors: List[Color] = []
        self.hues: int = hues or 3
        self.colors: List[Color] = self.get_colors(colors, rainbow, invert)
        self.hues = len(self.colors)

        gradient_substrings: Text = self.generate_gradient_substrings(True)
        self._spans = gradient_substrings.spans

    def __str__(self) -> str:
        return self.plain

    def __repr__(self) -> str:
        return f"<gradient {self!r}>"

    def __add__(self, other: Any) -> "Text":
        if isinstance(other, (str, Text)):
            result = self.copy()
            result.append(other)
            return result
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Text):
            return NotImplemented
        return self.plain == other.plain and self._spans == other._spans

    def __contains__(self, other: object) -> bool:
        if isinstance(other, str):
            return other in self.plain
        elif isinstance(other, Text):
            return other.plain in self.plain
        return False

    def __getitem__(self, slice: Union[int, slice]) -> "Text":
        def get_text_at(offset: int) -> "Text":
            _Span = Span
            text = Text(
                self.plain[offset],
                spans=[
                    _Span(0, 1, style)
                    for start, end, style in self._spans
                    if end > offset >= start
                ],
                end="",
            )
            return text

        if isinstance(slice, int):
            return get_text_at(slice)
        else:
            start, stop, step = slice.indices(len(self.plain))
            if step == 1:
                lines = self.divide([start, stop])
                return lines[1]
            else:
                # This would be a bit of work to implement efficiently
                # For now, its not required
                raise TypeError("slices with step!=1 are not supported")

    @property
    def cell_len(self) -> int:
        """Get the number of cells required to render this text."""
        return cell_len(self.plain)

    @property
    def text(self) -> str:
        """The text of the gradient."""
        log.debug(f"Getting gradient._text: {self._text}")
        return self._text

    @text.setter
    def text(self, text: Optional[str | Text]) -> None:
        """Set the text of the gradient."""
        log.debug(f"Setting gradient._text: {text}")
        if isinstance(text, Text):
            sanitized_text = strip_control_codes(text.plain)
            self._length = len(sanitized_text)
            self._text = sanitized_text
            self._spans: List[Span] = text.spans
        if isinstance(text, str):
            if text == "":
                raise ValueError("Text cannot be empty.")
            sanitized_text = strip_control_codes(text)
            self._length = len(sanitized_text)
            self._text = sanitized_text

    @property
    def hues(self) -> int:
        """The number of colors in the gradient."""
        log.debug(f"Retrieving gradient._hues: {self._hues}")
        return self._hues

    @hues.setter
    def hues(self, hues: int) -> None:
        """Set the number of colors in the gradient.

        Args:
            hues (int): The number of colors in the gradient. Defaults to `3`.
        """
        log.debug(f"Setting gradient._hues: {hues}")
        if hues < 2:
            raise ValueError("Gradient must have at least two colors.")
        self._hues = hues

    @property
    def color_sample(self) -> bool:
        """Whether the gradient is a color sample."""
        log.debug(f"Retrieving gradient._color_sample: {self._color_sample}")
        return self._color_sample

    @color_sample.setter
    def color_sample(self, color_sample: bool) -> None:
        """Set whether the gradient is a color sample."""
        log.debug(f"Setting gradient._color_sample: {color_sample}")
        if color_sample:
            self.text = "█" * self._length
        self._color_sample = color_sample

    @property
    def style(self) -> Style:
        """The style of the gradient."""
        log.debug(f"Retrieving gradient._style: {self._style}")
        return self._style

    @style.setter
    def style(self, style: Style) -> None:
        """Set the style of the gradient.

        Args:
            style(`StyleType`): The style to set the gradient to.
        """
        log.debug(f"Setting gradient._style: {style}")
        if isinstance(style, Style):
            self._style = Style.copy(style).without_color
        if style is None:
            self._style = Style.null()
        elif isinstance(style, str):
            if style == "" or style == "null":
                self._style = Style.null()
            if style == "none" or style == "None":
                self._style = Style.null()
            self._style = Style.parse(style)

    def get_colors(
        self,
        input_colors: Optional[str | List[Color | Tuple | str]],
        rainbow: bool,
        invert: bool,
    ) -> List[Color]:
        """Get the colors for the gradient.

        Args:
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            verbose(`bool`): Whether to print verbose output. Defaults to True.\n

        Returns:
            List[Color]: A list of colors for the gradient.
        """
        if rainbow:
            self.hues = 10
            color_list = ColorList(self.hues, invert).color_list
            assert len(color_list) == self.hues, f"Color list length: {len(color_list)}"
            colors = color_list
            if self.validate_colors(colors):
                return colors
        if isinstance(input_colors, str):
            return self.mono(input_colors)
        if input_colors is not None:
            colors: List[Color] = []
            for color in input_colors:
                try:
                    color = Color(color)
                    colors.append(color)
                except ColorParseError as error:
                    raise ColorParseError(f"Can't parse color: {color}") from error
            if self.validate_colors(colors):
                return colors
        color_list = ColorList(self.hues, invert).color_list
        colors = color_list[: self.hues]
        if self.validate_colors(colors):
            return colors

    def mono(self, color: str | Color) -> List[Color]:
        """Create a list of monochromatic hues from a color.

        Args:
            color (str|Color): The color to generate monochromatic hues from.
        """
        log.debug(f"Called Gradient.mono({color})")
        if isinstance(color, str):
            try:
                color = Color(color)
            except ColorParseError as cpe:
                raise ColorParseError(f"Could not parse color: {color}") from cpe
        if not isinstance(color, Color):
            raise TypeError(f"Color must be a string or Color, not {type(color)}")
        else:
            return [
                Color(color.darken(0.6)),
                Color(color.darken(0.3)),
                color,
                Color(color.lighten(0.3)),
                Color(color.lighten(0.6)),
            ]

    def validate_colors(self, colors: Optional[List[Color]]) -> bool:
        """Validate self.colors to ensure that it is a list of colors."""
        valid: bool = True
        if colors is None:
            return False
        for color in colors:
            if not isinstance(color, Color):
                return False
        if valid:
            return True
        return False

    def generate_gradient_substrings(self, verbose: bool = False) -> List[Span]:
        """Generate gradient spans.

        Returns:
            List[Span]: The gradient spans.
        """
        text = self.generate_text()
        gradient_string = Text()
        indexes: List[List[int]] = self.generate_indexes()
        substrings: List[str] = self.generate_substrings(indexes, text)

        if verbose:
            substrings_table = Table(
                "Index", "Substring", "Length", expand=False, highlight=True
            )

        for index, substring in enumerate(substrings):
            gradient_length = len(substring)
            substring = Text(substring)
            if verbose:
                substrings_table.add_row(  # type: ignore
                    str(index),
                    substring,
                    str(gradient_length),
                )

            if index < self.hues - 1:
                color1 = self.colors[index]
                r1, g1, b1 = color1.rgb_tuple
                color2 = self.colors[index + 1]
                r2, g2, b2 = color2.rgb_tuple
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1

            for subindex in range(gradient_length):
                blend = subindex / gradient_length
                red = int(r1 + (blend * dr))  # type: ignore
                green = int(g1 + (blend * dg))  # type: ignore
                blue = int(b1 + (blend * db))  # type: ignore
                color = f"#{red:02X}{green:02X}{blue:02X}"
                substring.stylize(color, subindex, subindex + 1)

            if verbose:
                gradient_string = Text.assemble(
                    gradient_string,
                    substring,
                    style=self.style,
                    justify=self.justify,
                    overflow=self.overflow,
                    no_wrap=self.no_wrap,
                    end=self.end,
                    tab_size=self.tab_size,
                )
                substrings_table.add_row(  # type: ignore
                    f"{index}", substring, f"{len(gradient_string)}"
                )
        return gradient_string

    def clean_spans(self, gradient_string: Text) -> List[Span]:
        """Clean up redundant spans"""
        spans: List[Span] = []
        for span in gradient_string.spans:
            start = span.start
            end = span.end
            style = span.style
            if start + 1 == end:
                spans.append(Span(start, end, style))
            if style == Style():
                continue
            if style == "":
                continue
            spans.append(Span(start, end, style))
        return spans

    def generate_text(self) -> str:
        """Get the gradient text.

        Returns:
            str: The gradient text.
        """
        if isinstance(self._text, str):
            log.debug(f"Gradient._text is a string: {self._text}")
            return self._text
        if self._text:
            return "".join(self._text)
        else:
            raise TypeError("Gradient hasn't yet set a text value.")

    def generate_indexes(self, verbose: bool = False) -> List[List[int]]:
        """Generate the indexes for the gradient substring.

        Returns:
            List[List[int]]: The indexes for the gradient substring.
        """
        result: NDArray[Shape["*, *"], int] = np.array_split(
            np.arange(self._length), self.hues - 1
        )
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        for count, index in enumerate(indexes):
            if verbose:
                log.success(
                    f"[b white]Index {count}:[/]{', '.join([str(i) for i in index])}"
                )
            else:
                log.info(f"Index {count}: {', '.join([str(i) for i in index])}")
        return indexes

    def generate_substrings(self, indexes: List[List[int]], text: str) -> List[str]:
        """Generate a list of substrings for the gradient.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.
        """
        substrings: List[str] = []
        for index in indexes:
            substring = self.generate_substring(index, text)
            substrings.append(substring)
        return substrings

    def generate_substring(self, index: List[int], text: str) -> str:
        """Generate a string to make a GradientSubstring.

        Args:
            index (List[int]): The index of the substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.

        Returns:
            str: The substring.
        """
        substring_list: List[str] = []
        for num in index:
            substring_list.append(text[num])
        substring = "".join(substring_list)
        return substring

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Segment]:
        tab_size: int = console.tab_size or self.tab_size or 8
        justify = self.justify or options.justify or DEFAULT_JUSTIFY

        overflow = self.overflow or options.overflow or DEFAULT_OVERFLOW

        lines = self.wrap(
            console,
            options.max_width,
            justify=justify,
            overflow=overflow,
            tab_size=tab_size or 8,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap, False),
        )
        all_lines = Text("\n").join(lines)
        yield from all_lines.render(console, end=self.end)

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Measurement:
        text = self.plain
        lines = text.splitlines()
        max_text_width = max(cell_len(line) for line in lines) if lines else 0
        words = text.split()
        min_text_width = (
            max(cell_len(word) for word in words) if words else max_text_width
        )
        return Measurement(min_text_width, max_text_width)

    def render(self, console: "Console", end: str = "") -> Iterable["Segment"]:
        """Render the text as Segments.

        Args:
            console (Console): Console instance.
            end (Optional[str], optional): Optional end character.

        Returns:
            Iterable[Segment]: Result of render that may be written to the console.
        """
        _Segment = Segment
        text = str.strip(self.plain)
        if not self._spans:
            yield Segment(text)
            if end:
                yield _Segment(end)
            return
        get_style = partial(console.get_style, default=Style.null())

        enumerated_spans = list(enumerate(self._spans, 1))
        style_map = {index: get_style(span.style) for index, span in enumerated_spans}
        style_map[0] = get_style(self.style)
        log.debug(f"style_map: {style_map}")

        spans = [
            (0, False, 0),
            *((span.start, False, index) for index, span in enumerated_spans),
            *((span.end, True, index) for index, span in enumerated_spans),
            (len(text), True, 0),
        ]
        spans.sort(key=itemgetter(0, 1))

        stack: List[int] = []
        stack_append = stack.append
        stack_pop = stack.remove

        style_cache: Dict[Tuple[Style, ...], Style] = {}
        style_cache_get = style_cache.get
        combine = Style.combine

        def get_current_style() -> Style:
            """Construct current style from stack."""
            styles = tuple(style_map[_style_id] for _style_id in sorted(stack))
            cached_style = style_cache_get(styles)
            if cached_style is not None:
                return cached_style
            current_style = combine(styles)
            style_cache[styles] = current_style
            return current_style

        for (offset, leaving, style_id), (next_offset, _, _) in zip(spans, spans[1:]):
            if leaving:
                stack_pop(style_id)
            else:
                stack_append(style_id)
            if next_offset > offset:
                yield _Segment(text[offset:next_offset], get_current_style())
        if end:
            yield _Segment(end)


    def as_text(self) -> Text:
        """Return the gradient as a Text object."""
        return Text(
            self.text,
            style=self.style,
            justify=self.justify,
            overflow=self.overflow,
            no_wrap=self.no_wrap,
            end=self.end,
            tab_size=self.tab_size,
            spans=self.spans,
        )


# register_repr(Gradient)(normal_repr)


def strip_control_codes(text: str) -> str:
    """Remove control codes from a string."""
    return "".join(char for char in text if ord(char) >= 32)


# def cell_len(text: str) -> int:Y


def pick_bool(value: Optional[bool], default: bool, fallback: bool) -> bool:
    """Pick a boolean value from a set of options."""
    if value is not None:
        return value
    if default is not None:
        return default
    return fallback


if __name__ == "__main__":  # pragma: no cover
    from lorem_text import lorem
    from rich.panel import Panel

    console.line(2)
    gradient = Panel(
        Gradient(
            lorem.paragraph(),
            colors=["red", "orange", "yellow", "green", "cyan"],
            justify="left",
            style="bold"
        ),
        title=Gradient("Gradient Example"),
        expand=True,
        width=70,
        padding=(1, 4),
        border_style="bold",
    )
    # inspect(gradient)
    console.print(gradient, justify="center")
    console.line(2)
