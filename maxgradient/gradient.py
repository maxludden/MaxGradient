import re
from io import StringIO
from os import environ
from typing import Any, Dict, List, Optional, Tuple

from lorem_text import lorem
from rich import inspect
from rich.align import AlignMethod
from rich.box import ROUNDED, Box
from rich.columns import Columns
from rich.console import (Console, Group, JustifyMethod, OverflowMethod,
                          RenderableType)
from rich.control import strip_control_codes
from rich.layout import Layout
from rich.padding import PaddingDimensions
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text, TextType
from rich.traceback import install as install_rich_traceback

from maxgradient.color import Color
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
StyleType = Optional[str | Style]
WHITESPACE_REGEX = re.compile(r"^\s+$")


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
            end (str, optional): Character to end text with. Defaults to "\\\\n".
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.
            verbose(`bool`): Whether to print verbose output. Defaults to False.
    """

    __slots__ = ["_colors", "invert", "color_box", "color_sample", "hues"]

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
    ) -> None:
        # inheritance and dealing with entered text
        match = WHITESPACE_REGEX.match(text)
        if match:
            text = Text.from_markup(match.group(0))
            return
        if isinstance(text, Text):
            spans = text._spans
            text = text.plain
        self.style = Style.parse(style).without_color
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

        # text
        sanitized_text = strip_control_codes(text)
        self._length = len(sanitized_text)

        # invert
        self.invert = invert

        # color_box
        self.color_sample = color_sample
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

        self.clamp_colors()
        self._spans = self.generate_spans()

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"<Gradient {self._text!r} {self._spans!r}>"

    def generate_spans(self, verbose: bool = False) -> List[Span]:
        """Generate tuples with the enumerated tuple of start and end index of each span"""
        if verbose:
            _console = Console(theme=GradientTheme())
            install_rich_traceback(console)

        spans: List[Span] = []

        length = len("".join(self._text))
        hues = len(self._colors)
        gradients = hues - 1
        gradient_length = length // gradients
        gradient_remainder = length % gradients
        subtotal = gradient_length * gradients
        total = subtotal + gradient_remainder

        if verbose:
            if length == total:
                caption = f"[italic lime]:white_check_mark: The length of the text ({length}) is equal to the total ({total}).[/]"
                captions_style = "italic lime"
            else:
                caption = f"[bold red]:x: The length of the text ({length}) is not equal to the total ({total}).[/]"
                caption_style = "bold red"
            table = Table(
                show_header=False,
                expand=False,
                caption=caption,
            )
            table.add_column("Attributes", justify="left", style="bold cyan")
            table.add_column("Values", justify="left", style="bold italic magenta")
            table.add_column("Description", justify="left", style="dim white")
            table.add_row(
                "Length", f"{length}", "The number of characters in self._text."
            )
            table.add_row("Hues", f"{hues}", "The number of colors in the gradient.")
            table.add_row(
                "Gradients", f"{gradients}", "The number of gradients in the gradient."
            )
            table.add_row(
                "Gradient Length",
                f"{gradient_length}",
                f"{length}//{gradients} | The integer division of length by gradients",
            )
            table.add_row(
                "Gradient Remainder",
                f"{gradient_remainder}",
                f"{length}%{gradients} | The remainder of length divided by gradients",
            )
            table.add_row(
                "Subtotal",
                f"{subtotal}",
                f"{gradient_length}*{gradients} | The product of gradient length and gradients",
            )
            table.add_row(
                "Total",
                f"{total}",
                f"{subtotal}+{gradient_remainder} | The sum of subtotal and gradient remainder",
            )
            _console.log(table)

        spans: List[Span] = []
        span_start = 0
        for gradient_index in range(gradients):
            gradient_start = gradient_index * gradient_length
            gradient_end = gradient_start + gradient_length
            if gradient_index < gradient_remainder:
                gradient_end += 1
            if gradient_index == gradients - 1:
                gradient_end = length

            if gradient_index < gradients:
                color1 = self._colors[gradient_index]
                r1, g1, b1 = color1.rgb_tuple
                color2 = self._colors[gradient_index + 1]
                r2, g2, b2 = color2.rgb_tuple
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1
                if verbose:
                    table = Table(show_header=False, expand=False)
                    table.add_column("Attributes", justify="left", style="bold cyan")
                    table.add_column(
                        "Values", justify="left", style="bold italic magenta"
                    )
                    table.add_column("Description", justify="left", style="dim white")
                    table.add_row(
                        "Gradient Index",
                        f"{gradient_index}",
                        "The index of the gradient.",
                    )
                    table.add_row(
                        "Gradient Start",
                        f"{gradient_start}",
                        "The start index of the gradient.",
                    )
                    table.add_row(
                        "Gradient End",
                        f"{gradient_end}",
                        "The end index of the gradient.",
                    )
                    table.add_row(
                        "Color 1",
                        f"[bold {color1.hex}]{color1}[/]",
                        "The first color of the gradient.",
                    )
                    table.add_row(
                        "Color 2",
                        f"[bold {color2.hex}]{color2}[/]",
                        "The second color of the gradient.",
                    )
                    _console.log(table)

            span_start = 0
            for span_index in range(gradient_length):
                blend = span_index / gradient_length
                span_start = gradient_start + span_index
                span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
#TODO Add support for combining styles

                span_style = self.generate_span_style(span_color)

                current_span = Span(span_start, span_start + 1, span_style)
                spans.append(current_span)
                if verbose:
                    _console.log(current_span)

        if span_start + 1 < total:
            span_start += 1
            span_color = f"#{int(r2):02X}{int(g2):02X}{int(b2):02X}"
            span_style = Style(color=span_color)
            if isinstance(self.style, (Style, str)) and self.style != "_null":
                span_style = span_style._add(self.style)

            current_span = Span(span_start, total, span_style)
            spans.append(current_span)
            if verbose:
                _console.log(current_span)
        return spans

    def clamp_colors(self) -> None:
        """Limit the number of colors (`self._colors`) in a gradient to at most one color per two characters.
        This function is used to treat edge cases where the color count exceeds that
        limit causing the last several characters in the message to be the same color
        or have no color at all."""
        length = len("".join(self._text))
        hues = len(self._colors)
        if hues > length // 2:
            self._colors = self._colors[::2]

    def generate_span_style(self, color: Color) -> Style:
        """Generate a style with the specified color."""
        if self.style is None or self.style == "_null":
            self.style=Style(color=color)
            return self.style
        if not isinstance(color, Color):
            color = Color(color)
        if isinstance(self.style, str):
            self.style = Style.parse(self.style)
        elif isinstance(self.style, Style):
            style_def = str(self.style)
            self.style = Style.parse(f"{style_def} {str(color)}")
        inspect(self.style, all=True)
        return self.style
# End of Gradient Class


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


def gradient_color_examples() -> Group:
    """Generate several examples of gradients."""
    console.line(3)
    console.rule(
        title=Gradient(
            "Types of Gradients",
            style="bold",
        )
    )
    examples_layout: Layout = Layout(name="color_example_layout")
    examples_layout.split_row(
        Layout(
            GradientPanel(
                lorem.paragraph(),
                title="Random",
                subtitle="A gradient with random colors (if no colors are specified).",
            ),
            name="random",
        ),
        Layout(
            GradientPanel(
                lorem.paragraph(),
                title="Three Color Gradient",
                colors=["red", "orange", "yellow"],
                subtitle="colors=['red', 'orange', 'yellow']",
            ),
            name="named colors",
        ),
        Layout(
            GradientPanel(
                lorem.paragraph(),
                title="X11 Colors",
                colors=["darkgreen", "green", "deepskyblue", "indigo"],
                subtitle="colors=['darkgreen', 'green', 'deepskyblue', 'indigo']",
            ),
            name="x11 colors",
        ),
        Layout(
            GradientPanel(
                lorem.paragraph(),
                colors=["#f0f", "af00ff", "#5f00ff"],
                title="HEX Colors",
                subtitle="color=['#f0f', 'af00ff', '#5f00ff']]",
            ),
            name="hex colors",
        ),
        Layout(
            GradientPanel(
                lorem.paragraph(),
                colors=["rgb(0,0,255)", "(0,136,255)", (0, 255, 255)],
                title="RGB Color Codes",
                subtitle="colors=['rgb(0,0,255)', '(0,136,255)', (0,255,255)]",
            ),
            name="rgb colors",
        ),
    )
    # examples_grid.add_row(
    #     GradientPanel(
    #         lorem.paragraph(),
    #         title="Random",
    #         subtitle="A gradient with random colors (if no colors are specified).",
    #     ),
    #     GradientPanel(
    #         lorem.paragraph(),
    #         title="Three Color Gradient",
    #         colors=['red', 'orange', 'yellow'],
    #         subtitle="colors=['red', 'orange', 'yellow']",
    #     ),
    #     GradientPanel(
    #         lorem.paragraph(),
    #         title="X11 Colors",
    #         colors=['darkgreen', 'green', 'deepskyblue', 'indigo'],
    #         subtitle="colors=['darkgreen', 'green', 'deepskyblue', 'indigo']"
    #     ),
    #     GradientPanel(
    #         lorem.paragraph(),
    #         colors=['#f0f', 'af00ff', '#5f00ff'],
    #         title="HEX Colors",
    #         subtitle="color=['#f0f', 'af00ff', '#5f00ff']]",
    #     ),
    #     GradientPanel(
    #         lorem.paragraph(),
    #         colors=['rgb(0,0,255)', '(0,136,255)', (0,255,255)],
    #         title="RGB Color Codes",
    #         subtitle="colors=['rgb(0,0,255)', '(0,136,255)', (0,255,255)]"
    #     )
    # )
    # return examples_grid


def explanation_1() -> Layout:
    console = Console(theme=GradientTheme())
    console.clear()
    console.line(2)
    examples_preface = "Gradients can be made in a number of types:"
    random_example = "\n[bold lightblue]- [/bold lightblue]\
[lime]1)[/] [bold white]When [/]\
[#ff0000]no[/#ff0000]\
[bold white] colors are specified, the text will have a [/]\
[italic bold #00ffff]random gradient[/italic bold #00ffff]\
[bold white] applied to it[/]."
    named_example = "\n[bold lightblue]- [/]\
[lime]2)[/] [bold white]When a list of color is provided, \
The gradient will be generated from those.\n The vibrant spectrum \
of colors that Gradient uses are:\n\n[/bold white]"
    x11_example = "\n\n[bold lightblue]- [/]\
[#00FF00]3)[/] [bold] \
[#FFFFFF]Colors can also be parsed from X11 keywords such as:[/]\
[#006400] `darkgreen`[/#006400],\
[#008000] `green`[/#008000], \
[#00BFFF]`deepskyblue`[/#00BFFF],\
[bold #ffffff] or [/bold #ffffff]\
[#4B0082] `indigo`[/#4B0082].[/bold]"
    hex_example = "\n[bold lightblue]- [/]\
[lime]4)[/] [bold] [white]Gradient may also be parsed \
from [italic #00ffff]3[/] or [italic #00ffff]6[/] \
digit hex color codes such as:[/]\
[bold #ff00ff] `#f0f`[/],\
[bold #af00ff] `af00ff`[/],\
[bold #ffffff] or [/]\
[bold #5f00ff]`#5f00ff`[/].[/bold]"
    rgb_example = "\n[bold lightblue]- [/]\
[lime]5)[/] [bold white]RGB Color code can be parsed from strings \
[bold #0000ff]`rgb(0, 0, 255)`[/] \
[bold white]or [/bold white]\
[bold #0088ff]`(0,136,255)`[/],\
or from tuples [#00ffff](0,255,255)[/]:"
    rgb_colors = [
        Color(color) for color in ["rgb(0,0,255)", "(0,136,255)", (0, 255, 255)]
    ]
    console.print(examples_preface, justify="center")
    console.print(random_example, justify="center")
    explanations = [named_example, x11_example, hex_example, rgb_example]
    for count in range(4):
        console.print(explanations[count], justify="center")
        if count == 0:
            colors = [Color(color) for color in Color.COLORS]
            console.print(Columns(colors, equal=True, expand=False), justify="center")


if __name__ == "__main__":
    console = Console(theme=GradientTheme())
    explanation_1()
    console.print(gradient_color_examples())
