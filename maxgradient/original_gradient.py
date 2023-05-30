# Ignore this file. It is a copy of the original gradient.py file from the maxgradient package.
"""Defines the Gradient class which is used to print text with a gradient. It inherits from the Rich Text class."""
import re
from io import StringIO
from time import sleep
from typing import Any, Dict, List, Optional, Tuple

from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich.columns import Columns
from rich.console import Console, JustifyMethod, OverflowMethod, RenderableType
from rich.control import strip_control_codes
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Span, Text
from rich.traceback import install as install_rich_traceback
from snoop import spy

from examples.color import Color, ColorParseError
from maxgradient.color_list import ColorList
from maxgradient.theme import GradientTheme

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX = re.compile(r"^\s+$")
VERBOSE: bool = False


console = Console(theme=GradientTheme())
install_rich_traceback(console=console)


class Gradient(Text):
    """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to empty string.
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. If `colors` has at least two parsable colors, `colors_start`\
                    and `end_color`'s arguments are ignored and those values are parsed from \
                        `colors`.Defaults to []
            rainbow(`bool`): Whether to print the gradient text in rainbow colors across \
                the spectrum. Defaults to False.
            invert(`bool): Reverse the color gradient. Defaults to False.
            hues(`int`): The number of colors in the gradient. Defaults to `3`.
            color_sample(`bool`): Whether to print the gradient on identically colored background. \
                This makes the gradient's text invisible, but it useful for printing gradient \
                samples. Defaults to False.
            style(`StyleType`) The style of the gradient text. Defaults to None.
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center", "full", \
                "right". Defaults to None.
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.
            end (str, optional): Character to end text with. Defaults to "\\\\n".
            no_wrap (bool, optional): Disable text wrapping, or None for default. Defaults to None.
            tab_size (int): Number of spaces per tab, or `None` to use `console.tab_size`.\
                Defaults to 8.
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.
            verbose(`bool`): Whether to print verbose output. Defaults to False.
    """

    __slots__ = [
        "_colors",
        "invert",
        "color_sample",
        "hues",
        "_G_INDEX",
        "_G_LENGTH",
        "_REMAINDER",
        "verbose",
    ]

    def __init__(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: Optional[Style | str] = None,
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,
        verbose: bool = VERBOSE,
    ) -> None:
        # Ignore gradients if the text is empty or only whitespaces.
        if isinstance(text, str):
            text = text.strip()
        elif isinstance(text, Text):
            text = text.plain.strip()
        elif text is None:
            text = ""
        match = WHITESPACE_REGEX.match(text)
        if match:
            text = Text.from_markup(match.group(0))
            return

        # Parse Text
        if isinstance(text, Text):
            spans = text._spans
            text = text.plain
        self.style = style

        # Initialize Text
        super().__init__(
            text=text,  #        #   self._text: List[str]
            style=style,  #  type: ignore    #   self.style: StyleType
            justify=justify,  #  #   self.justify: Optional[JustifyMethod]
            overflow=overflow,  ##   self.overflow: Optional[OverflowMethod]
            no_wrap=no_wrap,  #  #   self.no_wrap: Optional[bool]
            end=end,  #          #   self.end: str
            tab_size=tab_size,  ##   self.tab_size: Optional[int]
            spans=spans,  #      #   self._spans: Optional[List[Span]]
        )

        # text
        sanitized_text = strip_control_codes(text)
        self._length = len(sanitized_text)

        # invert
        self.invert = invert

        # Color Sample
        self.color_sample = color_sample
        if self.color_sample:
            self._text = "█" * self._length

        # hues
        if hues is not None:
            self.hues = hues
        else:
            self.hues = 3

        # colors
        self._colors: List[Color] = []
        if not rainbow:
            if colors is None:
                color_list = ColorList(self.hues, self.invert)
                self._colors = color_list.color_list
            else:
                for color in colors:
                    try:
                        parsed_color = Color(color)  # type: ignore
                        self._colors.append(parsed_color)
                    except:
                        print(f"Unable to parse color: {color}")
            self.hues = len(self._colors)

        else:
            self.hues = 10
            color_list = ColorList(self.hues, self.invert)
            self._colors = color_list.color_list

        # ensure that the gradient renderable is sufficiently long\
        # to display the gradient correctly.
        self.clamp_colors()
        self._spans = self.generate_spans(verbose=False)

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"<Gradient {self._text!r} {self._spans!r}>"

    def calculate_G_LENGTH(self, verbose: bool = VERBOSE) -> Tuple[int, int]:
        """Calculate the length of the gradient.

        Args:
            verbose(`bool`): Whether to print verbose output. Defaults to False.

        Returns:
            Tuple[int, int]: the length of the gradient as well as the integer remainder.
        """
        TEXT_LEN = self._length
        if verbose:
            console.log(f"Text Length: [bold #0ff]{TEXT_LEN}[/]")

        GRADIENTS = self.hues - 1
        if verbose:
            console.log(f"Number of Gradients: [bold #0ff]{GRADIENTS}[/]")

        self._G_LENGTH = TEXT_LEN // GRADIENTS  # floor (int) division
        self._REMAINDER = TEXT_LEN % GRADIENTS  # division remainder
        if verbose:
            console.log(f"Gradient Length: [bold #0ff]{self._G_LENGTH}[/]")
            console.log(f"Gradient Remainder: [bold dim #ff0]{self._REMAINDER}[/]")
        return self._G_LENGTH, self._REMAINDER

    def calculate_gradient_start(self) -> int:
        """Calculate the start index of the given gradient."""
        return self._G_INDEX * self._G_LENGTH

    def calculate_gradient_end(self, start: int) -> int:
        """Calculate the end index of the given gradient.

        Args:
            start(`int`): The start index of the gradient.
        """
        end = start + self._G_LENGTH
        if self._REMAINDER is not None:
            if self._G_INDEX < self._REMAINDER:
                end += 1
            if self._G_INDEX == self._REMAINDER:
                end = self._length
        return end

    def get_substring(self, start: int, end: int) -> str:
        """Return a substring of the given text.

        Args:
            start(`int`): The start index of the substring.
            end(`int`): The end index of the substring.

        Returns:
            str: The indicated substring.

        Raises:
            IndexError: If the start index is less than `0` or greater than the length of the text.
            IndexError: If the end index is less than `0` or greater than the length of the text.
            IndexError: If the end index is greater than the length of the text.
            ValueError: If the start index is greater than the end index.
        """
        TEXT = "".join(self._text)
        assert start >= 0, IndexError(
            f"Invalid Start Index: ({start}) Valid values must be greater than or equal to `0`."
        )
        assert end >= 0, IndexError(
            f"Invalid End Index: ({end}) Valid values must be greater than or equal to `0`."
        )
        assert end <= len(TEXT), IndexError(
            f"Invalid End Index: ({end}) Valid values range from  `0` to the length of the text ({self._length})."
        )
        assert start < end, ValueError(
            f"Invalid indexes: The start index ({start}) must be less than the end index ({end})."
        )
        return TEXT[start:end]

    def generate_spans(self, verbose: bool = False) -> List[Span]:
        """Generate tuples with the enumerated tuple of start and end index of each span"""
        if verbose:
            _console = Console(theme=GradientTheme())
            install_rich_traceback(console=_console)

        spans: List[Span] = []
        span_start = 0
        GRADIENTS: int = len(self._colors) - 1
        self._G_LENGTH, self._REMAINDER = self.calculate_G_LENGTH()

        # Loop through each gradient & generate the start and end indexes
        for self._G_INDEX in range(GRADIENTS):
            gradient_start = self.calculate_gradient_start()
            gradient_end = self.calculate_gradient_end(gradient_start)

            if self._G_INDEX < GRADIENTS:
                color1 = self._colors[self._G_INDEX]
                r1, g1, b1 = color1.rgb_tuple
                color2 = self._colors[self._G_INDEX + 1]
                r2, g2, b2 = color2.rgb_tuple
                dr = r2 - r1
                dg = g2 - g1
                db = b2 - b1
                if verbose:
                    self.log_deltas(color1, color2, gradient_start, gradient_end)

            span_start = 0
            for span_index in range(self._G_LENGTH):
                blend = span_index / self._G_LENGTH  # floating point division
                span_start = gradient_start + span_index
                span_color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"  # type: ignore
                span_style = self.generate_span_style(span_color)
                current_span = Span(span_start, span_start + 1, span_style)
                spans.append(current_span)
                if verbose:
                    _console.log(current_span)  # type: ignore
        return spans

    def clamp_colors(self) -> None:
        """Limit the number of colors (`self._colors`) in a gradient to at most one color per two characters.
        This function is used to treat edge cases where the color count exceeds that
        limit causing the last several characters in the message to be the same color
        or have no color at all."""
        length = len("".join(self._text))
        hues = len(self._colors)
        if hues > length // 2:
            self._colors = self._colors[::2]

    def generate_span_style(self, color: Color | str) -> Style:  # type: ignore
        """Generate a style with the specified color."""
        if isinstance(color, str):
            color = Color(color)
        if self.style is None or self.style == "_null":
            self.style = Style(color=color)  # type: ignore
            return self.style
        if not isinstance(color, Color):
            color = Color(color)
        if isinstance(self.style, str):
            self.style = Style.parse(self.style)
        elif isinstance(self.style, Style):
            style_def = str(self.style)
            self.style = Style.parse(f"{style_def} {str(color)}")
            return self.style
        else:
            raise TypeError(
                f"Unable to combine style (`{self.style}`) and color (`{color})`)"
            )

    def log_deltas(
        self, color1: Color, color2: Color, gradient_start: int, gradient_end: int
    ) -> None:
        """Log the deltas between each color in a gradient.

        Args:
            color1(`Color`): The first color in the gradient.
            color2(`Color`): The second color in the gradient.
            gradient_start(`int`): The start index of the gradient.
            gradient_end(`int`): The end index of the gradient.
        """

        # Initialize table instance
        gradient_table = Table(show_header=False, expand=False)

        # Columns
        gradient_table.add_column("Attributes", justify="left", style="bold cyan")
        gradient_table.add_column("Values", justify="left", style="bold italic magenta")
        gradient_table.add_column("Description", justify="left", style="dim white")

        # Rows
        gradient_table.add_row(
            "Gradient Index",
            f"{self._G_INDEX}",
            "The index of the gradient.",
        )
        gradient_table.add_row(
            "Gradient Start",
            f"{gradient_start}",
            "The start index of the gradient.",
        )
        gradient_table.add_row(
            "Gradient End",
            f"{gradient_end}",
            "The end index of the gradient.",
        )
        gradient_table.add_row(
            "Color 1",
            f"[bold {color1.hex}]{color1}[/]",
            "The first color of the gradient.",
        )
        gradient_table.add_row(
            "Color 2",
            f"[bold {color2.hex}]{color2}[/]",
            "The second color of the gradient.",
        )
        console.log(gradient_table)

    # End of Gradient Class


