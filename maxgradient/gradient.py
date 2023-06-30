"""Defines the Gradient class which is used to print text with a gradient. \
    It inherits from the Rich Text class."""
# pylint: disable=W0611,C0103, E0401, C0301
import re
from typing import List, Optional, Tuple

import numpy as np
from lorem_text import lorem
from numpy import ndarray
from rich.console import Console, JustifyMethod, OverflowMethod
from rich.control import strip_control_codes
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.text import Span, Text

from maxgradient.gradient_color import GradientColor as GC
from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.log import Log, LogConsole
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False
console = LogConsole()
log = Log(console=console)


class Gradient(Text):
    """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to `""`.\n
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
            color_sample(`bool`): Replace text with characters with `"█" `. Defaults to False.\n
            style(`StyleType`) The style of the gradient text. Defaults to None.\n
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center", "full", \
                "right". Defaults to None.\n
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.\n

    """

    __slots__ = ["colors", "_color_sample", "_hues", "_style"]

    # @snoop(watch=("gradient_spans", "substrings"))
    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]|str] = None,
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
    ) -> None:
        """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to `""`.\n
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
            color_sample(`bool`): Replace text with characters with `"█" `. Defaults to False.\n
            style(`StyleType`) The style of the gradient text. Defaults to None.\n
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center", "full", \
                "right". Defaults to None.\n
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.\n

    """

        if isinstance(text, Text):
            self._spans: List[Span] = text.spans
            text = strip_control_codes(text.plain)
        else:
            self._spans = spans
        assert isinstance(text, str), f"Text must be a string or Text, not {type(text)}"
        self._text: str = text
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

        gradient_substring: Text = self.generate_substrings()
        console.line(2)
        self._spans = gradient_substring.spans

    # @snoop(watch_explode=["colors", "self.colors"])
    def get_colors(
        self, colors: Optional[str|List[Color | Tuple | str]], rainbow: bool, invert: bool
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
        if isinstance(colors, str):
            return self.mono(colors)
        else:
            if rainbow:
                self.hues = 10
                color_list = ColorList(self.hues, invert).color_list
                colors_ = color_list
                if self.validate_colors(colors_):
                    return colors_

            else:
                if colors is not None:
                    colors_: List[Color] = []
                    for color in colors:
                        try:
                            color = Color(color)
                            colors_.append(color)
                        except ColorParseError as error:
                            raise ColorParseError(f"Can't parse color: {color}") from error
                    if self.validate_colors(colors_):
                        return colors_
                else:
                    color_list = ColorList(self.hues, invert).color_list
                    colors_ = color_list[: self.hues]
                    if self.validate_colors(colors_):
                        return colors_

    def mono(self, color: str|Color) -> List[Color]:
        """Create a list of monochromatic hues from a color.

        Args:
            color (str|Color): The color to generate monochromatic hues from.
        """
        log.debug(f"Called Gradient.mono({color})")
        if isinstance(color, str):
            try:
                color = Color(color)
            except:
                raise ColorParseError(f"Could not parse color: {color}")
            else:
                return [
                    # Color(color.darken(0.4)),
                    Color(color.darken(0.2)),
                    color,
                    Color(color.lighten(0.2)),
                    Color(color.lighten(0.6))
                ]

    def get_text(self) -> str:
        """Get the gradient text.

        Returns:
            str: The gradient text.
        """
        if isinstance(self._text, str):
            return self._text
        elif isinstance(self._text, List):
            return "".join(self._text)
        else:
            raise TypeError("Text must be a string or a list of strings.")

    def validate_colors(self, colors: Optional[List[Color]]) -> bool:
        """Validate self.colors to ensure that it is a list of colors."""
        valid: bool = True
        for color in colors:
            if not isinstance(color, Color):
                return False
        if valid:
            return True

    def get_indexes(self, verbose: bool = False) -> List[List[int]]:
        """Generate the indexes for the gradient substring.

        Returns:
            List[List[int]]: The indexes for the gradient substring.
        """
        result: ndarray = np.array_split(np.arange(self._length), self.hues - 1)
        indexes: List[List[int]] = [sublist.tolist() for sublist in result]
        for count, index in enumerate(indexes):
            msg = f"[b white]Index {count}:[/]{', '.join([str(i) for i in index])}\n\n"
            if verbose:
                log.success(msg)
            else:
                log.info(msg)
        return indexes

    def get_substrings(self, indexes: List[List[int]], text: str) -> List[str]:
        """Generate a list of substrings for the gradient.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.
            text (str): The text to generate the gradient substring from.
            verbose (bool, optional): Whether to print verbose output. Defaults to VERBOSE.
        """
        substrings: List[str] = []
        for index in indexes:
            substring = self.get_substring(index, text)
            substrings.append(substring)
        return substrings

    def get_substring(self, index: List[int], text: str) -> str:
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

    def generate_substrings(self) -> List[Span]:
        """Generate gradient spans.

        Returns:
            List[Span]: The gradient spans.
        """
        text = self.get_text()
        gradient_string = Text()
        indexes: List[List[int]] = self.get_indexes()
        substrings: List[str] = self.get_substrings(indexes, text)
        for index, substring in enumerate(substrings):
            gradient_length = len(substring)
            substring = Text(substring)

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
                red = int(r1 + (blend * dr))
                green = int(g1 + (blend * dg))
                blue = int(b1 + (blend * db))
                color = f"#{red:02X}{green:02X}{blue:02X}"
                substring.stylize(color, subindex, subindex + 1)

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
        return gradient_string

    def get_start_indexes(self, indexes: List[List[int]]) -> List[int]:
        """Get the start indexes for the gradient substring.

        Args:
            indexes (List[List[int]]): The indexes for the gradient substring.

        Returns:
            List[int]: The start indexes for the gradient substring.
        """
        start_indexes: List[int] = []
        for index in indexes:
            start_index = index[0]
            log.log("INFO", f"Start Index: {start_index}")
            start_indexes.append(start_index)
        return start_indexes

    def get_color_starts(self) -> List[Color]:
        """Generate the start colors for the gradient substring."""
        color_starts: List[Color] = []
        for index, color in enumerate(self.colors):
            if index < self.hues - 1:
                log.log("INFO", f"Color Start {index}: {color}")
                color_starts.append(color)
        return color_starts

    def get_color_ends(self) -> List[Color]:
        """Generate the end colors for the gradient substring."""
        color_ends: List[Color] = []
        for index, color in enumerate(self.colors):
            if index > 0:
                log.log("INFO", f"Color End {index}: {color}")
                color_ends.append(color)
        return color_ends

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
            self._text = [sanitized_text]
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
        """Set the number of colors in the gradient."""
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
    def style(self, style: StyleType) -> None:
        """Set the style of the gradient."""
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

    def generate_style(self, color: str) -> Style:
        """Generate a style for a color."""
        new_style = self.style + Style(color=color)
        log.debug(f"Generating style for `{color}`: {new_style}")
        return new_style


def examples() -> Layout:
    """Generate a layout for the examples of gradients."""
    TEXT = lorem.paragraphs(2)
    gradient_random = Gradient(TEXT)
    panel_random = Panel(
        gradient_random,
        title=Gradient("Random Gradient"),
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff])[/]",
        subtitle_align="right",
    )
    gradient_rainbow = Gradient(TEXT, rainbow=True)
    panel_rainbow = Panel(
        gradient_rainbow,
        title=Gradient("Rainbow Gradient", rainbow=True),
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff],[/] [#FF8800]rainbow[/] \
[#FB508E]=[/][#af00ff] True[/][#ffffff])[/]",
        subtitle_align="right",
    )
    gradient_red_orange_yellow = Gradient(TEXT, colors=["red", "orange", "yellow"])
    panel_red_orange_yellow = Panel(
        gradient_red_orange_yellow,
        title="[b #ff0000]Red[/], [b #ff8800]Orange[/]\
, [b #ffff00]Yellow[/] Gradient",
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]colors[/]\
[#FB508E]=[/][#fffff][[/][#ff0000]red[/][#ffffff], [/]\
[#ff8800] orange[/][#ffffff], [#ffff00]yellow[/]\
[#ffffff]])[/]",
        subtitle_align="right",
    )
    color_layout = Layout(name="root")
    color_layout.split_row(
        Layout(" ", name="pad1", ratio=1),
        Layout(panel_random, name="left", ratio=5),
        Layout(" ", name="pad2", ratio=1),
        Layout(panel_rainbow, name="center", ratio=5),
        Layout(" ", name="pad3", ratio=1),
        Layout(panel_red_orange_yellow, name="right", ratio=5),
        Layout(" ", name="pad4", ratio=1),
    )
    return color_layout


def style_layout() -> Layout:
    """Generate a layout for the examples of styles."""
    TEXT = lorem.paragraphs(2)
    regular = "[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff])[/]"

    bold = '[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]style[/]\
[#FB508E]=[/][#E3EC84]"bold"[/][#ffffff])[/]'

    italic_underline = '[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]style[/]\
[#FB508E]=[/][#E3EC84]"italic underline"[/][#ffffff])[/]'
    layout = Layout(name="root")
    layout.split_row(
        Layout(" ", name="pad1", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT,
                    colors=["yellow", "lime", "cyan", "lightblue"],
                ),
                title="No Style Gradient",
                padding=(2, 4),
                subtitle=regular,
                subtitle_align="right",
            ),
            ratio=5,
            name="normal",
        ),
        Layout(" ", name="pad2", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT, colors=["yellow", "lime", "cyan", "lightblue"], style="bold"
                ),
                title="Bold Gradient",
                padding=(2, 4),
                subtitle=bold,
                subtitle_align="right",
            ),
            ratio=5,
            name="bold",
        ),
        Layout(" ", name="pad3", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT,
                    colors=["yellow", "lime", "cyan", "lightblue"],
                    style="italic underline",
                ),
                title="Italic Underline Gradient",
                padding=(2, 4),
                subtitle=italic_underline,
                subtitle_align="right",
            ),
            ratio=5,
            name="italic underline",
        ),
        Layout(" ", name="pad4", ratio=1),
    )
    return layout


def example(record: bool = False) -> None:
    """Display examples of gradients.

    Args:
        record (bool, optional): Whether to record the examples. Defaults to False.
    """
    if record:
        example_console = Console(
            theme=GradientTheme(),
            record=record,
        )
    else:
        example_console = Console(
            theme=GradientTheme(),
        )
    console.rule(Gradient("Color Gradient Examples"))
    example_console.print(examples())
    example_console.line()
    example_console.print(style_layout())
    if record:
        example_console.save_svg("Images/gradient.svg", title="Gradient Examples")


if __name__ == "__main__":
    example()