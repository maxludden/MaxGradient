"""Streamline Gradient class"""
import re
from functools import partial
from operator import itemgetter
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, Union

import numpy as np

# from snoop import snoop
from cheap_repr import normal_repr, register_repr
from rich.cells import cell_len
from rich.console import Console, ConsoleOptions, JustifyMethod, OverflowMethod
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text

from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.highlighter import ColorReprHighlighter

# from maxgradient.log import log
from maxgradient.theme import GradientTheme

GradientMethod = Literal["default", "list", "mono", "rainbow"]
DEFAULT_JUSTIFY: JustifyMethod = "default"
DEFAULT_OVERFLOW: OverflowMethod = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False
console = Console(theme=GradientTheme(), highlighter=ColorReprHighlighter())
DEFAULT_JUSTIFY = "left"
DEFAULT_OVERFLOW = "crop"
VERBOSE = True


class Gradient(Text):
    """Text with gradient color / style.

    Args:
        text (Text): The text to print. Defaults to `""`.\n
        colors (List[Optional[Color|Tuple|str|int]]): A list of colors to use \
            for the gradient. Defaults to None.\n
        rainbow (bool): Whether to print the gradient text in rainbow colors\
                across the spectrum. Defaults to False.\n
        invert (bool): Reverse the color gradient. Defaults to False.\n
        hues (int): The number of colors in the gradient. Defaults to `3`.\n
        style (StyleType) The style of the gradient text. Defaults to None.\n
        justify (Optional[JustifyMethod]): Justify method: "left", "center",\
                "full", "right". Defaults to None.\n
        overflow (Optional[OverflowMethod]):  Overflow method: "crop", "fold", \
            "ellipsis". Defaults to None.\n
        end (str, optional): Character to end text with. Defaults to "\\\\n".\n
        no_wrap (bool, optional): Disable text wrapping, or None for default.\
            Defaults to None.\n
        tab_size (int): Number of spaces per tab, or `None` to use\
                `console.tab_size`. Defaults to 8.\n
        spans (List[Span], optional). A list of predefined style spans.\
            Defaults to None.\n

    """

    __slots__ = [
        "_colors",
        "_text",
        "_length",
        "length",
        "_hues",
        "_style",
        "_spans",
        "_rainbow",
    ]

    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str] | str] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        style: StyleType = Style.null(),
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 4,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Text styled with gradient color.

        Args:
            text (text): The text to print. Defaults to `""`.\n
            colors (List[Optional[Color|Tuple|str|int]]): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow (bool): Whether to print the gradient text in rainbow colors\
                  across the spectrum. Defaults to False.\n
            invert (bool): Reverse the color gradient. Defaults to False.\n
            hues (int): The number of colors in the gradient. Defaults to `3`.\n
            style (StyleType) The style of the gradient text. Defaults to None.\n
            justify (Optional[JustifyMethod]): Justify method: "left", "center",\
                  "full", "right". Defaults to None.\n
            overflow (Optional[OverflowMethod]):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use\
                  `console.tab_size`. Defaults to 4.\n
            spans (List[Span], optional). A list of predefined style spans.\
                Defaults to None.\n

        """
        # Parse text input
        if isinstance(text, Text):
            self._spans: List[Span] = text.spans
            text = strip_control_codes(text.plain)
        else:
            self._spans = spans or []
            text = strip_control_codes(str(text))
        # self._text: str = text
        # self._length: int = len(text)

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
        # self.colors: List[Color] = colors or []
        self.rainbow = rainbow
        self._hues: int = hues or 3
        self.colors = colors or []  # type: ignore
        self._hues = len(self.colors)
        gradient_substrings: Text = self.generate_gradient_substrings(True)
        self._spans = gradient_substrings.spans

    def __str__(self) -> str:
        return self.plain

    def __repr__(self) -> str:
        colors = ", ".join([str(color) for color in self.colors])
        return f"Gradient<colors=`{colors}`, text=`{self.text}`>"

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

        return self._text

    @text.setter
    def text(self, text: Optional[str | Text]) -> None:
        """Set the text of the gradient."""

        if isinstance(text, Text):
            sanitized_text = strip_control_codes(text.plain)
            length = len(sanitized_text)
            self.length: int = length
            self._text = sanitized_text
            self._spans = text.spans
        elif isinstance(text, str):
            if text == "":
                raise ValueError("Text cannot be empty.")
            sanitized_text = strip_control_codes(text)
            self._length = len(sanitized_text)
            self._text = sanitized_text
        elif text is None:
            raise ValueError("Text cannot be None.")
        else:
            raise TypeError(f"Text must be a string or Text, not {type(text)}")

    @property
    def hues(self) -> int:
        """The number of colors in the gradient."""
        if self._hues is None:
            return 3
        return self._hues

    @hues.setter
    def hues(self, hues: int) -> None:
        """Set the number of colors in the gradient.

        Args:
            hues (int): The number of colors in the gradient. Defaults to `3`.
        """

        if hues < 2:
            raise ValueError("Gradient must have at least two colors.")
        self._hues = hues

    @property
    def style(self) -> Style:
        """The style of the gradient."""

        return self._style

    @style.setter
    def style(self, style: Style) -> None:
        """Set the style of the gradient.

        Args:
            style(`StyleType`): The style to set the gradient to.
        """

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

    @property
    def rainbow(self) -> bool:
        """Whether to print the gradient text in rainbow colors across the spectrum."""
        if self._rainbow is None:
            return False
        else:
            return self._rainbow

    @rainbow.setter
    def rainbow(self, value: bool) -> None:
        """Set whether to print the gradient text in rainbow colors across the spectrum.

        Args:
            value (bool): Whether to print the gradient text in rainbow colors \
                across the spectrum.
        """

        if value is None:
            self._rainbow = False
        elif isinstance(value, bool):
            self._rainbow = value
        elif isinstance(value, str):
            if str(value).lower() == "true":
                self._rainbow = True
            elif str(value).lower() == "false":
                self._rainbow = False
            else:
                raise ValueError(f"Rainbow must be a bool, not {value}")
        else:
            raise TypeError(f"Rainbow must be a bool, not {type(value)}")

    @property
    def colors(self) -> List[Color]:
        """The colors of the gradient."""
        return self._colors

    @colors.setter
    def colors(self, colors: Optional[List[Color | Tuple | str]]) -> None:
        """Set the colors of the gradient.

        Args:
            colors (List[Color|Tuple|str|int]): The colors to set the gradient to.
        """

        if colors is None or colors == []:
            if self._hues is None:
                self._hues = 3
            if self.rainbow:
                self._hues = 10
            _colors: List[Color] = ColorList(self._hues, False).color_list
            if self.validate_colors(_colors):
                self._colors: List[Color] = _colors
            else:
                raise ValueError("No input colors. Unable to generate colors.")
        elif isinstance(colors, list):
            _colors = []
            for color in colors:
                if isinstance(color, (str, tuple, Color)):
                    try:
                        color = Color(color)
                        _colors.append(color)
                    except ColorParseError as cpe:
                        raise ColorParseError(
                            f"Could not parse color: {color}"
                        ) from cpe
                else:
                    raise TypeError(
                        f"Color must be a string, tuple, or Color, not {type(color)}"
                    )
            if self.validate_colors(_colors):
                self._colors = _colors
            else:
                raise ValueError("Colors were a list of invalid colors.")
        else:
            raise TypeError(f"Colors must be a list, not {type(colors)}")

    def get_colors(
        self,
        input_colors: Optional[str | List[Color | Tuple | str]],
        rainbow: bool,
        invert: bool,
    ) -> List[Color]:
        """Get the colors for the gradient.

        Args:
            colors (List[Optional[Color|Tuple|str|int]]): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow (bool): Whether to print the gradient text in rainbow colors \
                across the spectrum. Defaults to False.\n
            invert (bool): Reverse the color gradient. Defaults to False.\n
            verbose (bool): Whether to print verbose output. Defaults to True.\n

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
            else:
                raise ValueError("Rainbow Colors are invalid.")
        if isinstance(input_colors, str):
            colors = self.mono(input_colors)
            if self.validate_colors(colors):
                return colors
            else:
                raise ValueError("Colors are invalid. Input colors is a string.")
        if input_colors is not None:
            colors = []
            for color in input_colors:
                try:
                    color = Color(color)
                    colors.append(color)
                except ColorParseError as error:
                    raise ColorParseError(f"Can't parse color: {color}") from error
            if self.validate_colors(colors):
                return colors
            else:
                raise ValueError("Colors are invalid. Input colors are not None.")
        elif input_colors is []:
            color_list = ColorList(self.hues or 3, invert).color_list
            colors = color_list[: self.hues]
            if self.validate_colors(colors):
                return colors
            else:
                raise ValueError("Colors are invalid. Input colors: []")
        else:
            color_list = ColorList(self.hues, invert).color_list
            colors = color_list[: self.hues]
            if self.validate_colors(colors):
                return colors
            else:
                raise ValueError("Colors are invalid.")

    def mono(self, color: str | Color) -> List[Color]:
        """Create a list of monochromatic hues from a color.

        Args:
            color (str|Color): The color to generate monochromatic hues from.
        """

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
        elif colors == []:
            return False
        for color in colors:
            if not isinstance(color, Color):
                return False
        if valid:
            return True
        return False

    def generate_gradient_substrings(self, verbose: bool = False) -> Text:
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
            subtext = Text(substring)
            if verbose:
                substrings_table.add_row(  # type: ignore
                    str(index),
                    subtext,
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
                subtext.stylize(color, subindex, subindex + 1)

            if verbose:
                gradient_string = Text.assemble(
                    gradient_string,
                    subtext,
                    style=self.style,
                    justify=self.justify,
                    overflow=self.overflow,
                    no_wrap=self.no_wrap,
                    end=self.end,
                    tab_size=self.tab_size or 4,
                )
                substrings_table.add_row(  # type: ignore
                    f"{index}", subtext, f"{len(gradient_string)}"
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
        if self.hues < 2:
            self.hues = 3
        result = np.array_split(np.arange(self._length), self.hues - 1)  # noqa: F722
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        for count, index in enumerate(indexes):
            if verbose:
                console.log(
                    f"[b white]Index {count}:[/]{', '.join([str(i) for i in index])}"
                )
        return indexes

    def generate_substrings(self, indexes: List[List[int]], text: str) -> List[str]:
        """Generate a list of substrings for the gradient.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output.
                Defaults to VERBOSE.
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
            verbose (bool, optional): Whether to print verbose output.
                Defaults to VERBOSE.

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
            no_wrap=pick_bool(self.no_wrap, options.no_wrap, False),  # type: ignore
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


register_repr(Gradient)(normal_repr)


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
    from rich.panel import Panel

    PLACEHOLDER: str = """Excepteur incididunt ex laborum amet non aute ullamco \
nostrud non dolore aute do fugiat esse amet. Laborum nulla non mollit et ad. \
Adipisicing labore ut sunt sit id ea cillum labore id. Ea reprehenderit laborum \
sit laboris et Lorem proident elit cillum nisi sint ea excepteur Lorem et. Qui \
sint nulla labore aliqua do Lorem incididunt occaecat exercitation minim culpa \
in. Duis duis ad velit dolore ullamco labore eu enim velit quis eu mollit amet \
elit. Irure adipisicing pariatur pariatur eu tempor sunt irure exercitation duis 
do magna duis est. Exercitation dolore ipsum tempor cillum minim irure ipsum \
nisi quis pariatur excepteur elit exercitation nostrud do. Ex qui aliquip anim \
minim ullamco nisi. Mollit fugiat enim cupidatat ad fugiat occaecat officia \
fugiat Lorem nisi occaecat amet. Eu sit adipisicing sint ad nisi ut et sit do \
aliquip anim et laborum officia aute. Non cillum et dolor ipsum elit consequat \
id anim ex aute ex. In consequat occaecat pariatur incididunt sit. Aliqua \
excepteur fugiat irure proident enim. Nulla duis elit ut labore eiusmod \
proident qui tempor Lorem occaecat ullamco."""
    console.line(2)
    gradient = Panel(
        Gradient(
            PLACEHOLDER,
            colors=["red", "orange", "yellow", "green", "cyan"],
            justify="left",
            style="bold",
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
    console.line(2)
