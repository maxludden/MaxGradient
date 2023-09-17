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

def console_gradient_example() -> None:
    """Print an example of a gradient."""
    console = Console(width=70, record=True)
    console.line()
    console.gradient(
        "   This is by far the simplest way to print gradient colored       text to the console.",
        colors = [
            "red",
            "orange",
            "yellow",
            "green"
        ],
        justify = "center",
        style = "bold"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/console_gradient_example.svg",
        title="Console Gradient Example",
        theme=GradientTerminalTheme(),
    )

def console_gradient_rule_thin() -> None:
    """Print an example of a thin gradient rule."""
    console = Console(width=80, record=True)
    console.line()
    console.gradient_rule(
        "[bold]Thin Gradient Rule[/]",
        thickness="thin"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/console_gradient_rule_thin.svg",
        title="Console Gradient Rule Thin",
        theme=GradientTerminalTheme(),
    )

def console_gradient_rule_medium() -> None:
    """Print an example of a thin gradient rule."""
    console = Console(width=80, record=True)
    console.line()
    console.gradient_rule(
        "[bold]Medium Gradient Rule[/]",
        thickness="medium"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/console_gradient_rule_medium.svg",
        title="Console Gradient Rule Medium",
        theme=GradientTerminalTheme(),
    )

def console_gradient_rule_thick() -> None:
    """Print an example of a thick gradient rule."""
    console = Console(width=80, record=True)
    console.line()
    console.gradient_rule(
        "[bold]Thick Gradient Rule[/]",
        thickness="thick"
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/console_gradient_rule_thick.svg",
        title="Console Gradient Rule Thick",
        theme=GradientTerminalTheme(),
    )

if __name__ == "__main__":
    # console_print()
    console_gradient_example()
    console_gradient_rule_thin()
    console_gradient_rule_medium()
    console_gradient_rule_thick()
