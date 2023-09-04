"""MaxGradient.main"""
from typing import Iterable

from lorem_text import lorem
from rich.columns import Columns
from rich.panel import Panel

from maxgradient.console import Console
from maxgradient.gradient import Gradient

def generate_panels() -> Iterable[Panel]:
    """Generate panels for the examples of gradients."""
    TEXT = lorem.paragraph()

    # Formatted strings for the titles & subtitles
    c_gradient = "[#7FD6E8]Gradient[/]"
    r_para = "[#fff]([/]"
    l_para = "[#fff])[/]"
    r_brac = "[#fff]][/]"
    l_brac = "[#fff][[/]"
    comma = "[#fff], [/]"
    c_text = "[#B088E7]TEXT[/]"
    c_true = "[#B088E7]True[/]"
    equal = "[#Fb508e]=[/]"
    cyan = "[#00ffff]cyan[/]"
    c_cyan = "[bold #00ffff]Cyan[/]"
    lightblue = "[#0088ff]lightblue[/]"
    c_lightblue = "[bold #0088ff]Lightblue[/]{comma}"
    blue = "[#0000ff]blue[/]"
    c_blue = f"[bold #0000ff]Blue[/]{comma}"
    purple = "[#5f00ff]purple[/]"
    c_purple = f"[bold #5f00ff]Purple[/]{comma}"
    violet = "[#af00ff]violet[/]"
    c_violet = f"[bold #af00ff]Violet[/]{comma}"
    magenta = "[#ff00ff]magenta[/]"
    c_magenta = f"[bold #ff00ff]Magenta[/]{comma}"
    red = "[#ff0000]red[/]"
    c_red = "[bold #ff0000]Red[/]"
    orange = "[#ff8800]orange[/]"
    c_orange = "[bold #ff8800]Orange[/]"
    yellow = "[#ffff00]yellow[/]"
    c_yellow = "[bold #ffff00]Yellow[/]"
    c_rainbow = "[#D59A5A]rainbow[/]"
    c_colors = "[#D59A5A]colors[/]"

    # Random Gradient
    yield Panel(
        Gradient(TEXT),
        title=Gradient(
            "Random Gradient",
            style="bold"
        ),
        padding=(2, 4),
        subtitle=f"{c_gradient}{r_para}{c_text}{l_para}",
        subtitle_align="right",
        width=80,
    )

    # Rainbow Gradient
    yield Panel(
        Gradient(TEXT, rainbow=True),
        title=Gradient(
            "Rainbow Gradient",
            rainbow=True,
            style="bold"
        ),
        padding=(2, 4),
        subtitle=f"{c_gradient}{r_para}{c_text}{comma} \
{c_rainbow}{equal}{c_true}{l_para}",
        subtitle_align="right",
        width=80,
    )

    # Red, Orange, Yellow Gradient
    gradient_short = Gradient(TEXT, colors=["red", "orange", "yellow"])
    sub_1_1 = f"{c_gradient}{r_para}{c_text}{comma}"
    sub_1_2 = f"{c_colors}{equal}{l_brac}\
{red}{comma}{orange}{comma}{yellow}{r_brac}{l_para}"
    short_subtitle = f"{sub_1_1}{sub_1_2}"
    yield Panel(
        gradient_short,
        title=f"{c_red}, {c_orange}, [#888]and[/] {c_yellow} [b]Gradient[/]",
        padding=(2, 4),
        subtitle=short_subtitle,
        subtitle_align="right",
        width=80,
    )

    # Magenta, Violet, Purple, Blue, Lightblue, Cyan Gradient
    gradient_long = Gradient(TEXT, colors=["magenta", "violet", "purple", \
"blue", "lightblue", "cyan"])
    sub_2_1 = f"{c_gradient}{r_para}{c_text}{comma}"
    sub_2_2 = f"{c_colors}{equal}{l_brac}"
    sub_2_3 = f"{magenta}{comma}{violet}{comma}{purple}\n{comma}"
    sub_2_4 = f"{blue}{comma}{lightblue}{comma}{cyan}{r_brac}{l_para}"
    long_subtitle = f"{sub_2_1}{sub_2_2}{sub_2_3}{sub_2_4}"
    yield Panel(
        gradient_long,
        title=f"{c_magenta}{c_violet}{c_purple}{c_blue}{c_lightblue}\
[#888]and[/] {c_cyan} [b]Gradient[/]",
        padding=(2, 4),
        subtitle=long_subtitle,
        subtitle_align="right",
        width=80,
    )


def main() -> None:
    """Run the main function."""

    console = Console(record=True)
    console.line(2)
    console.gradient_rule("[b]Gradient Color Examples[/]")
    console.line(2)
    console.print(
        Columns(
            generate_panels(),
            padding=(2, 8),
            equal=True),
            justify="center"
    )
    console.line()
    console.save_max_svg(
        "docs/img/main_examples.svg",
        title="MaxGradient Examples",
    )


if __name__ == "__main__":
    main()
