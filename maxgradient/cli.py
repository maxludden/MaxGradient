"""MaxGradient CLI"""
# pylint: disable=R0913
from typing import Annotated, List, Optional

from rich.text import Text
from typer import Option, Typer

from maxgradient._log import Log

# from maxgradient._gc import GradientColor as GC
from maxgradient.color import ColorParseError
from maxgradient.console import Console, JustifyMethod, OverflowMethod
from maxgradient.gradient import Gradient

log: Log = Log()

APP_NAME: str = "max"
app = Typer(
    name=APP_NAME,
    no_args_is_help=True,
    short_help="Print gradient colored, formatted text to the console.",
    rich_markup_mode="rich",
)


def rainbow_gradient() -> Gradient:
    """Generate the text, `rainbow gradient`, in a rainbow gradient."""
    return Gradient("rainbow gradient", rainbow=True, end=" ")


@app.command("gradient")
def gradient(
    text: Annotated[
        str,
        Option(
            "-t",
            "--text",
            help="[i white]The[/] [b i #E3EC84]text[/][i white] \
        to print.[/]",
            rich_help_panel="Gradient Options",
        ),
    ] = "",
    colors: Annotated[
        Optional[str | List[str]],
        Option(
            "-c",
            "--colors",
            help="The [i]colors[/] to of the gradient.",
            rich_help_panel="[dim lightblue]Gradient Options[/]",
        ),
    ] = None,
    rainbow: Annotated[
        Optional[bool],
        Option(
            "-r",
            "--rainbow",
            help=Text.assemble(
                [
                    "Print the text in a ",
                    rainbow_gradient(),
                    ". Much more colorful. Defaults to [b violet]False[/].",
                ]
            ),
            rich_help_panel="Gradient Options",
        ),
    ] = False,
    invert: Annotated[
        Optional[bool],
        Option(
            "-i",
            "--invert",
            help="Invert the order of the colors in the gradient. Defaults to \
            [b violet]False[/].",
            rich_help_panel="Gradient Options",
        ),
    ] = False,
    hues: Annotated[
        Optional[int],
        Option(
            "-h",
            "--hues",
            help="""The number of colors, [dim]`[/][b #7FD6E8]int[/][dim]`[/] \
to use to generate a gradient. Defaults to [bold cyan]3[/].""",
            rich_help_panel="Gradient Options",
        ),
    ] = 3,
    color_sample: Annotated[
        Optional[bool],
        Option(
            "-s",
            "--color-sample",
            help="Create a gradient color sample (`██████`), rather than gradient text. Defaults to\
            [b violet] False[/]. The color sample length is determined by the length of the text.",
            rich_help_panel="Gradient Options",
        ),
    ] = False,
    style: Annotated[
        Optional[str],
        Option(
            "-s",
            "--style",
            help="The style of the [b i #E3EC84]text[/] ([dim]`[/][b #7FD6E8]bold[/][dim]`[/], \
                [dim]`[/][b #7FD6E8]italic[/] dim]`[/], [dim]`[/][b #7FD6E8]underline[/][dim]`[/]\
                ). Defaults to [b violet]None[/].",
            rich_help_panel="Gradient Options",
        ),
    ] = None,
    justify: Annotated[
        Optional[JustifyMethod],
        Option(
            "-j",
            "--justify",
            help="The justification of the text: [dim]`[/][b #7FD6E8]left[/][dim]`[/],\
[dim]`[/][b #7FD6E8]center[/][dim]`[/], [dim]`[/][b #7FD6E8]left[/][dim]`[/], \
or [dim]`[/][b #7FD6E8]full[/][dim]`[/]. Defaults to [b i #7FD6E8]left[/][dim]`[/].",
            rich_help_panel="Text Options",
        ),
    ] = "left",
    overflow: Annotated[
        Optional[OverflowMethod],
        Option(
            "-o",
            "--overflow",
            help="The overflow method of the text: [dim]`[/][b #7FD6E8]crop[/][dim]`[/],\
[dim]`[/][b #7FD6E8]fold[/][dim]`[/], [dim]`[/][b #7FD6E8]ellipsis[/][dim]`[/], \
or [dim]`[/][b #7FD6E8]ignore[/][dim]`[/]. Defaults to [b i #7FD6E8]ellipsis[/][dim]`[/].",
            rich_help_panel="Text Options",
        ),
    ] = "fold",
    no_wrap: Annotated[
        Optional[bool],
        Option(
            "--no-wrap",
            help="Disable text wrapping. Defaults to [b violet]False[/].",
            rich_help_panel="Text Options",
        ),
    ] = False,
    end: Annotated[
        Optional[str],
        Option(
            "--end",
            help="The text to print at the end of the line. Defaults to `\\\\n`.",
            rich_help_panel="Text Options",
        ),
    ] = "",
    tab_size: Annotated[
        Optional[int],
        Option(
            "--tab-size",
            help="The number of spaces to use for a tab. Defaults to [b violet]4[/].",
            rich_help_panel="Text Options",
        ),
    ] = 8,
    console: Annotated[
        Optional[Console],
        Option(
            "-c",
            "--console",
            help="The console to print to. Defaults to [b violet]None[/].",
        ),
    ] = None,
) -> None:
    """
    Print gradient colored and formatted text to the console.

    Gradient Options:
        -t --text       The text to print. Defaults to `""`.\n
        -c --colors     The colors to create a gradient from. \
            Defaults to [dim]`[/][b violetNone[/][dim]`[/]. If \
            [i dim]`[[b violet]None[/][i dim]`[/], the gradient will \
            be generated randomly from consecutive color, [dim]`[/]\
            [b #7FD6E8]MaxGradient[/].[b #7FD6E8]gradient_color[/].\
            [b i #7FD6E8]GradientColors[/].[b white]NAMES.\n
        -r --rainbow    Print the text in a rainbow gradient. Much more colorful.\
            Defaults to [b violet]False[/].\n
        -i --invert     Invert the order of the colors in the gradient. Defaults to \
            [b violet]False[/].\n
        -h --hues       The number of colors [i dim](int)[/] to use to generate a gradient. \
            Defaults to [bold cyan]3[/].\n
        -s --style      The style of the text ([dim]`bold`, `italic`, `reverse`[/]). Defaults \
            to [b violet]None[/].\n\n\n\n

    Text Options:
        -j --justify    JustifyMethod = 'left',
        -o --Overflow   OverflowMethod = 'fold',
        --no-wrap       Disable text wrapping. Defaults to [b violet]False[/].\n
        --end           The text to print at the end of the line. Defaults to `\\\\n`.\n
        --tab-size      The number of spaces to use for a tab. Defaults to [b violet]8[/].\n
    
    Console Options:
        -c --console    The console to print to. Defaults to [b violet]None[/].\n
    """
    if not console:
        console = Console()

    console.line(2)
    try:
        console.print(
            Gradient(
                text=text,
                colors=colors,
                rainbow=rainbow,
                invert=invert,
                hues=hues,
                color_sample=color_sample,
                style=style,
                justify=justify,
                overflow=overflow,
                no_wrap=no_wrap,
                end=end,
                tab_size=tab_size,
            ),
            justify=justify,
            overflow=overflow,
        )
    except ColorParseError as cpe:
        console.log(f"[bold red]ERROR:[/] {cpe}")
