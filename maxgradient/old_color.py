"""Purpose: Color class to parse colors for a gradient."""

import colorsys
import re
from collections.abc import 
from typing import Optional, Tuple

from loguru import logger
from rich.box import SQUARE
from rich.style import Style
from rich.color import Color as RichColor
from rich.color import ColorParseError
from rich.color_triplet import ColorTriplet
from rich.columns import Columns
from rich.console import Console, RenderResult
from rich.highlighter import ReprHighlighter
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback
from snoop import snoop
from cheap_repr import register_repr, normal_repr

from maxgradient._rich import RICH, RICHHEX, RICHRGB, get_rich_color, rich_table
from maxgradient._x11 import X11, X11HEX, X11RGB, get_x11_color, x11_table
from maxgradient.log import Log
from maxgradient.theme import GradientTheme
from maxgradient._abstract_color import Mode

ColorType = str | Tuple[int, int, int] | RichColor

register_repr(RichColor)(normal_repr)
register_repr(ColorTriplet)(normal_repr)
register_repr(Table)(normal_repr)

HEX_REGEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_REGEX = re.compile(r"^r?g?b?\((\d{1,3}),\s?(\d{1,3}),\s?(\d{1,3})\)$")
console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
install_rich_traceback(console=console)
log = Log(console)


