"""MaxGradient.gradient.Gradient()"""
# pylint: disable=E0402, E0401
from lorem_text import lorem
from rich.console import Group, NewLine
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from maxgradient.console import GradientConsole
from maxgradient.gradient import Gradient
from maxgradient.rule import GradientRule
from maxgradient.theme import GradientTerminalTheme

TEXT = lorem.paragraphs(2)


def gradient_hello() -> None:
    """Gradient Hello, World!"""
    console = GradientConsole(width=70, record=True)
    console.line()
    console.gradient(
        "Hello, World!", justify="center"
    )  # Uses the gradient function of console
    console.line(2)
    console.save_svg(
        "docs/img/hello_world.svg",
        title="Quick Start Example Result",
        theme=GradientTerminalTheme(),
    )


def gradient_with_color_1() -> None:
    """Print a gradient with color."""
    console = GradientConsole(width=70, record=True)
    console.line()
    console.gradient(
        "This gradient contains the colors: magenta, violet, and purple.",
        colors=["magenta", "violet", "purple"],
        justify="center",
    )
    console.line(2)
    console.save_svg(
        "docs/img/gradient_with_color_1.svg",
        title="Example 1 Result",
        theme=GradientTerminalTheme(),
    )


def gradient_with_color_2() -> None:
    """Print a gradient with color."""
    console = GradientConsole(width=80, record=True)
    console.line()
    console.gradient(
        "\tThis gradient contains the colors: violet, purple, blue, lightblue, and cyan.",
        colors=["violet", "purple", "blue", "lightblue", "cyan"],
        justify="center",
        style="bold",
    )
    console.line(2)
    console.save_svg(
        "docs/img/gradient_with_color_2.svg",
        title="Example 2 Result",
        theme=GradientTerminalTheme(),
    )


def gradient_cool() -> None:
    """Print a cool gradient."""
    console = GradientConsole(width=40, record=True)
    console.line()
    console.gradient("\tGradients are cool!", justify="center")
    console.line(2)
    console.save_svg("docs/img/gradient_are_cool.svg", title="Random Gradient Result")


def gradient_string_colors() -> None:
    """Create a gradient from strings of color names."""
    console = GradientConsole(width=65, record=True)
    console.line(2)
    console.print(
        Gradient(
            "Creating gradients from strings!",
            colors=["red", "green", "blue"],  # Popular color name
        ),
        justify="center",
    )
    console.line(2)

    console.save_svg(
        "docs/img/string_color_gradient.svg", title="`String Color Gradient`! Result"
    )


def gradient_hex_colors() -> None:
    """Create a gradient from hex color codes."""
    console = GradientConsole(width=65, record=True)
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

    console.save_svg(
        "docs/img/hex_colors_gradient.svg", title="`Hex Colors Gradient` Result"
    )


def gradient_rgb_colors() -> None:
    """Create a gradient from rgb color codes and color tuples."""
    console = GradientConsole(width=65, record=True)
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
    console.save_svg("docs/img/rgb_gradient.svg", title="RGB Color Gradient Result")


def gradient_random_panel() -> Panel:  # type: ignore
    """Generate the syntax for a random gradient and the result."""

    def group() -> Group:
        TEXT = lorem.paragraph()

        def syntax() -> Syntax:
            """Generate the syntax for a random gradient."""
            code = Syntax(
                f"""import maxgradient as mg

console = mg.Console()

console.print(
    mg.Gradient({lorem.paragraphs(2)}),
)""",
                "python",
                theme="dracula",
                line_numbers=True,
                indent_guides=False,
                word_wrap=True,
                padding=(1, 2),
            )
            code.stylize_range("italic #83DDF0", (5, 13), (5, 20))  # Console
            code.stylize_range("#50FA7B", (7, 8), (7, 13))  # print
            code.stylize_range("italic #83DDF0", (8, 7), (8, 15))  # Gradient
            return code

        def gradient() -> Gradient:
            """Generate a random gradient."""
            return Gradient(TEXT)

        return Group(
            syntax(), NewLine(), GradientRule("Results as"), NewLine(), gradient()
        )

    console = GradientConsole(width=80, record=True)
    console.line()
    console.print(Panel(group(), title=Gradient("Random Gradient"), padding=(2, 4)))
    console.line(2)
    console.save_svg(
        "docs/img/random_gradient.svg",
        title="Random Gradient Result",
        theme=GradientTerminalTheme(),
    )


def random_gradient_example() -> None:
    """Generate the syntax for a random gradient and the result."""

    def group() -> Group:
        TEXT1 = "It's incredibly easy to create a gradient! All it requires is a string. Given a string, the gradient will randomly generate colors for you automatically."
        TEXT2 = "Or even easier... just use the Console's gradient function. It's the same thing!"

        def syntax() -> Syntax:
            """Generate the syntax for a random gradient."""
            code = Syntax(
                f"""import maxgradient as mg

console = mg.Console()
console.print(
    Gradient(
        "{TEXT1}"
    )
)

console.gradient(
    "{TEXT2}"
)
""",
                "python",
                theme="dracula",
                line_numbers=True,
                indent_guides=False,
                word_wrap=True,
                padding=(1, 2),
            )
            code.stylize_range("italic #83DDF0", (3, 13), (3, 20))  # Console
            code.stylize_range("#50FA7B", (4, 8), (4, 13))  # print
            code.stylize_range("italic #83DDF0", (5, 4), (5, 12))  # Gradient
            code.stylize_range("#B58CEF", (6, 13), (9, 20))  # Console
            code.stylize_range("#50FA7B", (10, 8), (10, 16))  # gradient
            return code

        def gradient() -> Group:
            """Generate a random gradient."""
            return Group(Gradient(TEXT1), NewLine(), Gradient(TEXT2))

        return Group(
            syntax(), NewLine(), GradientRule("Results as"), NewLine(), gradient()
        )

    console = GradientConsole(width=80, record=True)
    console.line()
    console.print(Panel(group(), title=Gradient("Random Gradient"), padding=(2, 4)))
    console.line(2)
    console.save_svg(
        "docs/img/random_gradient.svg", title="", theme=GradientTerminalTheme()
    )


