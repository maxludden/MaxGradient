"""MaxGradient.main"""
from typing import Iterable

from lorem_text import lorem
from rich.columns import Columns
from rich.console import Group, NewLine
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.rule import GradientRule

TEXT = "Lorem nulla consequat enim adipisicing excepteur nostrud pariatur est. \
Cillum do commodo occaecat voluptate laborum sint labore cupidatat. Labore \
labore incididunt ex irure officia id consectetur do deserunt non culpa \
deserunt ipsum quis. Est qui exercitation magna. Minim est adipisicing elit \
incididunt ullamco consequat. Aliquip velit est aliquip officia consequat \
minim do ea tempor ex incididunt dolor laborum. Enim nulla anim fugiat."


def gen_random_group() -> Group:
    """Generate the syntax for a random gradient and the result."""

    def syntax() -> Syntax:
        """Generate the syntax for a random gradient."""
        code = Syntax(
            f"""import maxgradient as mg

TEXT = "{TEXT}"

console = mg.Console()

console.print(
    mg.Gradient(TEXT)
)""",
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            # background_color="#222222",
            padding=(1, 2),
        )
        code.stylize_range("italic #83DDF0", (5,13), (5,20)) # Console
        code.stylize_range("#50FA7B", (7,8), (7,13)) # print
        code.stylize_range("italic #83DDF0", (8,7), (8,15)) # Gradient
        return code

    def gradient() -> Gradient:
        """Generate a random gradient."""
        return Gradient(TEXT)

    return Group(syntax(), NewLine(), GradientRule("Results as"), NewLine(), gradient())


def gen_rainbow_group() -> Group:
    """Generate the syntax for a rainbow gradient and the result."""

    def explination() -> Text:
        """Generate the explination for a rainbow gradient."""
        text = [
            Text(
                "That's not the simplest way to do it though... The ", style="#ffffff"
            ),
            Text("Console", style="bold #83DDF0"),
            Text(" object has a `", style="#ffffff"),
            Text("gradient", style="italic #50FA7B"),
            Text(
                "` classmethod to automate creating a gradient with all of \
the available options present in the `",
                style="#ffffff",
            ),
            Text("Gradient", style="bold #83DDF0"),
            Text("` class.", style="#ffffff"),
            Text("\n\nIn the following example we'll use the ", style="#ffffff"),
            Text("rainbow", style="bold #FFB86C"),
            Text(" keyword argument to create a rainbow gradient.", style="#ffffff"),
            Text("\n\nNote: that in this example we are also using the ", style="i #aaaaaa"),
            Text("style", style="italic bold #FFB86C"),
            Text(" keyword argument to make the gradient bold.", style="i #aaaaaa"),
        ]
        return Text.assemble(*text)

    def syntax() -> Syntax:
        """Generate the syntax for a rainbow gradient."""
        code = """console = mg.Console()
console.gradient(TEXT, rainbow=True, style="bold")"""
        code = Syntax(
            code,
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            # background_color="#222222",
            padding=(1, 2),
            start_line=10,
        )
        code.stylize_range("italic #83DDF0", (1,13), (1,20)) # Console
        code.stylize_range("#50FA7B", (2,7), (2,16)) # gradient

        return code

    def gradient() -> Gradient:
        """Generate a rainbow gradient."""
        return Gradient(TEXT, rainbow=True, style="bold")

    return Group(
        explination(),
        NewLine(),
        syntax(),
        NewLine(),
        GradientRule("Results as"),
        NewLine(),
        gradient(),
    )

def gen_red_orange_yellow_group() -> Group:
    """Generate the syntax for a red, orange, yellow gradient and the result."""

    def explination() -> Text:
        """Generate the explination for a red, orange, yellow gradient."""
        text = [
            Text(
                "You're not just stuck to creating random or rainbow gradients.\
 If you would like more control of the gradient, simply pass the Gradient object \
the ", style="#ffffff"),
            Text("colors", style="bold #FFB86C"),
            Text(" keyword argument with a list of colors you would like to use.", style="#ffffff")
        ]
        return Text.assemble(*text)

    def syntax() -> Syntax:
        """Generate the syntax for a red, orange, yellow gradient."""
        code = Syntax("""console = mg.Console()

console.print(
    mg.Gradient(
        TEXT,
        colors=["red", "orange", "yellow"],
        style="bold italic",
    )
)""",
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            start_line=12)
        code.stylize_range("italic #83DDF0", (1,13), (1,20)) # Console
        code.stylize_range("#50FA7B", (3,7), (3,13)) # print
        code.stylize_range("italic #83DDF0", (4,7), (4,15)) # Gradient
        return code

    def gradient() -> Gradient:
        """Generate a red, orange, yellow gradient."""
        return Gradient(
            TEXT,
            colors=["red", "orange", "yellow"],
            style="bold italic",
        )
    
    return Group(
        explination(),
        NewLine(),
        syntax(),
        NewLine(),
        GradientRule("Results as"),
        NewLine(), 
        gradient()
    )
    
