"""MaxGradient.main"""
from typing import Iterable

from lorem_text import lorem
from rich.columns import Columns
from rich.layout import Layout
from rich.panel import Panel

import maxgradient as mg
from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTheme

console = Console()
console.print(f"Console Width: {console.width}")


def examples() -> Layout:
    """Generate a layout for the examples of gradients."""
    TEXT = lorem.paragraphs(2)
    gradient_random = Gradient(TEXT)
    panel_random = Panel(
        gradient_random,
        title=Gradient("Random Gradient"),
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff])[/]",
        subtitle_align="right",
    )
    gradient_rainbow = Gradient(TEXT, rainbow=True)
    panel_rainbow = Panel(
        gradient_rainbow,
        title=Gradient("Rainbow Gradient", rainbow=True),
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff],[/] [#FF8800]rainbow[/] \
[#FB508E]=[/][#af00ff] True[/][#ffffff])[/]",
        subtitle_align="right",
    )
    gradient_red_orange_yellow = Gradient(TEXT, colors=["red", "orange", "yellow"])
    panel_red_orange_yellow = Panel(
        gradient_red_orange_yellow,
        title="[b #ff0000]Red[/], [b #ff8800]Orange[/]\
, [b #ffff00]Yellow[/] Gradient",
        padding=(2, 4),
        subtitle="[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]colors[/]\
[#FB508E]=[/][#fffff][[/][#ff0000]red[/][#ffffff], [/]\
[#ff8800] orange[/][#ffffff], [#ffff00]yellow[/]\
[#ffffff]])[/]",
        subtitle_align="right",
    )
    color_layout = Layout(name="root")
    color_layout.split_row(
        Layout(" ", name="pad1", ratio=1),
        Layout(panel_random, name="left", ratio=5),
        Layout(" ", name="pad2", ratio=1),
        Layout(panel_rainbow, name="center", ratio=5),
        Layout(" ", name="pad3", ratio=1),
        Layout(panel_red_orange_yellow, name="right", ratio=5),
        Layout(" ", name="pad4", ratio=1),
    )
    return color_layout


def style_layout() -> Layout:
    """Generate a layout for the examples of styles."""
    TEXT = lorem.paragraphs(2)
    regular = "[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff])[/]"

    bold = '[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]style[/]\
[#FB508E]=[/][#E3EC84]"bold"[/][#ffffff])[/]'

    italic_underline = '[#7FD6E8]Gradient[/][#ffffff]([/]\
[#af00ff]TEXT[/][#ffffff], [/][#ff8800]style[/]\
[#FB508E]=[/][#E3EC84]"italic underline"[/][#ffffff])[/]'
    layout = Layout(name="root")
    layout.split_row(
        Layout(" ", name="pad1", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT,
                    colors=["yellow", "lime", "cyan", "lightblue"],
                ),
                title="No Style Gradient",
                padding=(2, 4),
                subtitle=regular,
                subtitle_align="right",
            ),
            ratio=5,
            name="normal",
        ),
        Layout(" ", name="pad2", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT, colors=["yellow", "lime", "cyan", "lightblue"], style="bold"
                ),
                title="Bold Gradient",
                padding=(2, 4),
                subtitle=bold,
                subtitle_align="right",
            ),
            ratio=5,
            name="bold",
        ),
        Layout(" ", name="pad3", ratio=1),
        Layout(
            Panel(
                Gradient(
                    TEXT,
                    colors=["yellow", "lime", "cyan", "lightblue"],
                    style="italic underline",
                ),
                title="Italic Underline Gradient",
                padding=(2, 4),
                subtitle=italic_underline,
                subtitle_align="right",
            ),
            ratio=5,
            name="italic underline",
        ),
        Layout(" ", name="pad4", ratio=1),
    )
    return layout


def example(record: bool = False) -> None:
    """Display examples of gradients.

    Args:
        record (bool, optional): Whether to record the examples. Defaults to False.
    """
    if record:
        example_console = Console(
            theme=GradientTheme(),
            record=record,
        )
    else:
        example_console = Console(
            theme=GradientTheme(),
        )
    example_console.rule(Gradient("Color Gradient Examples"))
    example_console.print(examples())
    example_console.line()
    example_console.print(style_layout())
    if record:
        example_console.save_svg("Images/gradient.svg", title="Gradient Examples")


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
    c_text = f"[#B088E7]TEXT[/]"
    c_true = "[#B088E7]True[/]"
    equal = "[#Fb508e]=[/]"
    cyan = "[#00ffff]cyan[/]"
    c_cyan = f"[bold #00ffff]Cyan[/]"
    lightblue = "[#0088ff]lightblue[/]"
    c_lightblue = f"[bold #0088ff]Lightblue[/]{comma}"
    blue = "[#0000ff]blue[/]"
    c_blue = f"[bold #0000ff]Blue[/]{comma}"
    purple = "[#5f00ff]purple[/]"
    c_purple = f"[bold #5f00ff]Purple[/]{comma}"
    violet = "[#af00ff]violet[/]"
    c_violet = f"[bold #af00ff]Violet[/]{comma}"
    magenta = "[#ff00ff]magenta[/]"
    c_magenta = f"[bold #ff00ff]Magenta[/]{comma}"
    red = "[#ff0000]red[/]"
    c_red = f"[bold #ff0000]Red[/]"
    orange = "[#ff8800]orange[/]"
    c_orange = f"[bold #ff8800]Orange[/]"
    yellow = "[#ffff00]yellow[/]"
    c_yellow = f"[bold #ffff00]Yellow[/]"
    c_rainbow = "[#D59A5A]rainbow[/]"
    c_colors = "[#D59A5A]colors[/]"

    # Random Gradient
    yield Panel(
        Gradient(TEXT),
        title=Gradient("Random Gradient"),
        padding=(2, 4),
        subtitle=f"{c_gradient}{r_para}{c_text}{l_para}",
        subtitle_align="right",
        width=80,
    )

    # Rainbow Gradient
    yield Panel(
        Gradient(TEXT, rainbow=True),
        title=Gradient("Rainbow Gradient", rainbow=True),
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
    console.line(2)
    console.gradient_rule("Gradient Color Examples")
    console.line(2)
    console.print(
        Columns(
            generate_panels(),
            padding=(2, 8),
            equal=True),
            justify="center"
    )
    console.line()
    # console.print(style_layout())


if __name__ == "__main__":
    main()
