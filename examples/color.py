from maxgradient.console import Console
from maxgradient.color import Color
from maxgradient.theme import GradientTerminalTheme

def color_red() -> None:
    """Print the color red"""
    console = Console(width=80, record=True)
    console.line()
    console.print(
        Color("red"),
        justify="center"
    )
    console.line(2)
    console.save_html(
        "docs/img/color_red.html",
        theme=GradientTerminalTheme(),
    )

def color_aaffaa() -> None:
    """Print the color #aaffaa"""
    console=Console(width=80, record=True)
    console.line()
    console.print(
        Color("#aaffaa"),
        justify="center"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/color_aaffaa.svg",
        title="Color #AAFFAA",
        theme=GradientTerminalTheme(),
    )

def color_darkorchid() -> None:
    """Print the X11 color DarkOrchid"""
    console=Console(width=80, record=True)
    console.line()
    console.print(
        Color("DarkOrchid"),
        justify="center"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/color_darkorchid.svg",
        title="Color DarkOrchid",
        theme=GradientTerminalTheme(),
    )
    

if __name__ == "__main__":
    color_red()
    color_aaffaa()
    color_darkorchid()