from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTerminalTheme

def console_print() -> None:
    """Console Hello, World!"""
    console = Console(width=70, record=True)
    console.line()
    console.print("\t[bold #00ff00]Hello, World![/]")  # Uses the gradient function of console
    console.line(2)
    console.save_max_svg(
        "docs/img/console_print.svg",
        title="Console Print Result",
        theme=GradientTerminalTheme(),
    )

if __name__ == "__main__":
    console_print()