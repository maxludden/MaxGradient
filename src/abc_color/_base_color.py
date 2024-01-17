# ruff: noqa: F401
from abc import (
    ABC,
    abstractclassmethod,
    abstractmethod,
    abstractproperty,
    abstractstaticmethod,
)
from colorsys import rgb_to_hsv
from enum import Enum
from functools import singledispatchmethod
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    cast,
)

from rich.box import HEAVY, SQUARE
from rich.color import Color as RichColor
from rich.color import blend_rgb, ColorType
from rich.color_triplet import ColorTriplet
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

from maxgradient._hex_color import Hex as _HEX
from maxgradient._mode import Mode
from maxgradient._rgb_color import RGB as _RGB

console = Console()
tr_install(console=Console(), show_locals=True)

ColorInput: TypeAlias = Union[_HEX, _RGB, RichColor, str, ColorTriplet]


class OutputFormat(Enum):
    """An enum for the output format of a color."""

    COLOR_TRIPLET = ColorTriplet
    COLOR = RichColor
    STYLE = Style

    def __eq__(self, other: Any) -> bool:
        """Return True if the output format is equal to another."""
        if isinstance(other, OutputFormat):
            return self.value == other.value
        else:
            return False

    def __repr__(self) -> str:
        """Return a representation of the output format."""
        return f"OutputFormat.{str(self.value).upper()}"

    def __rich__(self) -> Text:
        """Return a rich text representation of the output format."""
        mode = Text("OutputFormat", style="italic #7FD6E8")
        dot = Text(".", style="bold.white")
        value: str = str(self.value).upper()
        formatted_value = Text(value, style="bold.white")
        rich_repr = Text.assemble(mode, dot, formatted_value)
        return rich_repr


