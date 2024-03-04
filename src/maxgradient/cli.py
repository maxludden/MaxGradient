"""CLI for maxgradient."""

from io import StringIO
from sys import stdout
from typing import List, Optional

from rich import inspect
from rich.console import Console
from rich.panel import Panel
from typer import Argument, BadParameter, Exit, Option, Typer
from typing_extensions import Annotated

from maxgradient.gradient import Gradient

app = Typer(name="gradient", help="Print text to the console in a gradient of colors.")

valid_colors = [
    "magenta",
    "purple",
    "violet",
    "blue",
    "dodgerblue",
    "deepskyblue",
    "lightskyblue",
    "cyan",
    "springgreen",
    "lime",
    "greenyellow",
    "yellow",
    "orange",
    "darkorange",
    "red",
    "deeppink",
    "hotpink",
]

VALID_HEX = [
    "#ff00ff", # 1 - magenta
    "#af00ff", # 2 - violet
    "#5f00ff", # 3 - purple
    "#0000ff", # 4 - blue
    "#005fff", # 5 - dodgerblue
    "#00afff", # 6 - deepskyblue
    "#00ffff", # 7 - cyan
    "#00ffaf", # 8 - springgreen
    "#00ff00", # 10 - lime
    "#5fff00", # 11 - greenyellow
    "#ffff00", # 12 - yellow
    "#ffaf00", # 13 - orange
    "#ff5f00", # 14 - darkorange
    "#ff0000", # 15 - red
    "#ff005f", # 16 - deeppink
    "#ff00af" ## 17 - hotpink
]


def complete_color(incomplete: str):
    """Complete the color."""
    completion = []
    for color in valid_colors:
        if color.startswith(incomplete):
            completion.append(color)
    return completion


def justify_callback(value: str):
    """Validate the justify value."""
    if value not in ["default", "left", "center", "right"]:
        raise BadParameter(
            f"Invalid justify method: {value}. Valid methods include: `default`, `left`, `center`, `right`"
        )
    return value


def parse_console(value: str):
    """Parse the console value."""
    if value.lower() == "true":
        return Console(file=StringIO())
    elif value.lower() == "false":
        return Console(file=stdout)
    else:
        raise BadParameter(
            f"Invalid console: {value}. Valid consoles include: true, false"
        )


@app.command()
def main(
    text: Annotated[str, Argument(..., help="Text to print")] = "",
    style: Annotated[
        str,
        Option(
            "--style",
            "-s",
            show_default=False,
            help="Style to use. Valid styles include: bold, italic, underline",
        ),
    ] = "default",
    rainbow: Annotated[
        bool,
        Option(
            "--rainbow",
            "-r",
            show_default=False,
            help="Whether to use a random rainbow of colors for the Gradient.",
        ),
    ] = False,
    justify: Annotated[
        str,
        Option(
            "--justify",
            "-j",
            case_sensitive=True,
            callback=justify_callback,
            help="Justify method to use. Valid methods include: \
default, left, center, right",
        ),
    ] = "default",
    colors: Annotated[
        Optional[List[str]],
        Option(
            "--colors",
            "-c",
            case_sensitive=False,
            autocompletion=complete_color,
            help="Colors to use in the gradient. Valid colors include: \
magenta, violet, purple, blue, dodgerblue, deepskyblue, cyan, lime, yellow, orange, darkorange\
and red.",
        ),
    ] = None,
    panel: Annotated[
        bool,
        Option(
            "--panel",
            "-p",
            show_default=False,
            help="Whether to print the gradient in a panel.",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        Option(
            "--verbose",
            "-v",
            show_default=False,
            is_eager=True,
            help="Whether to print verbose output.",
        ),
    ] = False,
) -> None:
    """Print gradient colored text to the console."""
    console = Console()
    err_console = Console(stderr=True)

    # Text
    if text:
        if text == "":
            err_console.print(
                "[bold italic red]Error:[/bold italic red] No text provided."
            )
            raise Exit(code=1)

    # verify that the text
    if isinstance(style, list):
        style = " ".join(style)

    if justify:
        justify = justify
        if justify not in ["default", "left", "center", "right"]:
            error_msg = "[b italic red]Error:[/] Invalid justify method: "
            err_console.print(
                f"{error_msg}{justify}. Valid methods include: `default`, `left`, `center`, `right`"
            )
            raise Exit(code=1)

    if colors:
        gradient = Gradient(
            text=text,
            colors=colors,  # type: ignore
            style=style,
            rainbow=rainbow,
            justify=justify,  # type: ignore
        )

    elif rainbow:
        gradient = Gradient(text=text, style=style, rainbow=rainbow)
    else:
        gradient = Gradient(text=text, style=style)
    if verbose:
        inspect(gradient)
    console.line()

    if panel:
        console.print(
            Panel(gradient, border_style="dim"), justify=justify  # type: ignore
        )
    else:
        console.print(gradient, justify=justify)  # type: ignore
    console.line()


if __name__ == "__main__":
    app()