def _color(plural: bool = True, capital: bool = False) -> Gradient:
    """The word `color` in a random gradient."""
    if plural:
        word = "colors"
    else:
        word = "color"
    if capital:
        word = word.capitalize()
    return Gradient(word)


# @snoop
def gradient_examples_table(console: Console = Console(theme=GradientTheme())) -> Table:  # type: ignore
    """Generate several examples of gradients.

    Args:
        console(`Console`): The console instance to use for rendering.

    Returns:
        `List[Layout]`: A list of Layout instances.
    """

    console.line(3)
    console.rule(title=Gradient("Gradient Examples"))
    console.line(2)


def format_value(variable: str) -> Text:
    """Format a variable.

    Args:
        variable(`str`): The variable to format.

    Returns:
        `Text`: The formatted variable.
    """
    # Boolean Variables
    if variable == "True" or variable == "False":
        style = "bold #5f00ff"
        if variable == "True":
            return Text("True", style=style)
        return Text("False", style=style)

    # Attempt to parse `variable` as a color
    try:
        color = Color(variable)
        return Text(f'"{variable}"', style=f"bold {color.hex}")

    # Format `variable`` as a string
    except ColorParseError as cpe:
        return Text(f'"{variable}"', style="#E0E781")
    except ValueError as ve:
        return Text(f'"{variable}"', style="#E0E781")
    except TypeError as te:
        return Text(f'"{variable}"', style="#E0E781")
    except Exception as e:
        return Text(f'"{variable}"', style="#E0E781")


