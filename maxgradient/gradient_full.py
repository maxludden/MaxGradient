"""Streamline Gradient class"""
# pylint: disable=W0621,C0103,W0622,E0401,E0611,C0412, w1203
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from io import StringIO
from multiprocessing import cpu_count

# from itertools import groupby
from operator import itemgetter
from time import sleep
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, Union

import numpy as np
from nptyping import NDArray, Shape
from rich.box import Box
from rich.cells import cell_len
from rich.console import Console, ConsoleOptions, ConsoleRenderable
from rich.containers import Lines, Renderables
from rich.control import strip_control_codes
from rich.measure import Measurement
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback

from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.log import Log
from maxgradient.theme import GradientTerminalTheme, GradientTheme

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

    # __slots__ = [
    #     "colors",
    #     "_color_sample",
    #     "_hues",
    #     "_style",
    #     "_color_sample",
    #     "_console",
    #     "_buffer",
    # ]

    def __init__(
        self,
        renderable: Optional[str | Text | ConsoleRenderable] = "",
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
            renderableRich(`text): The text to print. Defaults to `""`.\n
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
        buffer = StringIO()
        console = Console(
            theme=GradientTheme(),
            highlighter=ColorReprHighlighter(),
            record=True,
        )
        renderable = "Enim ad exercitation labore culpa non sint nisi duis \
ad ad enim enim. Ea quis irure pariatur. Enim veniam dolor esse ipsum \
eiusmod nulla cillum non eu non velit deserunt sint pariatur cupidatat. \
Ut exercitation nulla dolore."

        console.log(renderable)

        panel = Panel.fit(
            Gradient(renderable),
            title="Panel Title",
            border_style="bold",
            width=70,
            padding=(1, 4),
        )
        console.print(panel)
        buffer = StringIO()
        console = Console(
            file=buffer,
            theme=GradientTheme(),
            highlighter=ColorReprHighlighter(),
            record=True,
        )

        panel = Panel.fit(renderable)
        console.save_svg(
            "docs/img/buffer_output.svg",
            title="Buffer Output",
            theme=GradientTerminalTheme(),
        )
        output = buffer.getvalue()
        buffer.close()
        console.log(f"Output: {output}")

        super().__init__(
            text=renderable,
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

    # Dunder methods
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

    # Properties
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
    def justify(self) -> JustifyMethod:
        """The justification of the gradient."""
        log.debug(f"Retrieving gradient._justify()")
        if not self._justify:
            self._justify = DEFAULT_JUSTIFY
        return self._justify

    @justify.setter
    def justify(self, justify: JustifyMethod) -> None:
        """Set the justification of the gradient.

        Args:
            justify(`JustifyMethod`): The justification to set the gradient to.
        """
        log.debug(f"Setting gradient._justify: {justify}")
        if justify is None:
            self._justify = DEFAULT_JUSTIFY
        else:
            self._justify = justify

    @property
    def overflow(self) -> OverflowMethod:
        """The overflow of the gradient."""
        log.debug(f"Retrieving gradient._overflow()")
        return self._overflow

    @overflow.setter
    def overflow(self, overflow: OverflowMethod) -> None:
        """Set the overflow of the gradient.

        Args:
            overflow(`OverflowMethod`): The overflow to set the gradient to.
        """
        log.debug(f"Setting gradient._overflow()")
        if overflow is None:
            self._overflow = DEFAULT_OVERFLOW
        else:
            self._overflow = overflow

    @property
    def end(self) -> str:
        """The end character of the gradient."""
        log.debug(f"Retrieving gradient._end())")
        return self._end

    @end.setter
    def end(self, end: str) -> None:
        """Set the end character of the gradient.

        Args:
            end(`str`): The end character to set the gradient to.
        """
        log.debug(f"Setting gradient._end())")
        if end is None:
            self._end = "\n"
        else:
            self._end = end

    @property
    def no_wrap(self) -> bool:
        """Whether to wrap the gradient."""
        log.debug(f"Retrieving gradient._no_wrap()")
        return False

    @no_wrap.setter
    def no_wrap(self, no_wrap: bool) -> None:
        """Set whether to wrap the gradient.

        Args:
            no_wrap(`bool`): Whether to wrap the gradient.
        """
        log.debug(f"Setting gradient._no_wrap()")
        if no_wrap is None:
            self._no_wrap = False
        else:
            self._no_wrap = no_wrap

    @property
    def hues(self) -> int:
        """The number of colors in the gradient."""
        log.debug(f"Retrieving gradient._hues()")
        return self._hues

    @hues.setter
    def hues(self, hues: int) -> None:
        """Set the number of colors in the gradient.

        Args:
            hues (int): The number of colors in the gradient. Defaults to `3`.
        """
        log.debug(f"Setting gradient._hues()")
        if hues < 2:
            raise ValueError("Gradient must have at least two colors.")
        self._hues = hues

    @property
    def color_sample(self) -> bool:
        """Whether the gradient is a color sample."""
        log.debug(f"Retrieving gradient._color_sample()")
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

    @property
    def buffer(self) -> StringIO:
        """The buffer for the gradient."""
        log.debug(f"Retrieving gradient._buffer")
        if self._buffer is None:
            self._buffer: StringIO = StringIO()
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: StringIO) -> None:
        """Set the buffer for the gradient.

        Args:
            buffer(`StringIO`): The buffer to set the gradient to.
        """
        log.debug(f"Setting gradient._buffer: {buffer}")
        if isinstance(buffer, StringIO):
            self._buffer: StringIO = buffer
        else:
            raise TypeError(f"Buffer must be a StringIO, not {type(buffer)}")

    @property
    def console(self) -> Console:
        """The file console for the gradient."""
        log.debug(f"Retrieving gradient._console")
        if self._console is None:
            self._console = Console(
                file=self.buffer,
                theme=GradientTheme(),
                highlighter=ColorReprHighlighter(),
            )
        return self._console

    @console.setter
    def console(self, console: Console) -> None:
        """Set the file console for the gradient.

        Args:
            console(`Console`): The file console to set the gradient to.
        """
        log.debug(f"Setting gradient._console: {console}")
        if isinstance(console, Console):
            self._console = console
        else:
            raise TypeError(f"File console must be a Console, not {type(console)}")

    @property
    def tab_size(self) -> int:
        """The tab size for the gradient."""
        return 4

    @tab_size.setter
    def tab_size(self, tab_size: int) -> None:
        """Set the tab size for the gradient.

        Args:
            tab_size(`int`): The tab size to set the gradient to.
        """
        log.debug(f"Setting gradient._tab_size: {tab_size}")
        if tab_size is None:
            self._tab_size = 4
        else:
            self._tab_size = tab_size
