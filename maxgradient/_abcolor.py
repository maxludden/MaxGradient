""""Generate a gradient of colors to print to the console."""
# pylint: disable=E0401,W0611,W0201
import colorsys
import re
from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from enum import Enum, auto
from typing import Tuple, Optional

from rich.box import SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError
from rich.color_triplet import ColorTriplet
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback

from maxgradient.log import Log
from maxgradient.theme import GradientTheme

console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
install_rich_traceback(console=console)
log = Log(console=console)


class Mode(Enum):
    """A color mode. Used to determine how a color was parsed."""
    COLOR = auto()
    NAMED = auto()
    X11 = auto()
    RICH = auto()
    HEX = auto()
    RGB = auto()
    RGB_TUPLE = auto()

    @property
    def color_mode(self) -> str:
        """Return the color mode."""
        if self.value == Mode.COLOR:
            return str("color")
        if self.value == Mode.NAMED:
            return str("named")
        elif self.value == Mode.X11:
            return str("x11")
        elif self.value == Mode.RICH:
            return str("rich")
        elif self.value == Mode.HEX:
            return str("hex")
        elif self.value == Mode.RGB:
            return str("rgb")
        elif self.value == Mode.RGB_TUPLE:
            return str("rgb_tuple")
        else:
            raise ValueError(f"Invalid mode: {self}")

    def __eq__(self, other: "Mode"|str) -> bool:
        """Return True if the color mode is equal to another."""
        if isinstance(other, Mode):
            return self.value == other.value
        elif isinstance(other, str):
            return self.color_mode == other
        else:
            return False

    def __repr__(self) -> str:
        """Return a representation of the color mode."""
        return f"Mode.{self.value.upper()}"

    def __rich_repr__(self) -> Text:
        """Return a rich text representation of the color mode."""
        mode = Text("Mode", style="bold italic white")
        dot = Text(".", style="bold.white")
        value: str = self.value.upper()
        formatted_value = Text(value, style="bold lime")
        rich_repr = Text.assemble(mode, dot, formatted_value)
        return rich_repr

    def __rich__(self) -> Text:
        """Return a rich text representation of the color mode."""
        return self.__rich_repr__()


RGB_REGEX = r"^rgb\((\d{1,3}),\s?(\d{1,3}),\s?(\d{1,3})\)$"
RGB_TUPLE_REGEX = r"^\((\d{1,3}),\s?(\d{1,3}),\s?(\d{1,3})\)$"


