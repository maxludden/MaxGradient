from maxgradient.console import Console
from maxgradient._color import Color
from maxgradient.theme import GRADIENT_TERMINAL_THEME


def color_red() -> None:
    """Print the color red"""
    console = Console(width=80, record=True)
    console.line()
    console.print(Color("red"), justify="center")
    console.line(2)
    console.save_html(
        "docs/img/color_red.html",
        theme=GRADIENT_TERMINAL_THEME,
    )


def color_aaffaa() -> None:
    """Print the color #aaffaa"""
    console = Console(width=80, record=True)
    console.line()
    console.print(Color("#aaffaa"), justify="center")
    console.line(2)
    console.save_svg(
        "docs/img/color_aaffaa.svg",
        title="Color #AAFFAA",
        theme=GRADIENT_TERMINAL_THEME,
    )


def color_darkorchid() -> None:
    """Print the X11 color DarkOrchid"""
    console = Console(width=80, record=True)
    console.line()
    console.print(Color("DarkOrchid"), justify="center")
    console.line(2)
    console.save_svg(
        "docs/img/color_darkorchid.svg",
        title="Color DarkOrchid",
        theme=GRADIENT_TERMINAL_THEME,
    )


if __name__ == "__main__":
    color_red()
    color_aaffaa()
    color_darkorchid()