def format_list(list: List[str]) -> Text:
    """Format a list of strings.

    Args:
        list(`List[str]`): The list to format.

    Returns:
        `Text`: The formatted list.
    """
    formatted_list = [Text("[", style="bold #ffbbff")]
    COMMA = Text(", ", style="#cccccc")
    num_of_items = len(list)

    for index, item in enumerate(list, start=1):
        formatted_list.append(format_value(item))
        if index < num_of_items:
            formatted_list.append(COMMA)
    formatted_list.append(Text("]", style="bold #ffbbff"))
    return Text.assemble(*formatted_list)


def assignment(var: Optional[str] = "color") -> Text:
    """Generate a formatted variable and its assignment operator.

    Args:
        var(`Optional[str]`): The variable name.

    Returns:
        `Text`: The formatted variable and its assignment operator.
    """
    return Text.assemble(
        Text(var, style="italic #ff8800"),  # type: ignore
        Text(" = ", style="#FF0066"),
    )


def generate_subtitle(var: Optional[str] = "color", attr: List[str] = []) -> Text:
    """Automate the generation of a subtitle for a gradient example.

    Args:
        attributes (str | List[str]): The Gradient attributes to emphasize.
        variable (Optional[str], optional): The variable of the emphasized attributes. Defaults to "color".

    Returns:
        Text: The formatted and colored subtitle
    """
    # Format the variable
    key = assignment(var)  # The variable and its assignment operator

    # Format the attribute(s)
    if len(attr) > 1:  # Multiple attributes
        value = format_list(attr)

    elif len(attr) == 1:  # Single attribute
        value = format_value(attr[0])

    return Text.assemble(key, value)  # type: ignore


