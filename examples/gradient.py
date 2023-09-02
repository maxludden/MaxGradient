"""MaxGradient.gradient.Gradient()"""
# pylint: disable=E0402, E0401
from lorem_text import lorem

from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTerminalTheme

TEXT = lorem.paragraphs(2)


def gradient_hello() -> None:
    """Gradient Hello, World!"""
    console = Console(width=70, record=True)
    console.line()
    console.gradient(
        "\tHello, World!", justify="center"
    )  # Uses the gradient function of console
    console.line(2)
    console.save_max_svg(
        "docs/img/hello_world.svg",
        title="Quick Start Example Result",
        theme=GradientTerminalTheme(),
    )


def gradient_with_color_1() -> None:
    """Print a gradient with color."""
    console = Console(width=70, record=True)
    console.line()
    console.gradient(
        "This gradient contains the colors: magenta, violet, and purple.",
        colors=["magenta", "violet", "purple"],
        justify="center",
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/gradient_with_color_1.svg",
        title="Example 1 Result",
        theme=GradientTerminalTheme(),
    )


def gradient_with_color_2() -> None:
    """Print a gradient with color."""
    console = Console(width=80, record=True)
    console.line()
    console.gradient(
        "\tThis gradient contains the colors: violet, purple, blue, lightblue, and \tcyan.",
        colors=["violet", "purple", "blue", "lightblue", "cyan"],
        justify="center",
    )
    console.line(2)
    console.save_max_svg(
        "docs/img/gradient_with_color_2.svg",
        title="Example 2",
        theme=GradientTerminalTheme(),
    )


def gradient_cool() -> None:
    """Print a cool gradient."""
    console = Console(width=40, record=True)
    console.line()
    console.gradient("\tGradients are cool!", justify="center")
    console.line(2)
    console.save_max_svg(
        "docs/img/gradient_are_cool.svg", title="Random Gradient Result"
    )


def gradient_string_colors() -> None:
    """Create a gradient from strings of color names."""
    console = Console(width=65, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from strings!",
            colors=["red", "green", "blue"],  # Popular color name
        ),
        justify="center",
    )
    console.line(2)

    console.save_max_svg(
        "docs/img/string_color_gradient.svg", title="`String Color Gradient`! Result"
    )


def gradient_hex_colors() -> None:
    """Create a gradient from hex color codes."""
    console = Console(width=65, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from Hex colors codes!",
            colors=[
                "#ff0000",  # Six digit hex
                "#f80",  # Three digit hex
                "ff0",  # Three digit hex without the hash
            ],
        ),
        justify="center",
    )
    console.line(2)

    console.save_max_svg(
        "docs/img/hex_colors_gradient.svg", title="`Hex Colors Gradient` Result"
    )


def gradient_rgb_colors() -> None:
    """Create a gradient from rgb color codes and color tuples."""
    console = Console(width=65, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from RGB color codes!",
            colors=[
                "rgb(255, 0, 0)",  # RGB color code
                (255, 128, 0),  # RGB color tuple
                "rgb(255, 255, 0)",  # RGB color code
            ],
        )
    )
    console.line(2)
    console.save_max_svg("docs/img/rgb_gradient.svg", title="RGB Color Gradient Result")

if __name__ == "__main__":
    gradient_hello()
    # gradient_with_color_1()
    # gradient_with_color_2()
    # gradient_cool()
    # gradient_string_colors()
    # gradient_hex_colors()
    # gradient_rgb_colors()