def gen_cool_group() -> Group:
    """Generate the syntax for a cool gradient and the result."""
    def explination() -> Text:
        """Generate the explination for a cool gradient."""
        return Text(
                "You can also use any valid X11 color name, hex code, or rgb value \
to create a gradient. In the following example we'll use a combination of all three \
to create a cool gradient.", style="#ffffff")

    def syntax() -> Syntax:
        """Generate the syntax for a cool gradient."""
        code = Syntax(
            """console = mg.Console()

console.print(
    mg.Gradient(
        TEXT,
        colors=[
            "#00ffff",
            "#0088ff",
            "rgb(0,0,255)",
            "#5f00ff",
            "#af00ff",
            "magenta"
        ],
        style="underline",
        justify='default'
    )
)""",
            "python",
            theme="dracula",
            line_numbers=True,
            indent_guides=False,
            word_wrap=True,
            padding=(1, 2),
        )
        code.stylize_range("italic #83DDF0", (1,13), (1,20)) # Console
        code.stylize_range("#50FA7B", (3,7), (3,16)) # print
        code.stylize_range("italic #83DDF0", (4,7), (4,15)) # Gradient
        return code

    def gradient() -> Gradient:
        """Generate a cool gradient."""
        return Gradient(
            TEXT,
            colors=["#00ffff", "#0088ff", "rgb(0,0,255)", "#5f00ff", "#af00ff", "magenta"],
            style="underline",
            justify='default'
        )

    return Group(
        explination(),
        NewLine(),
        syntax(),
        NewLine(),
        GradientRule("Results as"),
        NewLine(),
        gradient(),
    )

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
    c_red = "[bold #ff0000]Red[/]"
    orange = "[#ff8800]orange[/]"
    c_orange = "[bold #ff8800]Orange[/]"
    yellow = "[#ffff00]yellow[/]"
    c_yellow = "[bold #ffff00]Yellow[/]"
    c_rainbow = "[#D59A5A]rainbow[/]"
    c_colors = "[#D59A5A]colors[/]"

    # Random Gradient
    yield Panel(
        gen_random_group(),
        title=Gradient("Random Gradient", style="bold"),
        padding=(2, 4),
        width=80,
    )

    # Rainbow Gradient
    yield Panel(
        gen_rainbow_group(),
        title=Gradient("Rainbow Gradient", rainbow=True, style="bold"),
        padding=(2, 4),
#         subtitle=f"{c_gradient}{r_para}{c_text}{comma} \
# {c_rainbow}{equal}{c_true}{l_para}",
#         subtitle_align="right",
        width=80,
    )

    # Red, Orange, Yellow Gradient
    gradient_short = Gradient(TEXT, colors=["red", "orange", "yellow"])
    sub_1_1 = f"{c_gradient}{r_para}{c_text}{comma}"
    sub_1_2 = f"{c_colors}{equal}{l_brac}\
{red}{comma}{orange}{comma}{yellow}{r_brac}{l_para}"
    short_subtitle = f"{sub_1_1}{sub_1_2}"
    yield Panel(
        gen_red_orange_yellow_group(),
        title=f"{c_red}, {c_orange}, [#888]and[/] {c_yellow} [b]Gradient[/]",
        padding=(2, 4),
        # subtitle=short_subtitle,
        # subtitle_align="right",
        width=80,
    )

    # Magenta, Violet, Purple, Blue, Lightblue, Cyan Gradient
    gradient_long = Gradient(
        TEXT, colors=["magenta", "violet", "purple", "blue", "lightblue", "cyan"]
    )
    sub_2_1 = f"{c_gradient}{r_para}{c_text}{comma}"
    sub_2_2 = f"{c_colors}{equal}{l_brac}"
    sub_2_3 = f"{magenta}{comma}{violet}{comma}{purple}\n{comma}"
    sub_2_4 = f"{blue}{comma}{lightblue}{comma}{cyan}{r_brac}{l_para}"
    long_subtitle = f"{sub_2_1}{sub_2_2}{sub_2_3}{sub_2_4}"
    yield Panel(
        gen_cool_group(),
        title=f"{c_magenta}{c_violet}{c_purple}{c_blue}{c_lightblue}\
[#888]and[/] {c_cyan} [b]Gradient[/]",
        padding=(2, 4),
        width=80,
    )


def main() -> None:
    """Run the main function."""

    console = Console(record=True)
    console.line(2)
    console.gradient_rule("[b]Gradient Color Examples[/]")
    console.line(2)
    console.print(
        Columns(generate_panels(), padding=(2, 8), equal=True), justify="center"
    )
    console.line()
    console.save_max_svg(
        "docs/img/main_examples.svg",
        title="MaxGradient Examples",
    )


if __name__ == "__main__":
    main()
