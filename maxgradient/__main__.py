"""MaxGradient.main"""
from rich.layout import Layout
from rich.panel import Panel
from lorem_text import lorem
from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTheme
import maxgradient as mg

console = Console()
console.gradient("Hello, World!")


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


if __name__ == "__main__":
    example()
