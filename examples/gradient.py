"""MaxGradient.gradient.Gradient()"""
# pylint: disable=E0402, E0401
from lorem_text import lorem

from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTerminalTheme

TEXT = lorem.paragraphs(2)

def gradient_hello() -> None:
    """Gradient Hello, World!"""
    console = Console(width=40)
    console.line(2)
    console.gradient("Hello, World!", justify="center") # Uses the gradient function of console
    console.line(2)
    console.save_max_svg(
        "Images/hello_world.svg",
        title="`Hello, World!` Result",
        theme=GradientTerminalTheme(),
    )

def gradient_cool() -> None:
    """Print a cool gradient."""
    console = Console(width=40)
    console.line(2)
    console.gradient("Gradients are cool!", justify="center")
    console.line(2)
    console.save_max_svg(
        "Images/random_gradient.svg",
        title="`Random Gradient!` Result"
    )


def gradient_string_colors() -> None:
    """Create a gradient from strings of color names."""
    console = Console(width=55, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from strings!",
            colors=[
                "red", # Popular color name
                "green",
                "blue"]
        ),
        justify="center",
    )
    console.line(2)

    console.save_max_svg(
        "Images/string_color_gradient.svg",
        title="`String Color Gradient`! Result"
    )


def gradient_hex_colors() -> None:
    """Create a gradient from hex color codes."""
    console = Console(width=55, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from Hex colors codes!",
            colors=[
                "#ff0000", # Six digit hex
                "#f80", # Three digit hex
                "ff0"   # Three digit hex without the hash
            ]
        ),
        justify="center",
    )
    console.line(2)

    console.save_max_svg(
        "Images/hex_colors_gradient.svg",
        title="`Hex Colors Gradient`! Result"
    )

def gradient_rgb_colors() -> None:
    """Create a gradient from rgb color codes and color tuples."""
    console = Console(width=55, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from RGB color codes!",
            colors=[
                "rgb(255, 0, 0)", # RGB color code
                (255, 128, 0), # RGB color tuple
                "rgb(255, 255, 0)" # RGB color code
        )