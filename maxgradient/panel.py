"""Generate a gradient panel."""

from io import StringIO
from os import environ
from sys import stdout
from typing import TYPE_CHECKING, Any, Iterable, Optional, Tuple

from rich.align import AlignMethod
from rich.box import (
    Box,
    ASCII,
    ASCII2,
    ASCII_DOUBLE_HEAD,
    SQUARE,
    SQUARE_DOUBLE_HEAD,
    MINIMAL,
    MINIMAL_HEAVY_HEAD,
    MINIMAL_DOUBLE_HEAD,
    SIMPLE,
    SIMPLE_HEAD,
    SIMPLE_HEAVY,
    HORIZONTALS,
    ROUNDED,
    HEAVY,
    HEAVY_EDGE,
    HEAVY_HEAD,
    DOUBLE,
    DOUBLE_EDGE,
    MARKDOWN
)
from rich.cells import cell_len
from rich.console import Console, ConsoleOptions, RenderResult
from rich.containers import Lines
from rich.jupyter import JupyterMixin
from rich.measure import Measurement, measure_renderables
from rich.padding import Padding, PaddingDimensions
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style, StyleType
from rich.text import Text, TextType

from maxgradient.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.gradient import Gradient
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.log import Log
from maxgradient.theme import GradientTheme

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderableType, RenderResult

console = Console(theme=GradientTheme(), highlighter=ColorReprHighlighter())
log = Log()


def get_end_chars() -> Iterable[str]:
    """Generate a list of end chars for the boxes.

    Raises:
        ColorParseError: Unable to parse color.add()
        ColorParseError: _description_
        TypeError: Invalid type.add()

    Returns:
        list[str]: A list of the end characters of defined boxes.
    """
    BOXES = [
        ASCII,
        ASCII2,
        ASCII_DOUBLE_HEAD,
        SQUARE,
        SQUARE_DOUBLE_HEAD,
        MINIMAL,
        MINIMAL_HEAVY_HEAD,
        MINIMAL_DOUBLE_HEAD,
        SIMPLE,
        SIMPLE_HEAD,
        SIMPLE_HEAVY,
        HORIZONTALS,
        ROUNDED,
        HEAVY,
        HEAVY_EDGE,
        HEAVY_HEAD,
        DOUBLE,
        DOUBLE_EDGE,
        MARKDOWN
    ]

    for box in BOXES:
        line1, line2, line3, line4, line5, line6, line7, line8 = box.splitlines()
        # top
        _, _, _, top_right = iter(line1)
        yield top_right
        # head
        _, _, _, head_right = iter(line2)
        yield head_right

        # head_row
        _, _, _, head_row_right = iter(line3)
        yield head_row_right

        # mid
        _, _, _, mid_right = iter(line4)
        yield mid_right
        # row
        _, _, _, row_right = iter(line5)
        yield row_right
        # foot_row
        _, _, _, foot_row_right = iter(line6)
        yield foot_row_right
        # foot
        _, _, _, foot_right = iter(line7)
        yield foot_right
        # bottom
        _, _, _, bottom_right = iter(line8)
        yield bottom_right

