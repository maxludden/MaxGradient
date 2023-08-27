"""CLI for maxgradient."""

import typer

# from typing import Optional
from typing_extensions import Annotated

from maxgradient import Console, Gradient  # , Color, ColorList
from maxgradient import __version__ as version
from maxgradient._gc import GradientColor as GC
from maxgradient._hex import Hex
from maxgradient._rgb import RGB
from maxgradient._rich import Rich
from maxgradient._x11 import X11

app = typer.Typer(name="gradient", help="Print a gradient.")

console = Console()
err_console = Console(stderr=True)

valid_colors = [*GC.NAMES, *Rich.NAMES, *X11.NAMES]


def complete_color(incomplete: str):
    """Complete the color."""
    completion = []
    for color in valid_colors:
        if color.startswith(incomplete):
            completion.append(color)
    return completion


@app.command()
def main(
    text: Annotated[str, typer.Argument(default="", help="Text to print")],
    style: Annotated[
        str, typer.Option("--style", "-s", default="default", show_default=False)
    ],
    rainbow: Annotated[
        bool, typer.Option("--rainbow", "-r", default=False, show_default=False)
    ],
    colors: Annotated[
        list[str],
        typer.Option(
            "--colors",
            "-c",
            default=None,
            show_default=False,
            autocompletion=complete_color,
        ),
    ],
) -> None:
    """Print a gradient.

    Args:
        text (str): Text to print. Errors if not provided.
        style (str): Style to use. Valid styles include:
            - default (no style)
            - bold
            - italic
            - underline
        rainbow (bool): Whether to use a random rainbow colors. Defaults to `False`.
        colors (list[str]): List of colors to use. Defaults to `None`.
    """
    if text == "":
        err_console.print("[bold italic red]Error:[/bold italic red] No text provided.")
        raise typer.Exit(code=1)

    if colors:
        validated_colors = []
        for color in colors:
            if Hex(color).is_valid():
                validated_colors.append(color)
                continue
            if RGB(color).is_valid():
                validated_colors.append(color)
                continue
            if color not in valid_colors:
                err_console.print(
                    f"[bold italic red]Error:[/bold italic red] Invalid color: {color}"
                )
                raise typer.Exit(code=1)
            validated_colors.append(color)

    console.gradient(text=text, colors=validated_colors, style=style, rainbow=rainbow)