def gradient_examples_table() -> Table:
    """Generate several examples of gradients.

    Returns:
        Table: A table containing several examples of gradients.
    """
    TEXT = lorem.paragraphs(2)
    example_table = Table.grid("col_1", "col_2", padding=(1, 4), expand=True)

    RedYellow: List[str] = ["red", "orange", "yellow"]
    subtitle_RedYellow = generate_subtitle("color", RedYellow)

    example_table.add_row(
        Panel(  # Panel 1 - Row 1 - Random Gradient
            Gradient(TEXT),
            title=Gradient("Random Gradient"),
            subtitle=Text(
                f"A random color gradient is used when no colors are specified.",
                style="italic dim white",
            ),
            padding=(1, 4),
            expand=True,
        ),
        Panel(  # Panel 2 - Row 1 - Red-orange-yellow Gradient
            Gradient(TEXT, colors=["red", "orange", "yellow"]),
            title=Gradient("Three Color Gradient"),
            subtitle=subtitle_RedYellow,
            padding=(1, 4),
            expand=True,
        ),
    )

    # X11 Colors
    x11_colors: List[str] = ["darkgreen", "green", "deepskyblue", "indigo"]
    subtitle_x11 = generate_subtitle("colors", x11_colors)

    # HEX Colors
    hex_colors: List[str] = ["#f0f", "#af00ff", "#5f00ff"]
    subtitle_hex = generate_subtitle("colors", hex_colors)

    example_table.add_row(
        Panel(
            Gradient(TEXT, colors=x11_colors),  # type: ignore
            title=Gradient("X11 Colors", colors=x11_colors),  # type: ignore
            subtitle=subtitle_x11,
            padding=(1, 4),
            expand=True,
        ),
        Panel(
            Gradient(TEXT, colors=hex_colors),  # type: ignore
            title=Gradient("HEX Colors", colors=hex_colors),  # type: ignore
            subtitle=subtitle_hex,
            padding=(1, 4),
            expand=True,
        ),
    )

    # RGB Colors
    rgb_colors: List[str] = ["rgb(0,0,255)", "rgb(0,136,255)", "rgb(0,255,255)"]
    subtitle_rainbow = generate_subtitle("rainbow", ["True"])

    example_table.add_row(
        Panel(
            Gradient(TEXT, colors=rgb_colors),  # type: ignore
            title=Gradient("RGB Color Codes", colors=rgb_colors),  # type: ignore
            subtitle=generate_subtitle("colors", rgb_colors),
            padding=(1, 4),
            expand=True,
        ),
        Panel(
            Gradient(TEXT, rainbow=True),
            title=Gradient("Rainbow Gradient", rainbow=True),
            subtitle=subtitle_rainbow,
            padding=(1, 4),
            expand=True,
        ),
    )
    return example_table


