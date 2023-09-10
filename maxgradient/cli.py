"""CLI for maxgradient."""

from io import StringIO
from sys import stdout
from typing import List

from rich.text import Text
from typer import Argument, BadParameter, Exit, Option, Typer
from typing_extensions import Annotated

from maxgradient import Console
from maxgradient import __version__ as version
from maxgradient.color import Color, ColorParseError
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTheme

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

valid_justify = ["default", "left", "center", "right"]


def complete_color(incomplete: str):
    """Complete the color."""
    completion = []
    for color in valid_colors:
        if color.startswith(incomplete):
            completion.append(color)
    return completion


def justify_callback(value: str):
    """Validate the justify value."""
    if value not in valid_justify:
        raise BadParameter(
            f"Invalid justify method: {value}. Valid methods include: {valid_justify}"
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
        List[str],
        Option(
            "--style",
            "-s",
            show_default=False,
            help="Style to use. Valid styles include: bold, italic, underline",
        ),
    ] = ["default"],
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
            help="Justify method to use. Valid methods include: default, left, center, right",
        ),
    ] = "default",
    colors: Annotated[
        List[str],
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
        if verbose:
            console.print(f"[bold italic green]Text:[/bold italic green] {text}")

    if style:
        style = " ".join(style)
        if verbose:
            console.print(f"[bold italic green]Style:[/bold italic green] {style}")

    if justify:
        justify = justify.lower()
        if justify not in valid_justify:
            err_console.print(
                f"[bold italic red]Error:[/bold italic red] Invalid justify method: {justify}. Valid methods include: {valid_justify}"
            )
            raise Exit(code=1)
        if verbose:
            console.print(f"[bold italic green]Justify:[/bold italic green] {justify}")

    if colors != [] and colors is not None:
        validated_colors = []
        for color in colors:
            try:
                valid_color = Color(color)
                validated_colors.append(valid_color)
            except ColorParseError as cpe:
                err_console.print(f"[bold italic red]Error:[/bold italic red] {cpe}")
                raise Exit(code=2) from cpe
        if verbose:
            console.print(
                f"[bold italic green]Colors:[/bold italic green] {', '.join(validated_colors)}"
            )

        gradient = Gradient(
            text=text,
            colors=validated_colors,
            style=style,
            rainbow=rainbow,
            justify=justify,
        )

    elif rainbow:
        gradient = Gradient(text=text, style=style, rainbow=rainbow)
    else:
        gradient = Gradient(text=text, style=style)
    console.line()
    console.print(gradient, justify=justify)


if __name__ == "__main__":
    app()