def rainbow_gradient_example() -> None:
    """Generate a rainbow gradient example."""

    def explination() -> Text:
        """Generate the explination text."""
        text = [
            Gradient("Rainbow Gradients ", rainbow=True, style="bold"),
            Text("are not particularly difficult to create. Just ", style="#fff"),
            Text("set the ", style="#fff"),
            Text("rainbow ", style="#FFB86C"),
            Text("parameter to ", style="#fff"),
            Text("True", style="#BD93F9"),
            Text(", and that's it! The ", style="#fff"),
            Text("Gradient ", style="#86E1F5"),
            Text("class will take care of the rest.", style="#fff"),
        ]
        return Text.assemble(*text)

    def syntax() -> Syntax:
        """Generate the syntax for a rainbow gradient."""
        code = Syntax(
            """console.print(
    Gradient(
        "If a random gradient isn't colorful enough for you, try a rainbow gradient!",
        rainbow=True,
        style="bold"
    ),
)""",
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            padding=(1, 2),
        )
        code.stylize_range("#50FA7B", (1, 8), (1, 13))  # print
        code.stylize_range("#86E1F5", (2, 4), (2, 12))  # Gradient
        code.stylize_range("#FFB86C", (4, 8), (4, 15))  # rainbow
        code.stylize_range("#BD93F9", (4, 16), (4, 20))  # True
        code.stylize_range("#FFB86C", (5, 8), (5, 13))  # style
        return code

    def gradient() -> Gradient:
        """Generate a rainbow gradient."""
        return Gradient(
            "If a random gradient isn't colorful enough for you, try a rainbow gradient!",
            rainbow=True,
            style="bold",
        )

    def group() -> Group:
        """Generate the syntax and gradient."""
        return Group(
            explination(),
            NewLine(),
            syntax(),
            NewLine(),
            GradientRule("Results as"),
            NewLine(),
            gradient(),
        )

    console = GradientConsole(width=80, record=True)
    console.line()
    console.print(
        Panel(group(), title=Gradient("Rainbow Gradient", rainbow=True), padding=(2, 4))
    )
    console.line(2)
    console.save_svg(
        "docs/img/rainbow_gradient.svg", title="", theme=GradientTerminalTheme()
    )


def red_orange_yellow_gradient() -> None:
    """Generate a red, orange, yellow gradient."""
    TEXT = lorem.paragraph()

    def explination() -> Text:
        """Generate the explination text."""
        text = [
            Text(
                "If you need a gradient with a specific set of colors, ", style="#fff"
            ),
            Text("create a gradient and pass it's ", style="#fff"),
            Text("colors ", style="#FFB86C"),
            Text("parameter a list of colors.", style="#fff"),
            Text("Colors may be of any type that the ", style="#fff"),
            Text("Color ", style="#86E1F5"),
            Text("class accepts.", style="#fff"),
        ]
        return Text.assemble(*text)

    def syntax() -> Syntax:
        """Generate the syntax for a red, orange, yellow gradient."""
        code = Syntax(
            f"""console.print(
    Gradient(
        "Lets create a gradient with the colors red, orange, and yellow. \\n\\n{TEXT}",
        colors=["red", "orange", "yellow"],
        justify="center"
    )
)""",
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            padding=(1, 2),
        )
        code.stylize_range("#50FA7B", (1, 8), (1, 13))  # print
        code.stylize_range("#86E1F5", (2, 4), (2, 12))  # Gradient
        code.stylize_range("#FF79C6", (2, 12), (2, 13))  # colors
        code.stylize_range("#FFB86C", (4, 8), (4, 14))  # colors
        code.stylize_range("#FFB86C", (5, 8), (5, 15))  # justify
        code.stylize_range("#FF79C6", (6, 0), (6, 13))  # colors
        return code

    def gradient() -> Gradient:
        """Generate a red, orange, yellow gradient."""
        return Gradient(
            f"Lets create a gradient with the colors red, orange, and yellow.\n\n{TEXT}",
            colors=["red", "orange", "yellow"],
            justify="center",
        )

    def group() -> Group:
        """Generate the syntax and gradient."""
        return Group(
            explination(),
            NewLine(),
            syntax(),
            NewLine(),
            GradientRule("Results as"),
            NewLine(),
            gradient(),
        )

    console = GradientConsole(width=80, record=True)
    console.line()
    panel = Panel(
        group(),
        title="[b #ff0000]Red[/], [b #ff8800]Orange[/], [b #ffff00]Yellow[/] [b #ffffff]Gradient[/]",
        padding=(2, 4),
    )
    console.print(panel)
    console.line(2)
    console.save_svg(
        "docs/img/red_orange_yellow_gradient.svg",
        title="",
        theme=GradientTerminalTheme(),
    )


if __name__ == "__main__":
    gradient_hello()
    gradient_with_color_1()
    gradient_with_color_2()
    gradient_cool()
    gradient_string_colors()
    gradient_hex_colors()
    gradient_rgb_colors()
    random_gradient_example()
    rainbow_gradient_example()
    red_orange_yellow_gradient()
