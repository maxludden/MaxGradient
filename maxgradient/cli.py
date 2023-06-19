"""CLI for maxgradient."""
# pylint: disable=E0401
from enum import Enum
from typing import List

import typer
from typing_extensions import Annotated
from rich.console import Console

from maxgradient.color import Color
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTheme

app = typer.Typer()

class JustifyMethod(Enum):
    """Justify method."""
    DEFAULT = "default"
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    FULL = "full"

class OverflowMethod(Enum):
    """Overflow method."""
    DEFAULT = "default"
    CLIP = "clip"
    ELLIPSIS = "ellipsis"
    WRAP = "wrap"

@app.command()
def main(
    text: str,
    colors: Annotated[List[Color], typer.Option(
        "--colors",
        "-c",
        help="List of colors to use for gradient.")] = None,
    rainbow: Annotated[bool, typer.Option(
        "--rainbow",
        "-r",
        help="Use rainbow colors for gradient.")] = False,
    invert: Annotated[bool, typer.Option(
        "--invert",
        "-i",
        help="Invert the gradient.")] = False,
    hues: Annotated[int, typer.Option(
        "--hues",
        "-h",
        help="List of hues to use for gradient.")] = 3,
    style: Annotated[str, typer.Option(
        "--style",
        "-s",
        help="Style to use for gradient.")] = "bold",
    justify: Annotated[JustifyMethod, typer.Option(
        "--justify",
        "-j",
        help="Justify method to use for gradient.")] = JustifyMethod.DEFAULT,
    overflow: Annotated[OverflowMethod, typer.Option(
        "--overflow",
        "-o",
        help="Overflow method to use for gradient.")] = OverflowMethod.DEFAULT,
    no_wrap: Annotated[bool, typer.Option(
        "--no-wrap",
        "-n",
        help="Don't wrap text.")] = False,
    end: Annotated[str, typer.Option(
        "--end",
        "-e",
        help="End string.")] = "\n",
    tab_size: Annotated[int, typer.Option(
        "--tab-size",
        "-t",
        help="Tab size.")] = 8
    ) -> None:
    """Main function."""
    console = Console(theme=GradientTheme())
    gradient = Gradient(
        text=text,
        colors=colors,
        rainbow=rainbow,
        invert=invert,
        hues=hues,
        style=style,
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        end=end,
        tab_size=tab_size
        )
    console.print(gradient)
