"""CLI for maxgradient."""

from io import StringIO
from sys import stdout
from typing import List, Optional

from rich import inspect
from rich.panel import Panel
from typer import Argument, BadParameter, Exit, Option, Typer
from typing_extensions import Annotated

from maxgradient import Console
from maxgradient.gradient import Gradient

app = Typer(name="gradient", help="Print a gradient.")

valid_colors = [
    "magenta",
    "violet",
    "purple",
    "blue",
    "lightblue",
    "cyan",
    "green",
    "green",
    "yellow",
    "orange",
    "red",
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
            case_sensitive=False,
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
magenta, violet, purple, blue, lightblue, cyan, green/green, yellow, orange, \
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
    if text:
        if text == "":
            err_console.print(
                "[bold italic red]Error:[/bold italic red] No text provided."
            )
            raise Exit(code=1)

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
        )  # type: ignore
    else:
        console.print(gradient, justify=justify)  # type: ignore
    console.line()


if __name__ == "__main__":
    app()