class BaseColor(ABC, RichColor):
    """A superclass for all colors."""

    @abstractproperty
    def NAMES(self) -> Tuple:  # noqa: E741 # type: ignore
        """Return a tuple of all color names."""
        pass

    @abstractproperty
    def HEX(self) -> str:  # noqa: E741 # type: ignore
        """Return the hex color code."""
        pass

    @abstractproperty
    def RGB(self) -> Tuple:  # noqa: E741 # type: ignore
        """Return the RGB color code."""
        pass

    @abstractproperty
    def TRIPLETS(self) -> Tuple:  # noqa: E741 # type: ignore
        """Return the ColorTriplet."""
        pass

    @singledispatchmethod
    @abstractmethod
    def __init__(self, value):
        """Initialize the color."""
        self.type: ColorType = ColorType.TRUECOLOR

    @abstractclassmethod
    @__init__.register
    def _ColorTriplet(cls, value: ColorTriplet):
        """Initialize the color from a ColorTriplet."""
        pass

    @abstractmethod
    def find_index(self, value) -> int:
        """Find the index of the color in its group."""
        for group in [self.NAMES, self.HEX, self.RGB, self.TRIPLETS]:
            if value in group:
                return group.index(value)
            else:
                continue
        raise ValueError(f"Color not found: {value}")

    @property
    def name(self) -> str:
        """Return the name of the color."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the color."""
        self._name = value

    @property
    def red(self) -> int:
        """Return the red value of the color."""
        return self._red

    @red.setter
    def red(self, value: int) -> None:
        """Set the red value of the color."""
        assert (
            value >= 0 and value <= 255
        ), f"Expected value between 0 and 255, got {value}"
        self._red = value

    @property
    def green(self) -> int:
        """Return the green value of the color."""
        return self._green

    @green.setter
    def green(self, value: int) -> None:
        """Set the green value of the color."""
        assert (
            value >= 0 and value <= 255
        ), f"Expected value between 0 and 255, got {value}"
        self._green = value

    @property
    def blue(self) -> int:
        """Return the blue value of the color."""
        return self._blue

    @blue.setter
    def blue(self, value: int) -> None:
        """Set the blue value of the color."""
        assert (
            value >= 0 and value <= 255
        ), f"Expected value between 0 and 255, got {value}"
        self._blue = value

    @abstractproperty
    def mode(self) -> Mode:
        """Return the mode of the color."""
        return Mode()

    @mode.setter
    def mode(self, value: Mode) -> None:
        """Set the mode of the color."""
        self._mode = value

    @property
    def hex(self) -> str:
        """Return the hex color code."""
        red_str = f"{self.red:02X}"
        green_str = f"{self.green:02X}"
        blue_str = f"{self.blue:02X}"
        return f"#{red_str}{green_str}{blue_str}"

    @property
    def rgb(self) -> str:
        """Return the RGB color code."""
        return f"rgb({self.red},{self.green},{self.blue})"

    @property
    def triplet(self) -> ColorTriplet:
        """Return the ColorTriplet."""
        return ColorTriplet(self.red, self.green, self.blue)

    @triplet.setter
    def triplet(self, value: ColorTriplet) -> None:
        """Set the ColorTriplet."""
        self.red = value.red
        self.green = value.green
        self.blue = value.blue

    @property
    def style(self) -> Style:
        """Return the Style."""
        return Style(color=self.name)

    @property
    def bg_style(self) -> Style:
        """Return the Style."""
        return Style(bgcolor=self.name)

    def darken(
        self, amount: float = 0.5, output: OutputFormat = OutputFormat.COLOR_TRIPLET
    ) -> ColorTriplet:
        """Generate the shade of a color."""
        return blend_rgb(self.triplet, ColorTriplet(0, 0, 0), amount)

    @property
    def shade(self) -> ColorTriplet:
        return self.darken()

    def lighten(
        self, amount: float = 0.5, output: OutputFormat = OutputFormat.COLOR_TRIPLET
    ) -> ColorTriplet:
        """Generate the tint of a color."""
        return blend_rgb(self.triplet, ColorTriplet(255, 255, 255), amount)

    @property
    def tint(self) -> ColorTriplet:
        return self.lighten()

    def __rich__(self) -> Panel:
        """Return a rich renderable for the color."""
        table = Table(
            box=HEAVY, border_style=f"bold {self.hex}", show_header=False, width=40
        )
        table.add_column("Attribute", justify="right", style=f"i on {self.hex}")
        table.add_column("Value", justify="left", style=f"bold {self.hex}")
        table.add_row(
            Text(
                "Mode",
                style=Style(
                    color=RichColor.from_triplet(self.get_contrast()),
                    bgcolor=RichColor.from_triplet(self.darken()),
                    italic=True,
                ),
            ),
            "[i #dddddd]Mode[/][b #ff00ff].[/][#7fafff]GRADIENT_COLOR[/]",
        )
        table.add_row(
            f"[bold {self.hex} on {self.shade}]Style[/]",
            f"[self.style]{str(self.style)}[/]",
        )
        table.add_row(
            Text(
                "Hex",
                style=Style(
                    color=RichColor.from_triplet(self.get_contrast()),
                    bgcolor=RichColor.from_triplet(self.darken()),
                    italic=True,
                ),
            ),
            f"[bold {self.hex}]{self.hex}[/]",
        )
        table.add_row(f"[bold {self.hex} on {self.shade}]RGB[/]", self.rgb)
        title_pad = (30 - len(self.name)) // 2
        pad = title_pad * " "
        tint = self.lighten(0.25, OutputFormat.STYLE)
        shade = self.darken(0.5, OutputFormat.STYLE)
        return Panel(
            table,
            title=f"[bold {shade} on {tint}]{pad}{self.name.capitalize()}{pad}[/]",
            border_style=f"bold dim {self.hex}",
            box=SQUARE,
            expand=False,
        )

    def get_contrast(self) -> ColorTriplet:
        """Generate a foreground color for the color style.

        Generate a foreground color for the color style based on the color's
        contrast ratio. If the color is dark, the foreground color will be
        white. If the color is light, the foreground color will be black.

        Returns:
            str: The foreground color.
        """

        def triplet_to_hsv(triplet: ColorTriplet) -> Tuple[float, float, float]:
            """Convert an RGB color to HSV."""
            h, s, v = rgb_to_hsv(
                triplet.red / 255, triplet.green / 255, triplet.blue / 255
            )
            return h, s, v

        def color_distance(triplet1: ColorTriplet, triplet2: ColorTriplet):
            """Calculate the distance between two colors."""
            h1, s1, v1 = triplet_to_hsv(triplet1)
            h2, s2, v2 = triplet_to_hsv(triplet2)
            dh: float = min(abs(h1 - h2), 1 - abs(h1 - h2))
            ds: float = abs(s1 - s2)
            dv: float = abs(v1 - v2)
            color_distance: float = dh + ds + dv
            return color_distance

        def find_closest_color(triplet: ColorTriplet, color_list: List[ColorTriplet]):
            """Calculate the closest color in a list."""
            closest_color = None
            min_distance = float("inf")
            for color in color_list:
                distance = color_distance(triplet, color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color
            return closest_color

        closest = find_closest_color(
            self.triplet,
            color_list=[ColorTriplet(0, 0, 0), ColorTriplet(255, 255, 255)],
        )
        if closest == ColorTriplet(0, 0, 0):
            return ColorTriplet(255, 255, 255)
        else:
            return ColorTriplet(0, 0, 0)