class ABColor(ABC):
    """An abstract base class for colors."""

    HEX_REGEX = re.compile(r"([0-9a-fA-F]{6})$")
    RGB_PATTERN = re.compile(RGB_REGEX)
    RGB_TUPLE_PATTERN = re.compile(RGB_TUPLE_REGEX)
    COLORS: Tuple[str, ...]
    HEX: Tuple[str, ...]
    RGB: Tuple[str, ...]
    RGB_TUPLE: Tuple[Tuple[int, int, int], ...]
    _original: str
    name: str
    value: RichColor

    @abstractmethod
    def __init__(self, abcolor: str | Tuple[int, int, int]) -> None:
        """Initialize an ABColor object."""

    @abstractmethod
    def as_title(self) -> Text:
        """Return the color name as a title."""

    @classmethod
    @abstractclassmethod
    def get_class(cls) -> str:
        """Return the class name."""

    def parse_named(
        self, color: "ABColor" | str | Tuple[int, int, int]
        ) -> Optional[Tuple[str, RichColor, Mode]]:
        """Parse a named color."""
        log.debug(f"Attempting to parse a named color: {color}")
        for group in (self.COLORS, self.HEX, self.RGB, self.RGB_TUPLE):
            if color in group:
                continue
            else:
                index = group.index(color)
                rgb_tuple = self.RGB_TUPLE[index]
                triplet = ColorTriplet(*rgb_tuple)
                color_name: str = color
                color_value: RichColor = RichColor.from_triplet(triplet)
                color_mode: Mode = Mode.NAMED
                result = (color_name, color_value, color_mode)
                log.debug(f"Successfully parsed named color: {result}")
                return



    def parse_color(self, color: "ABColor" | str | Tuple[int, int, int]) -> Tuple[str, RichColor, Mode]:
        """Parse a color."""
        log.debug(f"Attempting to parse an ABColor object: {color}")
        if isinstance(color, Color):
            self.name = color.name
            self.value = color.value
            self.color_mode = color.mode
            log.debug(f"Successfully parsed Color: {self}")
            return
        else:
            raise TypeError(f"parse_color() expected ABColor, got {type(color)}")

    def parse_hex(self, color: str) -> bool:
        """Parse a hex color."""
        log.debug(f"Attempting to parse Hex color: {color}")
        assert len(color) in [3, 4, 6, 7], f"Invalid hex color: {color}"
        if "#" in color:
            color = color.replace("#", "")
            if len(color) == 3:
                color = "".join([char * 2 for char in color])
        try:
            match = self.HEX_REGEX.match(color)
            if match:
                rgb_tuple = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
                log.debug(f"Parsed Hex colo ({color}): {rgb_tuple}")
                triplet = ColorTriplet(*rgb_tuple)
                self.name = color
                self.value = RichColor.from_triplet(triplet)
                self.mode = Mode.HEX
                log.debug(f"Successfully parsed Hex: {self}")
                return
        except ColorParseError as cpe:
            raise ColorParseError(f"Invalid hex color: {color}") from cpe

    def parse_rgb(self, color: str) -> bool:
        """Parse an RGB color."""
        log.debug(f"Attempting to parse RGB color: {color}")
        try:
            match = self.RGB_PATTERN.match(color)
            if match:
                rgb_tuple = tuple(int(x) for x in match.groups()[1:3])
                triplet = ColorTriplet(*rgb_tuple)
                self.name = color
                self.value = RichColor.from_triplet(triplet)
                self.mode = Mode.RGB
                log.debug(f"Successfully parsed RGB: {self}")
                return
        except ColorParseError as cpe:
            raise ColorParseError(f"Invalid rgb color: {color}") from cpe

    def parse_rgb_tuple(self, color: Tuple[int, int, int]) -> None:
        """Parse and RGB Tuple."""
        log.debug(f"Attempting to parse RGB Tuple: {color}")
        try:
            assert len(color) == 3
            assert [isinstance[color, int] for color in color]
            assert [0 <= x <= 255 for x in color]
            triplet = ColorTriplet(*color)
            self.name = str(color)
            self.value = RichColor.from_triplet(triplet)
            self.mode = Mode.RGB_TUPLE
            log.debug(f"Successfully parsed RGB Tuple: {self}")
            return
        except ColorParseError as cpe:
            raise ColorParseError(f"Invalid rgb tuple: {color}") from cpe

    @property
    def value(self) -> RichColor:
        """Return the color value."""
        log.debug(f"Getting color {self.name}'s value: {self._value}")
        return self._value

    @value.setter
    def value(self, value: RichColor) -> None:
        """Set the color value."""
        log.debug(f"Setting color {self.name}'s value: {value}")
        self._value = value

    @property
    def name(self) -> str:
        """Return the color name."""
        log.debug(f"Getting color {self.name}'s name: {self._name}")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Return the color name."""
        self._name = name
        log.debug(f"Setting color {self.name}'s name: {self._name}")

    @property
    def rgb(self) -> str:
        """Return the RGB value."""
        rgb = self.value.triplet.rgb
        log.debug(f"Getting color {self.name}'s rgb: {rgb}")
        return rgb

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """Return the RGB Tuple value."""
        triplet = self.value.triplet
        red = triplet.red
        green = triplet.green
        blue = triplet.blue
        rgb_tuple = (red, green, blue)
        log.log(f"Getting rgb_tuple for {self.name}: {rgb_tuple}")
        return rgb_tuple

    @property
    def hex(self) -> str:
        """Return the hex value."""
        hex_str = self.value.triplet.hex
        log.debug(f"Getting color {self.name}'s hex: {hex_str}")
        return hex_str

    @property
    def style(self) -> Style:
        """Return the color as a Style object."""
        style = Style(color=self.hex, bgcolor="default")
        log.debug(f"Getting color {self.name}'s Style: {style}")
        return style

    @property
    def bg_style(self) -> Style:
        """Return the color as a Style object."""
        fg_color = self.get_contrast_color()
        bg_style = Style(color=fg_color, bgcolor=self.value)
        log.debug(f"Getting color {self.name}'s bg_style: {bg_style}")
        return bg_style

    @staticmethod
    @abstractstaticmethod
    def hex_to_rgb(hex_str: str) -> str:
        """Convert a hex string to an RGB string."""
        log.debug(f"Converting Hex ({hex_str}) to RGB.")
        hex_code = hex_str.lstrip("#")

        if len(hex_code) == 3:
            hex_code = "".join([c * 2 for c in hex_code])
        red = int(hex_code[0:2], 16)
        green = int(hex_code[2:4], 16)
        blue = int(hex_code[4:6], 16)
        rgb = f"rgb({red}, {green}, {blue})"
        log.debug(f"Successfully converted Hex ({hex_str}) to RGB: {rgb}")
        return rgb

    @staticmethod
    def rgb_to_hex(rgb: str) -> str:
        """Convert an RGB string to a hex string."""
        log.debug(f"Converting RGB ({rgb}) to Hex.")
        components = re.findall(r"(\d+)", rgb)
        if components:
            rgb_tuple = tuple(int(x) for x in components.groups()[1:3])
            hex_str = ColorTriplet(*rgb_tuple).hex
            log.debug(f"Successfully converted RGB ({rgb}) to Hex: {hex_str}")
        return hex

    @staticmethod
    def rgb_to_rgb_tuple(rgb: str) -> Tuple[int, int, int]:
        """Convert an RGB string to an RGB Tuple."""
        log.debug(f"Converting RGB ({rgb}) to RGB Tuple.")
        components = re.findall(r"(\d+)", rgb)
        if components:
            rgb_tuple = tuple(int(x) for x in components.groups()[1:3])
            log.debug(f"Successfully converted RGB ({rgb}) to RGB Tuple: {rgb_tuple}")
        return rgb_tuple

    def get_contrast_color(self) -> str:
        """Generate a foreground color for the color style.

        Returns:
            str: The foreground color.
        """
        log.debug(f"Getting contrast for {self.name}")

        def rgb_to_hsv(rgb_color: Tuple[int, int, int]):
            """Convert an RGB color to HSV."""
            red, green, blue = rgb_color
            log.debug(f"Converting {rgb_color} to HSV")
            hue, saturation, value = colorsys.rgb_to_hsv(
                red / 255, green / 255, blue / 255
            )
            log.debug(f"HSV: {hue}, {saturation}, {value}")
            return hue, saturation, value

        def color_distance(rgb_color1, rgb_color2):
            """Calculate the distance between two colors."""
            hue1, saturation1, value1 = rgb_to_hsv(rgb_color1)
            hue2, saturation2, value2 = rgb_to_hsv(rgb_color2)
            delta_hue = min(abs(hue1 - hue2), 1 - abs(hue1 - hue2))
            delta_saturation = abs(saturation1 - saturation2)
            delta_value = abs(value1 - value2)
            color_distance = delta_hue + delta_saturation + delta_value
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

    def __str__(self) -> str:
        """Return the color name."""
        log.debug(f"Stringifying {self.name}: {self._name}")
        return self.name

    def __repr__(self) -> str:
        """Return the color name."""
        class_name = self.get_class()
        color_repr = f"{class_name.capitalize()}<{self._name}>"
        log.debug(f"Generated Repr: {color_repr}")
        return color_repr

    def __rich_repr__(self) -> str:
        """Return the color name."""
        class_name = self.get_class().capitalize()
        repr1 = f"[bold violet]{class_name}[/]"
        repr2 = "[bold dim white]<[/]"
        repr3 = f"[{self.hex}]{self._name}[/]"
        repr4 = "[bold dim white]>[/]"
        color_repr = "".join([repr1, repr2, repr3, repr4])
        log.debug(f"Generated Rich Repr: {color_repr}")
        return color_repr

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
        table.add_row("Original", str(self._original).capitalize())
        table.add_row("Mode", self.mode)
        table.add_row("HEX", str(self.hex).upper())
        table.add_row("RGB", self.rgb)
        return table