class GradientPanel(Panel):
    """Create a gradient panel."""

    file_console = Console(
        file=StringIO(), theme=GradientTheme(), highlighter=ColorReprHighlighter()
    )

    def __init__(
        self,
        renderable: "RenderableType",
        colors: Optional[Iterable[str]] = None,
        hues: int = 3,
        rainbow: bool = False,
        box: Box = ROUNDED,
        *,
        title: Optional[TextType] = None,
        title_align: AlignMethod = "center",
        subtitle: Optional[TextType] = None,
        subtitle_align: AlignMethod = "center",
        safe_box: Optional[bool] = None,
        expand: bool = False,
        style: StyleType = "none",
        border_style: StyleType = "none",
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: PaddingDimensions = (0, 1),
        highlight: bool = False,
    ) -> None:
        """Initialize the gradient panel."""
        self.buffer = StringIO()
        self.file_console = Console(
            file=self.buffer, theme=GradientTheme(), highlighter=ColorReprHighlighter()
        )
        self.hue: int = hues
        self.rainbow: bool = rainbow
        self.colors: Optional[str | list[Color | Tuple | str]] = colors
        self.box = box
        panel = Panel(
            renderable,
            box=self.box,
            title=title,
            title_align=title_align,
            subtitle=subtitle,
            subtitle_align=subtitle_align,
            safe_box=safe_box,
            expand=expand,
            style=style,
            border_style=border_style,
            width=width,
            height=height,
            padding=padding,
            highlight=highlight,
        )
        self.width = panel.width
        self.file_console.print(panel)
        self.text: Text = Text(self.buffer.getvalue())
        self.buffer.close()
        

        self.colors = colors
        console.print(f"Colors: {[color.name for color in self.colors]}")

        for line in lines:
            console.print(
                Gradient(
                    line,
                    colors=[color.name for color in self.colors],
                    hues=hues,
                    rainbow=rainbow,
                )
            )
        self.hues = hues
        self.rainbow = rainbow
        self.colors = colors

    @property
    def colors(self) -> list[Color]:
        """Retrieve the colors for the gradient."""
        log.debug(
            f"Called colors.getter with value: {[color.name for color in self._colors]}"
        )
        return self._colors

    @colors.setter
    def colors(self, value: list[Color | Tuple | str]) -> None:
        """Set the colors for the gradient."""
        log.debug(f"Called colors.setter")
        if value is None:
            value = self.get_colors(
                input_colors=value, rainbow=self.rainbow, hues=self.hues
            )
        self.hues = len(value)
        self._colors = value

    @property
    def buffer(self) -> StringIO:
        """Retrieve the buffer for the gradient."""
        log.debug(f"Called buffer.getter")
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: StringIO) -> None:
        """Set the buffer for the gradient."""
        log.debug(f"Called buffer.setter")
        self._buffer = buffer

    @property
    def file_console(self) -> Console:
        """Retrieve the file console for the gradient."""
        log.debug(f"Called file_console.getter")
        return self._file_console

    @file_console.setter
    def file_console(self, value: Console) -> None:
        """Set the file console for the gradient."""
        log.debug(f"Called file_console.setter")
        assert isinstance(
            value, Console
        ), f"File console must be a \
            Console object. Received: {type(value)}"
        self._file_console = value

    @property
    def hues(self) -> int:
        """Retrieve the number of hues for the gradient."""
        log.debug(f"Called hues.getter with value: {self._hues}")
        return self._hues

    @hues.setter
    def hues(self, value: int) -> None:
        """Set the number of hues for the gradient."""
        log.debug(f"Called hues.setter with value: {value}")
        if value is None:
            value = len(self.colors)
        self._hues = value

    @property
    def rainbow(self) -> bool:
        """Retrieve whether the gradient is a rainbow gradient."""
        log.debug(f"Called rainbow.getter with value: {self._rainbow}")
        return self._rainbow

    @rainbow.setter
    def rainbow(self, value: bool) -> None:
        """Set whether the gradient is a rainbow gradient."""
        log.debug(f"Called rainbow.setter with value: {value}")
        assert isinstance(
            value, bool
        ), f"Rainbow must be a boolean. Received: {type(value)}"
        if value:
            self.hues = 10
        self._rainbow = value

    @property
    def lines(self) -> str:
        """Retrieve the text for the gradient."""
        log.debug(f"Called text.getter")
        return self._lines

    @lines.setter
    def lines(self, text: Text) -> None:
        """Set the text for the gradient."""
        log.debug(f"Called text.setter({text}))")
        assert isinstance(text, Text), f"Text must be a Text object. Received: {type(text)}"
        lines: Lines = text.wrap(
            console=self.file_console,
            console=self.width,
            justify=self.justify,
            overflow=self.overflow,
            tab_size=self.tab_size,
            no_wrap=self.no_wrap,
        )
        
        gradients: Iterable[Gradient] = []
        for line: Text in lines:
            line = line.plain
            gradients.append(
                Gradient(
                    line,
                    colors=[color.name for color in self.colors],
                    rainbow=self.rainbow,
                    hues=self.hues,
                    rainbow=self.rainbow,
                    justify=self.justify,
                    overflow=self.overflow,
                    tab_size=self.tab_size,
                    no_wrap=self.no_wrap,
                )
            )
        
        

    @property
    def width(self) -> int:
        """Retrieve the width of the panel."""
        log.debug(f"Called width.getter")
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Set the width of the panel."""
        log.debug(f"Called width.setter")
        self._width = value

    def get_colors(
        self,
        input_colors: Optional[list[Color | Tuple | str]] = None,
        rainbow: bool = False,
        hues: int = 3,
    ) -> list[Color]:
        """Generate or validate the colors for the gradient.

        Args:
            input_colors (list[Color|Tuple|str], optional): The colors to
                generate or validate. Defaults to None.
            rainbow (bool, optional): Whether to generate a rainbow gradient.
                Defaults to False.
            hues (int, optional): The number of hues to generate. Defaults to
                hues.
        """
        # if rainbow is True
        if rainbow:
            self.hues = 10
            colors = ColorList(self.hues).color_list
            if self.validate_colors(colors):
                return colors

        # if input colors is str
        if isinstance(input_colors, str):
            return self.mono(input_colors)

        # Validate input colors
        if input_colors is not None:
            colors: list[Color] = []
            for color in input_colors:
                try:
                    color = Color(color)
                    colors.append(color)
                except ColorParseError as cpe:
                    raise ColorParseError(
                        f"Invalid color: {color}. Must be a valid color string or Color object."
                    ) from cpe
            if self.validate_colors(colors):
                return colors

        # Generate a list of colors
        color_list = ColorList(self.hues).color_list
        colors = color_list[: self.hues]
        if self.validate_colors(colors):
            return colors

    def validate_colors(self, colors: Optional[list[Color]]) -> bool:
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

    def mono(self, color: str | Color) -> list[Color]:
        """Generate a list of monochromatic colors."""
        if isinstance(color, str):
            color = Color(color)
            try:
                color = Color(color)
            except ColorParseError as cpe:
                raise ColorParseError(
                    f"Invalid color: {color}. Must be a valid color string or Color object."
                ) from cpe
        if not isinstance(color, Color):
            raise TypeError(
                f"Invalid color: {color}. Must be a valid color string or Color object."
            )
        else:
            return [
                Color(color.darken(0.6)),
                Color(color.darken(0.3)),
                color,
                Color(color.lighten(0.3)),
                Color(color.lighten(0.6)),
            ]


if __name__ == "__main__":
    console.print(GradientPanel("Hello, World!"))
