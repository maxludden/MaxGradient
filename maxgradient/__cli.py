# ruff: noqa: F401
import click
from rich.style import Style, StyleType
from rich.text import Text, TextType, Span
from typing import Any, List, Optional

from maxgradient import (
    Console,
    Gradient,
    JustifyMethod,
    OverflowMethod,
    Panel,
    Color,
    ColorList
)

@click.command(
    name="gradient",
    help="Print a gradient to the console.",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.argument(
    "text",
    type=str,
    required=True,
)
@click.option( # color
    '--colors',
    '-c',
    type=click.Choice(
        [
            "magenta",
            "violet",
            "purple",
            "blue",
            "lightblue",
            "cyan",
            "green",
            "yellow",
            "orange",
            "red",
        ],
        case_sensitive=False
    ),
    multiple=True,
    help="Colors to use in the gradient. Valid colors include: \
        magenta, violet, purple, blue, lightblue, \
        cyan, green/green, yellow, orange, and red.",

)
@click.option( # rainbow
    "--rainbow",
    "-r",
    is_flag=True,
    help="Whether to use a random rainbow of colors for the Gradient.",
)
@click.option( # hues
              "--hues",
    "-h",
    type=click.INT,
    help="Number of hues to use in the gradient. Valid numbers include: \
        2-10.",
    default=3
)
@click.option( # justify
    "--justify",
    "-j",
    type=click.Choice(
        [
            "default",
            "left",
            "center",
            "right",
        ],
        case_sensitive=False
    ),
    default="default",
    help="Justify the gradient. Valid methods include: \
        default, left, center, and right.",
)
@click.option( # style
    "--style",
    "-s",
    type=click.Choice(
        [
            "default",
            "bold",
            "italic",
            "underline",
        ],
        case_sensitive=False
    ),
    default="default",
    help="Style to use. Valid styles include: bold, italic, underline.\
        Default is no style.",
)
def gradient(
    text: str | Text | None = "",
    colors: Optional[List[str]] = None,
    rainbow: bool = False,
    hues: int | None = None,
    style: StyleType = Style.null(),
    *,
    justify: JustifyMethod | None = None,
    overflow: OverflowMethod | None = None,
    no_wrap: bool | None = None,
    end: str = "\n",
    tab_size: int | None = 4,
    spans: List[Span] | None = None) -> None:
    """Print a gradient to the console."""
    gradient_colors: List[Color] = []
    if colors is None:
        if hues is None:
            hues = 3
        if rainbow:
            hues = 10
        if hues > 10:
            hues = 10
        if hues < 2:
            hues = 2
        gradient_colors = ColorList(hues=hues).color_list[0:hues]
    else:
        for color in colors:
            gradient_colors.append(Color(color))
    console = Console(
        tab_size=tab_size or 4,
        style=style
    )
    gradient = Gradient(
        text=text,
        colors= gradient_colors, #type: ignore
        rainbow=rainbow,
        hues=hues,
        style=style,
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        end=end,
    )
    console.print(gradient)

if __name__ == "__main__":
    gradient()
