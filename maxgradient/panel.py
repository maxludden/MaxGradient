"""A wrapper around rich.panel.Panel that contains gradient text. GradientPanel also has
attributes to control whether to make the panel's title gradient as well as all of panel's other attributes."""
from io import StringIO
from re import compile
from typing import List, Optional, Tuple

from rich.align import AlignMethod
from rich.box import ROUNDED, Box
from rich.console import Console, JustifyMethod, RenderableType
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.text import Text, TextType

from examples.color import Color
from maxgradient.original_gradient import DEFAULT_JUSTIFY, Gradient


class GradientPanel(Panel):
    """Generate a rich.panel.Panel with gradient text. and optionally a gradient border."""

    def __init__(
        self,
        renderable: RenderableType,
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        justify: JustifyMethod = DEFAULT_JUSTIFY,
        *,
        box: Box = ROUNDED,
        style: StyleType = "none",
        title: Optional[TextType] = "",
        title_align: AlignMethod = "center",
        gradient_title: bool = True,
        title_rainbow: bool = False,
        title_invert: bool = False,
        title_hues: Optional[int] = None,
        title_colors: Optional[List[Color | Tuple | str]] = None,
        title_style: StyleType = "bold #ffffff",
        subtitle: TextType | None = "",
        subtitle_align: AlignMethod = "center",
        safe_box: bool | None = None,
        expand: bool = True,
        border_style: StyleType = "bold #aaaaaa",
        width: int | None = None,
        height: int | None = None,
        padding: PaddingDimensions = ...,
        highlight: bool = False,
    ) -> None:
        self.renderable = self.parse_renderable(renderable)
        self.colors = colors
        self.rainbow = rainbow
        self.invert = invert
        self.hues = hues
        self.justify = justify
        self.box = box
        self.style = style
        self.title = title
        self.title_align = title_align
        self.gradient_title = gradient_title
        self.title_colors = title_colors
        self.title_rainbow = (title_rainbow,)
        self.title_invert = (title_invert,)
        self.title_hues = (title_hues,)
        self.title_style = (title_style,)
        if not self.gradient_title:
            title_style = f"bold underline {self.title_style} #ffffff"
        self.subtitle = subtitle
        self.subtitle_align = subtitle_align
        self.safe_box = safe_box
        self.expand = expand
        self.border_style = border_style
        self.width = width
        self.height = height
        self.padding = padding
        self.highlight = highlight

        # Panel Gradient
        self.renderable = Gradient(
            text=self.renderable,
            colors=self.colors,
            style=self.style,
            rainbow=self.rainbow,
            invert=self.invert,
            hues=self.hues,
            justify=self.justify,
        )

        # Panel Title Gradient
        if gradient_title:
            self.title = Gradient(
                text=str(self.title),
                colors=self.title_colors,
                style=self.title_style,
                rainbow=self.title_rainbow,
                invert=self.title_invert,
                hues=self.title_hues,
                justify=self.title_align,
            )
        else:
            self.title = Text(
                self.title, style=self.title_style, justify=self.title_align
            )

        # Style
        if self.style is not None:
            assert isinstance(
                self.style, StyleType
            ), f"Style must be a string or rich.style.Style, not {self.style!r}"
            if isinstance(self.style, str):
                self.style = Style.parse(self.style).without_color
            elif isinstance(self.style, Style):
                self.style = self.style.without_color

        # Title Style
        if self.title_style is not None:
            assert isinstance(
                self.title_style, StyleType
            ), f"Style must be a string or rich.style.Style, not {self.title_style!r}"
            if isinstance(self.title_style, str):
                self.title_style = Style.parse(self.title_style).without_color
            elif isinstance(self.title_style, Style):
                self.title_style = self.title_style.without_color

        super().__init__(
            self.renderable,
            box=self.box,
            title=self.title,
            title_align=self.title_align,
            subtitle=self.subtitle,
            subtitle_align=self.subtitle_align,
            safe_box=self.safe_box,
            expand=self.expand,
            style=self.style,
            border_style=self.border_style,
            width=self.width,
            height=self.height,
            padding=self.padding,
            highlight=self.highlight,
        )

    def parse_renderable(self, renderable: RenderableType) -> str:
        """Parse the renderable object into a string."""
        if isinstance(renderable, Text):
            renderable = renderable.plain
        elif isinstance(renderable, str):
            return renderable
        else:
            buffer = StringIO()
            console = Console(file=buffer, no_color=True, record=True)
            console.print(renderable)
            renderable = console.export_text()
        return renderable.__str__()