def explanation_1() -> Layout:  # type: ignore
    console = Console(theme=GradientTheme())
    console.clear()
    console.line(2)
    examples_preface = "Gradients can be made in a number of types:"
    random_example = "\n[bold lightblue]- [/bold lightblue]\
[lime]1)[/] [bold white]When [/]\
[#ff0000]no[/#ff0000]\
[bold white] colors are specified, the text will have a [/]\
[italic bold #00ffff]random gradient[/italic bold #00ffff]\
[bold white] applied to it[/]."
    named_example = "\n[bold lightblue]- [/]\
[lime]2)[/] [bold white]When a list of color is provided, \
The gradient will be generated from those.\n The vibrant spectrum \
of colors that Gradient uses are:\n\n[/bold white]"
    x11_example = "\n\n[bold lightblue]- [/]\
[#00FF00]3)[/] [bold] \
[#FFFFFF]Colors can also be parsed from X11 keywords such as:[/]\
[#006400] `darkgreen`[/#006400],\
[#008000] `green`[/#008000], \
[#00BFFF]`deepskyblue`[/#00BFFF],\
[bold #ffffff] or [/bold #ffffff]\
[#4B0082] `indigo`[/#4B0082].[/bold]"
    hex_example = "\n[bold lightblue]- [/]\
[lime]4)[/] [bold] [white]Gradient may also be parsed \
from [italic #00ffff]3[/] or [italic #00ffff]6[/] \
digit hex color codes such as:[/]\
[bold #ff00ff] `#f0f`[/],\
[bold #af00ff] `af00ff`[/],\
[bold #ffffff] or [/]\
[bold #5f00ff]`#5f00ff`[/].[/bold]"
    rgb_example = "\n[bold lightblue]- [/]\
[lime]5)[/] [bold white]RGB Color code can be parsed from strings \
[bold #0000ff]`rgb(0, 0, 255)`[/] \
[bold white]or [/bold white]\
[bold #0088ff]`(0,136,255)`[/],\
or from tuples [#00ffff](0,255,255)[/]:"
    console.print(examples_preface, justify="center")
    console.print(random_example, justify="center")
    explanations = [named_example, x11_example, hex_example, rgb_example]
    for count in range(4):
        console.print(explanations[count], justify="center")
        if count == 0:
            colors = [Color(color) for color in Color.COLORS]
            console.print(Columns(colors, equal=True, expand=False), justify="center")


register_repr(Panel)(normal_repr)

if __name__ == "__main__":
    console = Console(theme=GradientTheme())
    # explanation_1()
    console.print(gradient_examples_table(), justify="center")
