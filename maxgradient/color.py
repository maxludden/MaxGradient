"""Module for parsing colors from strings."""
# pylint: disable=C0209,E0401,W0611, C0103
import colorsys
import re
from typing import Any, Tuple, List

from rich.box import SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError
from rich.color_triplet import ColorTriplet
from rich.columns import Columns
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback
from snoop import snoop
from cheap_repr import register_repr, normal_repr

from maxgradient._rich import Rich
from maxgradient._x11 import X11
from maxgradient._mode import Mode
from maxgradient.log import log, get_console
from maxgradient.theme import GradientTheme

console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
install_rich_traceback(console=console)

x11 = X11()
rich = Rich()

register_repr(Table)(normal_repr)
register_repr(Columns)(normal_repr)
register_repr(Text)(normal_repr)
register_repr(Style)(normal_repr)
register_repr(ColorTriplet)(normal_repr)
register_repr(Mode)(normal_repr)




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
            `original` (str): The original color string.\n\t
            `name` (str): The name of the color. The string\
                to parse to easily create a color.\n\t
            `value` (RichColor): The color value.\n\t
            `mode` (Mode): The color mode.\n\t
            `rgb` (str): The RGB string.\n\t
            `rgb_tuple` (Tuple[int, int, int]): The RGB string as a tuple of integers.\n\t
            `hex` (str): The hex string.\n\t
            `style` (str): A style with the color as the foreground.\n\t
            `bg_style` (str): A readable style with the color as the background.\n\t


    ---

        For an example of possible colors enter the following in a terminal:
        \t`python -m maxgradient.color.`
    """

    _name: str
    _value: RichColor
    _mode: Mode
    NAMED: Tuple[str, ...] = (
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
        "#0000fe",
        "#0088ff",
        "#00ffff",
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
        "rgb(0, 136, 255)",
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

    def __init__(self, color: Any) -> None:
        """A color to make gradients with."""
        self.original = str(color)
        self.name = str(color)
        log.debug(f"Parsing color: {self.original}")

        if isinstance(color, Color):
            log.debug("Color is a Color object.")
            self.name = color.name
            self.value = color.value
            self.mode = Mode.COLOR
            return
        if isinstance(color, str):
            log.debug("Color is a string.")
            # Named
            for group in (self.NAMED, self.HEX, self.RGB, self.RGB_TUPLE):
                if color in group:
                    log.debug(f"Color is a named color: {group} {color}")
                    index = group.index(color)
                    rgb_tuple = self.RGB_TUPLE[index]
                    triplet = ColorTriplet(*rgb_tuple)
                    self.value = RichColor.from_triplet(triplet)
                    self.name = self.NAMED[index]
                    self.mode = Mode.NAMED
                    return

            rich_color: Tuple[int, int, int] = Rich().get_color(color)
            if rich_color:
                log.debug(f"Color is a rich color: {rich_color}")
                index = Rich().get_rgb().index("rgb({0},{1},{2})".format(*rich_color))
                self.name = Rich().NAMES[index]
                triplet = ColorTriplet(*rich_color)
                self.value = RichColor.from_triplet(triplet)
                self.mode = Mode.RICH
                return

            # X11
            x11_color: Tuple[int, int, int] = X11().get_color(color)
            if x11_color:
                log.debug(f"Color is an X11 color: {x11_color}")
                index = X11().get_rgb().index("rgb({0},{1},{2})".format(*x11_color))
                self.name = X11().NAMES[index]
                triplet = ColorTriplet(*x11_color)
                self.value = RichColor.from_triplet(triplet)
                self.mode = Mode.X11
                return

            # Hex
            hex_match = re.match(r"^#\?([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$", color)
            if hex_match:
                log.debug(f"Color is a hex color: {hex_match.group(0)}")
                hex_color = hex_match.group(1)
                if len(hex_color) == 3:
                    hex_color = "".join([c * 2 for c in group])
                rgb = self.hex_to_rgb(hex_color)
                rgb_tuple = self.rgb_to_tuple(rgb)
                triplet = ColorTriplet(*rgb_tuple)
                self.value = RichColor.from_triplet(triplet)
                self.name = color
                self.mode = Mode.HEX
                return

            # RGB
            rgb_match = re.match(r"r?g?b?\((\d{1,3}), (\d{1,3}), (\d{1,3})\)", color)
            if rgb_match:
                log.debug(f"Color is an RGB color: {rgb_match.groups()}")
                rgb_tuple = self.rgb_to_tuple(color)
                triplet = ColorTriplet(*rgb_tuple)
                self.value = RichColor.from_triplet(triplet)
                self.name = color
                self.mode = Mode.RGB
                return

        # RGB Tuple
        if isinstance(color, tuple):
            log.debug(f"Color is an RGB tuple: {color}")
            assert len(color) == 3
            for count, num in enumerate(color):
                assert (
                    0 <= num <= 255
                ), f"RGB values must be between 0 and 255. Invalid number: {count}"
            triplet = ColorTriplet(*color)
            self.value = RichColor.from_triplet(triplet)
            self.name = str(color)
            self.mode = Mode.RGB_TUPLE
            return

        raise ColorParseError(f"Invalid color: {color}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        repr_str = f"Color<{str(self._original).capitalize()}>"
        log.debug(f"Getting repr for {self.name}: {repr_str}")
        return repr_str

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
            caption="\n\n",
        )
        table.add_column(
            "attribute", style=f"bold on {self.bg_style}", justify="center"
        )
        table.add_column(
            "value", style=f"bold {self.style} on #000000", justify="center"
        )
        original = str(self._original).capitalize()
        table.add_row("Original", original)
        mode = self.mode
        table.add_row("Mode", mode)
        hex_str = str(self.hex).upper()
        table.add_row("HEX", hex_str)
        rgb_str = self.rgb
        table.add_row("RGB", rgb_str)
        rgb_tuple = self.rgb_tuple
        tuple_str = str(rgb_tuple)
        table.add_row("RGB Tuple", tuple_str)
        return table

    # Properties
    @property
    def original(self) -> str:
        """Return the original color."""
        return self._original

    @original.setter
    def original(self, original: str) -> None:
        """Set the original color."""
        assert isinstance(
            original, (str, Tuple, Color)
        ), f"Invalid original: {original}"
        self._original = original

    # Properties
    @property
    def value(self) -> RichColor:
        """Return the color value."""
        return self._value

    @value.setter
    def value(self, color: RichColor) -> None:
        """Set the color value."""
        assert isinstance(color, RichColor), f"Invalid value: {color}"
        log.debug(f"Setting Color-{str(color)}'s value: {color}")
        self._value = color

    @property
    def name(self) -> str:
        """Return the color name."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the color name."""
        assert isinstance(name, str), f"Invalid name: {name}"
        log.debug(f"Setting Color-{name}'s name: {name}")
        self._name = name

    @property
    def color_name(self) -> str:
        """Return the color name formatted in the color."""
        name = self.name
        style = f"bold {self.hex}"
        color_name = f"[{style}]{name}[/{style}]"
        log.debug(f"Getting Color-{self.name}'s color name: {color_name}")
        return color_name

    @property
    def mode(self) -> Mode:
        """Return the color mode."""
        log.debug(f"Getting Color-{self.name}'s mode: {self._mode}")
        return self._mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        """Set the color mode."""
        assert isinstance(mode, Mode), f"Invalid mode: {mode}"
        log.debug(f"Setting Color<{self.name}>'s mode: {mode}")
        self._mode = mode

    # Format Properties
    @property
    def hex(self) -> str:
        """Return the color as a hex string."""
        hex_color = self.value.triplet.hex
        log.debug(f"Getting Color-{self.name}'s as hex: {hex_color}")
        return hex_color

    @property
    def rgb(self) -> str:
        """Return the color as a RGB string."""
        rgb_color = self.value.triplet.rgb
        log.debug(f"Getting Color-{self.name}'s as RGB: {rgb_color}")
        return rgb_color

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """Return the color as a RGB tuple."""
        rgb = self.value.triplet.rgb
        rgb_matches = re.findall(r"\d{1,3}", rgb)
        if rgb_matches:
            rgb_tuple = tuple([int(num) for num in rgb_matches])
        log.debug(f"Getting Color-{self.name}'s as RGB Tuple: {rgb_tuple}")
        return rgb_tuple

    @property
    def style(self) -> Style:
        """Get the color as a style."""
        style = Style(color=self.hex)
        log.debug(f"Getting Color-{self.name}'s as Style: {style}")
        return style

    @property
    def bg_style(self) -> Style:
        """Get the color as a background style."""
        foreground = self.get_contrast()
        style = Style(color=foreground, bgcolor=self.hex)
        log.debug(f"Getting Color-{self.name}'s as Background Style: {style}")
        return style

    def as_title(self) -> Text:
        """Return the rich representation of a color."""
        LESS = "[bold #ffffff]<[/]"
        GREATER = "[bold #ffffff]>[/]"
        C1 = "[bold #ff0000]C[/]"
        O1 = "[bold #ff8800]o[/]"
        L1 = "[bold #ffff00]l[/]"
        O2 = "[bold #00ff00]o[/]"
        R1 = "[bold #00ffff]r[/]"
        style = self.style
        NAME = f"[bold italic {style}]{str(self._original).capitalize()}[/]"
        colors = [C1, O1, L1, O2, R1, LESS, NAME, GREATER]
        markup = "".join(colors)
        return Text.from_markup(markup)

    @staticmethod
    def rgb_to_hex(rgb_str: str) -> str:
        """Convert a RGB string to a hex string."""
        rgb_match = re.match(r"^rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)$", rgb_str)
        if rgb_match:
            rgb_matches = rgb_match.groups()
            hex_code = "".join([f"{int(num):02x}" for num in rgb_matches])
            hex_code = f"#{hex_code}"
            return hex_code

    @staticmethod
    def hex_to_rgb(hex_input: str) -> str:
        """Convert a hex color to an RGB string."""
        if hex_input.startswith("#"):
            hex_code = hex.lstrip("#")

        if len(hex_code) == 3:
            hex_code = "".join([c * 2 for c in hex_code])

        red = int(hex_code[0:2], 16)
        green = int(hex_code[2:4], 16)
        blue = int(hex_code[4:6], 16)

        return f"rgb({red}, {green}, {blue})"

    @staticmethod
    def rgb_to_tuple(rgb_str: str) -> Tuple[int, int, int]:
        """Convert a RGB string to an RGB tuple."""
        rgb_match = re.match(r"^rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)$", rgb_str)
        if rgb_match:
            return tuple(int(c) for c in rgb_match.groups())
        return (0, 0, 0)

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

    @classmethod
    def named_table(cls) -> Columns:
        """Return a table of named colors."""
        log.debug("Generating named color table.")
        colors = []
        for color in cls.NAMED:
            colors.append(Color(color))
        return Columns(colors, equal=True)

    @classmethod
    def library_tables(cls) -> Columns:
        """Return a table of library colors."""
        log.debug("Generating library color table.")
        rich_table = Table(Rich.color_table())
        x11_table = Table(X11.color_table())
        # return Columns([rich_table, x11_table], equal=True)
        console.print(rich_table)
        console.print(x11_table)

    # @staticmethod
    # def color_title() -> Text:
    #     """Generate a colored text title."""
    #     _rich = Text("Rich ", style=Style(color="#5f00ff", bold=True))
    #     _and = Text(" & ", style=Style(color="#af00ff", bold=True))
    #     _x11 = Text("X11 ", style=Style(color="#ff00ff", bold=True))
    #     letter_c = Text("C", style=Style(color="#ff0000", bold=True))
    #     letter_o = Text("o", style=Style(color="#ff8800", bold=True))
    #     letter_l = Text("l", style=Style(color="#ffff00", bold=True))
    #     letter_o2 = Text("o", style=Style(color="#00ff00", bold=True))
    #     letter_r = Text("r", style=Style(color="#00ffff", bold=True))
    #     letter_s = Text("s", style=Style(color="#0088ff", bold=True))
    #     title = [_rich, _and, _x11, letter_c, letter_o, letter_l, letter_o2, letter_r, letter_s]
    #     return Text.assemble(*title)

    @classmethod
    def color_table(cls) -> Columns:
        """Return a table of all colors."""
        tables: List[Table] = []
        for colors in [Rich, X11]:
            log.debug("Generating color table.")
            title = colors.get_title()
            table = Table(title=title, show_header=True, header_style="bold.magenta")
            table.add_column("Example", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Hex", justify="center")
            table.add_column("RGB", justify="center")
            table.add_column("RGB Tuple", justify="center")


            def add_row(
                color: Color,
                table: Table = table,
                end_section: bool = False) -> Table:
                block = Text("█" * 12, style=f"bold {color.hex}")
                name = Text(color.name, style=f"bold {color.hex}")
                hex_color = Text(color.hex, style=f" bold {color.hex}")
                rgb_color = Text(color.rgb, style=f" bold {color.hex}")
                rgb_tuple = Text(str(color.rgb_tuple), style=f" bold {color.hex}")
                table.add_row(block, name, hex_color, rgb_color, rgb_tuple)
                if end_section:
                    table.add_section()
                return table

            for color in colors.NAMES:
                table = add_row(cls(color), table)
            tables.append(table)

        return Columns(tables, equal=True)


if __name__ == "__main__":
    console = get_console()
    console.print(Color.named_table(), justify="center")
    console.print(Color.color_table(), justify="center")