class Color:
    """A color parsed from a string. Colors can be parsed from:
        - The Named Colors:
            - `magenta`
            - `violet`
            - `purple`
            - `blue`
            - `lightblue`
            - `cyan`
            - `lime`
            - `yellow`
            - `orange`
            - `red`

        - Hex Colors:
            - Six digit hex color codes - `#ff00ff`
            - Three digit hex color codes - `#0f0`

        - RGB Colors:
            - `rgb(255, 0, 255)`

        - X11 colors:
            - `magenta`,
            - 'deepskyblue'

        - Or any of the `rich` library's standard colors:
            - `skyblue1`,
            - `bright_red`

        Attributes:\n\t
            `value` (RichColor): The color value.\n\t
            `mode` (Mode): The color mode.\n\t
            `rgb` (str): The RGB string.\n\t
            `rgb_tuple` (Tuple[int, int, int]): The RGB string as a tuple of integers.\n\t
            `hex` (str): The hex string.\n\t
            `style` (str): A style with the color as the foreground.\n\t
            `bg_style` (str): A readable style with the color as the background.\n\t


    ---

        For an example of possible colors enter the following in a terminal:
        \t`python -m gradient.color.`
    """

    # def __new__(cls, color: RichColor|str|Tuple[int,int,int]) -> "Color": # type: ignore
    #     """Create a new color instance from a str(Named Color, hex color code, rgb string),
    #         tuple, or RichColor."""
    #     return super(Color, cls).__new__(cls, color) # type: ignore

    
    def __init__(self, color: RichColor | str | Tuple[int, int, int]) -> None:
        """A color parsed from a string.

        Args:
            color (str): A color string. Can be a named color, hex color,
                rgb color, x11 color, or rich color.

        Raises:
            ColorParseError: If the color cannot be parsed.
        """
        self._original = color

        # Parse the color
        ## Named colors
        if color in self.COLORS:
            index = self.COLORS.index(color)
            rgb = self.RGB[index]
            rgb_tuple = self.rgb_to_tuple(rgb)
            triplet = ColorTriplet(*rgb_tuple)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.NAMED
            return

        ## Color
        elif isinstance(color, Color):
            self.value = color.value
            self.mode = color.mode
            return

        ## RGB Tuple colors
        elif isinstance(color, Tuple):
            red, green, blue = tuple(color)
            assert isinstance(red, int)
            assert isinstance(green, int)
            assert isinstance(blue, int)
            red = int(red)
            green = int(green)
            blue = int(blue)
            assert red >= 0 and red <= 255
            assert green >= 0 and green <= 255
            assert blue >= 0 and blue <= 255
            triplet = ColorTriplet(red, green, blue)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.RGB
            return

        ## X11 colors
        elif get_x11_color(color):
            rgb = str(get_x11_color(color))
            rgb_tuple = self.rgb_to_tuple(rgb)
            triplet = ColorTriplet(*rgb_tuple)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.X11
            return

        ## Rich colors
        elif get_rich_color(color):
            rgb = str(get_rich_color(color))
            rgb_tuple = self.rgb_to_tuple(rgb)
            triplet = ColorTriplet(*rgb_tuple)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.RICH
            return

        ## Hex colors
        elif HEX_REGEX.match(str(color)):
            rgb = self.hex_to_rgb(color)
            rgb_tuple = self.rgb_to_tuple(rgb)
            triplet = ColorTriplet(*rgb_tuple)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.HEX
            return

        ## RGB colors
        elif RGB_REGEX.match(str(color)):
            rgb_tuple = self.rgb_to_tuple(color)
            triplet = ColorTriplet(*rgb_tuple)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.RGB
            return

        else:
            raise ColorParseError(f"Invalid color: {color}")

    @property
    
    def value(self) -> RichColor:
        """Return the color value."""
        return self._value

    @value.setter
    def value(self, value: RichColor) -> None:
        """Set the color value."""
        self._value = value

    @property
    def name(self) -> str:
        """Return the color name."""
        string = self._original
        if self.mode == Mode.NAMED:
            if string in self.COLORS:
                index = self.COLORS.index(string)
            elif string in self.RGB:
                index = self.RGB.index(string)
            elif string in self.RGB_TUPLE:
                index = self.RGB_TUPLE.index(string)
            elif string in self.HEX:
                index = self.HEX.index(string)
            name = self.COLORS[index]
        elif self.mode == Mode.X11:
            if string in X11:
                index = X11.index(string)
            elif string in X11RGB:
                index = X11RGB.index(string)
            elif string in X11HEX:
                index = X11HEX.index(string)
            name = X11[index]
        elif self.mode == Mode.RICH:
            if string in RICH:
                index = RICH.index(string)
            elif string in RICHRGB:
                index = RICHRGB.index(string)
            elif string in RICHHEX:
                index = RICHHEX.index(string)
            name = RICH[index]
        elif self.mode == Mode.HEX:
            name = string
        elif self.mode == Mode.RGB:
            name = self.rgb
        log.debug(f"Getting name for {name}: {name}")
        return name

    @property
    
    def rgb(self) -> Optional[str]:
        """Return the RGB string."""
        rgb = self.value.triplet.rgb
        log.debug(f"Getting rgb for {self.name}: {rgb}")
        return rgb

    @property
    
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """Return the RGB string as a tuple of integers."""
        triplet = self.value.triplet
        red = triplet.red
        green = triplet.green
        blue = triplet.blue
        rgb_tuple = (red, green, blue)
        log.log(f"Getting rgb_tuple for {self.name}: {rgb_tuple}")
        return rgb_tuple

    @property
    
    def hex(self) -> str:
        """Return the hex string."""
        hex = self.value.triplet.hex
        log.debug(f"Getting hex for {self.name}: {hex}")
        return hex

    @property
    
    def style(self) -> Style:
        """Generate a style with the color as the foreground."""
        style = Style(color=self.value, bgcolor="default")
        log.debug(f"Getting style for {self.name}: {style}")
        return style

    @property
    
    def bg_style(self) -> str:
        """Generate a readable style with the color as the background."""
        foreground = self.get_contrast()
        bg_style = f"{foreground} on {self.hex}"
        log.debug(f"Getting bg_style for {self.name}: {bg_style}")
        return bg_style

    COLORS: Tuple[str, ...] = (
        "magenta",
        "violet",
        "purple",
        "blue",
        "lightblue",
        "cyan",
        "lime",
        "yellow",
        "orange",
        "red",
    )
    HEX: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#0088ff",
        "#0fffff",
        "#00ff00",
        "#ffff00",
        "#ff8800",
        "#ff0000",
    )
    RGB: Tuple[str, ...] = (
        "rgb(255, 0, 255)",
        "rgb(175, 0, 255)",
        "rgb(95, 0, 255)",
        "rgb(0, 0, 255)",
        "rgb(0,136,255)",
        "rgb(0, 255, 255)",
        "rgb(0, 255, 0)",
        "rgb(255, 255, 0)",
        "rgb(255, 136, 0)",
        "rgb(255, 0, 0)",
    )
    RGB_TUPLE: Tuple[Tuple[int, int, int], ...] = (
        (255, 0, 255),
        (175, 0, 255),
        (95, 0, 255),
        (0, 0, 255),
        (0, 136, 255),
        (0, 255, 255),
        (0, 255, 0),
        (255, 255, 0),
        (255, 136, 0),
        (255, 0, 0),
    )

    def __repr__(self) -> str:
        repr = f"Color<{str(self._original).capitalize()}>"
        log.debug(f"Getting repr for {self.name}: {repr}")
        return repr

    def __str__(self) -> str:
        string = str(self._original)
        log.debug(f"Getting string for {self.name}: {string}")
        return string

    
    def __rich__(self) -> Table:
        """Return the rich console representation of a color."""
        table = Table(
            title=self.as_title(),
            show_header=False,
            box=SQUARE,
            border_style=f"bold {self.style}",
            expand=False,
            width=40,
            collapse_padding=True,
            caption="\n\n"
        )
        table.add_column(
            "attribute", style=f"bold on {self.bg_style}", justify="center"
        )
        table.add_column(
            "value", style=f"bold {self.style} on #000000", justify="center"
        )
        table.add_row("Original", str(self._original).capitalize())
        table.add_row("Mode", self.mode)
        table.add_row("HEX", str(self.hex).upper())
        table.add_row("RGB", self.rgb)
        return table

    @staticmethod
    
    def rgb_to_tuple(rgb_string: str) -> Tuple[int, int, int]:
        """Get the color as a tuple of integers.

        Args:
            rgb_string (str): The RGB string to convert.

        Returns:
            tuple: The RGB string as a tuple of integers.

        Raises:
            ValueError: If the RGB string is invalid.
        """
        log.debug("Entered rgb_to_tuple()")
        if isinstance(rgb_string, tuple):
            rgb_string = f"rgb({rgb_string[0]}, {rgb_string[1]}, {rgb_string[2]})"
        RGB_REGEX = re.compile(r"r?g?b?\((\d+),\s*(\d+),\s*(\d+)\)")
        match = RGB_REGEX.match(rgb_string)
        if match:
            red = match.group(1)
            green = match.group(2)
            blue = match.group(3)
            rgb_tuple = (int(red), int(green), int(blue))
            log.debug(f"Converting {rgb_string} to tuple: {rgb_tuple}")
            return rgb_tuple
        else:
            raise ValueError("Invalid RGB string format")

    @staticmethod
    
    def tuple_to_triplet(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert a tuple of integers to a triplet.

        Args:
            rgb (tuple): The tuple of integers.

        Returns:
            tuple: The triplet.
        """
        triplet = ColorTriplet(rgb[0], rgb[1], rgb[2])
        log.debug(f"Converting {rgb} to triplet: {triplet}")
        return triplet

    
    def as_title(self) -> Text:
        """Return the rich representation of a color."""
        LESS = f"[bold #ffffff]<[/]"
        GREATER = f"[bold #ffffff]>[/]"
        C1 = f"[bold #ff0000]C[/]"
        O1 = f"[bold #ff8800]o[/]"
        L1 = f"[bold #ffff00]l[/]"
        O2 = f"[bold #00ff00]o[/]"
        R1 = f"[bold #00ffff]r[/]"
        style = self.style
        NAME = f"[bold italic {style}]{str(self._original).capitalize()}[/]"
        colors = [C1, O1, L1, O2, R1, LESS, NAME, GREATER]
        markup = "".join(colors)
        return Text.from_markup(markup)

    
    def get_contrast(self) -> str:
        """Generate a foreground color for the color style.

        Returns:
            str: The foreground color.
        """
        log.debug(f"Getting contrast for {self.name}")

        def rgb_to_hsv(rgb_color: Tuple[int, int, int]):
            """Convert an RGB color to HSV."""
            r, g, b = rgb_color
            log.debug(f"Converting {rgb_color} to HSV")
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            log.debug(f"HSV: {h}, {s}, {v}")
            return h, s, v

        def color_distance(rgb_color1, rgb_color2):
            """Calculate the distance between two colors."""
            h1, s1, v1 = rgb_to_hsv(rgb_color1)
            h2, s2, v2 = rgb_to_hsv(rgb_color2)
            dh = min(abs(h1 - h2), 1 - abs(h1 - h2))
            ds = abs(s1 - s2)
            dv = abs(v1 - v2)
            color_distance = dh + ds + dv
            log.debug(
                f"Color distance between {rgb_color1} and {rgb_color2}: {color_distance}"
            )
            return color_distance

        def find_closest_color(rgb_color, color_list):
            """Calculate the closest color in a list."""
            closest_color = None
            min_distance = float("inf")
            for color in color_list:
                distance = color_distance(rgb_color, color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color
            log.debug(f"{rgb_color} is closer to {closest_color}.")
            return closest_color

        closest = find_closest_color(self.rgb_tuple, [(0, 0, 0), (255, 255, 255)])
        if closest == (0, 0, 0):
            return "#ffffff"
        else:
            return "#000000"

    @staticmethod
    
    def hex_to_rgb(hex: str) -> str:
        hex_code = hex.lstrip("#")

        if len(hex_code) == 3:
            hex_code = "".join([c * 2 for c in hex_code])

        red = int(hex_code[0:2], 16)
        green = int(hex_code[2:4], 16)
        blue = int(hex_code[4:6], 16)

        return f"rgb({red}, {green}, {blue})"

    @staticmethod
    
    def hex_to_rgb_tuple(hex: str) -> str:
        """Convert a hex color to an RGB tuple."""
        hex = hex.lstrip("#")  # Remove the '#' symbol if present

        # Extract individual color components
        red = int(hex[0:2], 16)
        green = int(hex[2:4], 16)
        blue = int(hex[4:6], 16)

        # Return the RGB tuple
        rgb_tuple = (red, green, blue)
        log.debug(f"Converted Hex Color ({hex}) to RGB Tuple: {rgb_tuple}")
        return rgb_tuple


def named_table() -> Columns:
    """Return a table of named colors."""
    log.debug("Generating named color table.")
    colors = []
    for color in Color.COLORS:
        colors.append(Color(color))
    return Columns(colors, equal=True)


def library_tables() -> Columns:
    """Return a table of library colors."""
    log.debug("Generating library color table.")
    rich_table = Table(_rich.rich_table())  # type: ignore
    x11_table = Table(_x11.x11_table())  # type: ignore
    return Columns([rich_table, x11_table], equal=True)



class Tint:
    """The grayscale of Color."""

    NAMES: Tuple[str, ...] = (
        "white",
        "lightgrey"
        "grey",
        "darkgrey",
        "black"
    )

    HEX: Tuple[str, ...] = (
        "#ffffff",
        "#cccccc",
        "#888888",
        "#444444",
        "#000000"
    )

    RGB: Tuple[str, ...] = (
        'rgb(255, 255, 255)',
        'rgb(204, 204, 204)',
        'rgb(136, 136, 136)',
        'rgb(68, 68, 68)',
        'rgb(0, 0, 0)'
    )

    RGB_TUPLE: Tuple[Tuple[int, int, int], ...] = (
        (255, 255, 255),
        (204, 204, 204),
        (136, 136, 136),
        (68, 68, 68),
        (0, 0, 0)
    )

    def __init__(self, tint: "Color"|str|Tuple[int,int,int]) -> None:
        super().__init__(
            color=tint
        )



if __name__ == "__main__":
    from rich.console import Console
    from rich.traceback import install as install_rich_traceback

    import maxgradient._rich as _rich
    import maxgradient._x11 as _x11
    from maxgradient.theme import GradientTheme

    console = Console(theme=GradientTheme())
    install_rich_traceback(console=console)

    console.line()
    named = "[bold][red]Na[/][orange]m[/][yellow]e[/][lime]d[/]"
    colors = "[cyan]C[/][lightblue]o[/][blue]l[/][purple]o[/][violet]r[/][magenta]s[/]"
    named_color_title = f"{named} {colors}"
    console.print(named_color_title, justify="center")
    console.line()
    console.print(named_table(), justify="center")
    console.line(2)

    table = Table.grid(padding=10, expand=True)
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_row(_rich.rich_table(), _x11.x11_table())
    console.print(table, justify="center")
