"""Parse colors from strings."""
# ruff: noqa: F401
import colorsys
import re
from functools import lru_cache, singledispatchmethod
from re import IGNORECASE, Pattern, compile
from typing import Any, List, Tuple

from cheap_repr import normal_repr, register_repr
from rich import inspect
from rich.box import HEAVY, ROUNDED, SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError, ColorType, blend_rgb
from rich.color_triplet import ColorTriplet
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install
from snoop import snoop

console = Console()
tr_install(console=console, show_locals=True)


register_repr(ColorTriplet)(normal_repr)
register_repr(RichColor)(normal_repr)
register_repr(Panel)(normal_repr)


class GradientColorParseError(ColorParseError):
    """Unable to parse a GradientColor from input."""

    pass


RGB_REGEX = re.compile(
    r"r?g?b? ?\((?P<red>\d+\.?\d*)[ ,]? ?(?P<green>\d+\.?\d*)[ ,]? ?(?P<blue>\d+\.?\d*)\)"
)
HEX_REGEX = re.compile(
    r"(#[0-9a-fA-F]{3}\b)|(#[0-9a-fA-F]{6}\b)|([0-9a-fA-F]{3}\b)|([0-9a-fA-F]{6}\b)"
)


class GradientColor:
    """A gradient color."""

    NAMES: Tuple[str, ...] = (
        "magenta",
        "purple",
        "blueviolet",
        "blue",
        "lightblue",
        "skyblue",
        "cyan",
        "springgreen",
        "green",
        "lime",
        "chartreuse",
        "greenyellow",
        "yellow",
        "orange",
        "orangered",
        "red",
        "deeppink",
        "hotpink",
    )
    HEX: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#005fff",
        "#00afff",
        "#00ffff",
        "#00ffaf",
        "#00ff5f",
        "#00ff00",
        "#5fff00",
        "#afff00",
        "#ffff00",
        "#ffaf00",
        "#ff5f00",
        "#ff0000",
        "#ff005f",
        "#ff00af",
    )
    RGB: Tuple[str, ...] = (
        "rgb(255, 0, 255)",
        "rgb(175, 0, 255)",
        "rgb(95, 0, 255)",
        "rgb(0, 0, 255)",
        "rgb(0, 95, 255)",
        "rgb(0, 175, 255)",
        "rgb(0, 255, 255)",
        "rgb(0, 255, 175)",
        "rgb(0, 255, 95)",
        "rgb(0, 255, 0)",
        "rgb(95, 255, 0)",
        "rgb(175, 255, 0)",
        "rgb(255, 255, 0)",
        "rgb(255, 175, 0)",
        "rgb(255, 95, 0)",
        "rgb(255, 0, 0)",
        "rgb(255, 0, 95)",
        "rgb(255, 0, 175)",
    )
    TRIPLETS: Tuple[ColorTriplet, ...] = (
        ColorTriplet(255, 0, 255),
        ColorTriplet(175, 0, 255),
        ColorTriplet(95, 0, 255),
        ColorTriplet(0, 0, 255),
        ColorTriplet(0, 95, 255),
        ColorTriplet(0, 175, 255),
        ColorTriplet(0, 255, 255),
        ColorTriplet(0, 255, 175),
        ColorTriplet(0, 255, 95),
        ColorTriplet(0, 255, 0),
        ColorTriplet(95, 255, 0),
        ColorTriplet(175, 255, 0),
        ColorTriplet(255, 255, 0),
        ColorTriplet(255, 175, 0),
        ColorTriplet(255, 95, 0),
        ColorTriplet(255, 0, 0),
        ColorTriplet(255, 0, 95),
        ColorTriplet(255, 0, 175),
    )

    @singledispatchmethod
    def __init__(self, value) -> None:
        """Initialize a GradientColor object.

        Args:
            value (Any): A gradient color.
        """
        pass

    @__init__.register(RichColor)
    def _(self, value) -> None:
        self.name = value.name
        self.type: ColorType = ColorType.TRUECOLOR
        self.triplet = value.triplet
        super().__init__()
        self.hex = self.triplet.hex
        self.rgb = self.triplet.rgb

    @__init__.register(ColorTriplet)
    def _(self, value: ColorTriplet) -> None:
        if value not in self.TRIPLETS:
            raise GradientColorParseError(f"Invalid input: {value}")
        index: int = self.TRIPLETS.index(value)
        self.name = self.NAMES[index]
        self.type = ColorType.TRUECOLOR
        self.triplet = value
        super().__init__()
        self.hex = self.triplet.hex
        self.rgb = self.triplet.rgb

    @__init__.register(str)
    def _(self, value: str) -> None:
        index: int = -1
        for group in [self.NAMES, self.HEX, self.RGB]:
            if value in group:
                index = group.index(value)
                break
            else:
                continue
        if index < 0 or index > len(self.NAMES):
            raise GradientColorParseError(f"Invalid input: {value}")
        self.name = self.NAMES[index]
        self.type = ColorType.TRUECOLOR
        self.triplet = self.TRIPLETS[index]
        super().__init__()
        self.hex = self.triplet.hex
        self.rgb = self.triplet.rgb

    @property
    def name(self) -> str:
        """Return the name of the gradient color."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the gradient color."""
        if value not in self.NAMES:
            raise GradientColorParseError(f"Invalid input: {value}")
        self._name = value

    @property
    def hex(self) -> str:
        """Return the hex value of the gradient color."""
        return self._hex

    @hex.setter
    def hex(self, value: str) -> None:
        """Set the hex value of the gradient color."""
        match = HEX_REGEX.search(value)
        if match is None:
            raise GradientColorParseError(
                f"Invalid input: {value}. Expected hex string."
            )
        else:
            self._hex = value

    @property
    def rgb(self) -> str:
        """Return the RGB value of the gradient color."""
        return self._rgb

    @rgb.setter
    def rgb(self, value: str) -> None:
        """Set the RGB value of the gradient color."""
        match = RGB_REGEX.search(value)
        if match is None:
            raise GradientColorParseError(
                f"Invalid input: {value}. Expected RGB string."
            )
        else:
            self._rgb = value

    @property
    def triplet(self) -> ColorTriplet:
        """Return the ColorTriplet of the gradient color."""
        return self._triplet

    @triplet.setter
    def triplet(self, value: ColorTriplet) -> None:
        """Set the ColorTriplet of the gradient color."""
        if value not in self.TRIPLETS:
            raise GradientColorParseError(f"Invalid input: {value}")
        self._triplet = value

    def __str__(self) -> str:
        """String representation of the object."""
        return self.name

    def __repr__(self) -> str:
        return f"GradientColor<{self.name}>"

    @classmethod
    @lru_cache
    def get_names(cls) -> Tuple[str, ...]:
        """Retrieve the name of each GradientColor."""
        return cls.NAMES

    @classmethod
    @lru_cache
    def get_hex(cls) -> Tuple[str, ...]:
        """Retrieve the hex value of each GradientColor."""
        return cls.HEX

    @classmethod
    @lru_cache
    def get_rgb(cls) -> Tuple[str, ...]:
        """Retrieve the RGB value of each GradientColor."""
        return cls.RGB

    @classmethod
    @lru_cache
    def get_triplets(cls) -> Tuple[ColorTriplet, ...]:
        """Retrieve the ColorTriplet of each GradientColor."""
        return cls.TRIPLETS

    @property
    def contrast(self) -> ColorTriplet:
        """Generate a foreground color for the color style.

        Generate a foreground color for the color style based on the color's
        contrast ratio. If the color is dark, the foreground color will be
        white. If the color is light, the foreground color will be black.

        Returns:
            str: The foreground color.
        """
        closest = GradientColor.find_closest_color(
            self.triplet,
            color_list=[ColorTriplet(0, 0, 0), ColorTriplet(255, 255, 255)],
        )
        if closest == ColorTriplet(0, 0, 0):
            return ColorTriplet(255, 255, 255)
        else:
            return ColorTriplet(0, 0, 0)

    @property
    def row_styles(self) -> List[str]:
        """Generate a list of row styles for a rich table."""
        shade = RichColor.from_triplet(self.darken(0.9))
        shade_style = Style(color="#ffffff", bgcolor=shade, bold=True)
        return [f"bold #ffffff on {self.hex}", str(shade_style)]

    @staticmethod
    def triplet_to_hsv(triplet: ColorTriplet) -> Tuple[float, float, float]:
        """Convert an RGB color to HSV."""
        h, s, v = colorsys.rgb_to_hsv(
            triplet.red / 255, triplet.green / 255, triplet.blue / 255
        )
        return h, s, v

    @staticmethod
    def color_distance(triplet1: ColorTriplet, triplet2: ColorTriplet):
        """Calculate the distance between two colors."""
        h1, s1, v1 = GradientColor.triplet_to_hsv(triplet1)
        h2, s2, v2 = GradientColor.triplet_to_hsv(triplet2)
        dh: float = min(abs(h1 - h2), 1 - abs(h1 - h2))
        ds: float = abs(s1 - s2)
        dv: float = abs(v1 - v2)
        color_distance: float = dh + ds + dv
        return color_distance

    @staticmethod
    def find_closest_color(triplet: ColorTriplet, color_list: List[ColorTriplet]):
        """Calculate the closest color in a list."""
        closest_color = None
        min_distance = float("inf")
        for color in color_list:
            distance = GradientColor.color_distance(triplet, color)
            if distance < min_distance:
                min_distance = distance
                closest_color = color
        return closest_color

    def darken(self, amount: float = 0.5) -> ColorTriplet:
        """Darken a color by a given amount.

        Args:
            amount (float, optional): The amount to darken the color. Defaults to 0.5.

        Returns:
            GradientColor: A new GradientColor object.
        """
        black = ColorTriplet(0, 0, 0)
        shade = blend_rgb(self.triplet, black, amount)
        return shade

    def lighten(self, amount: float = 0.5) -> ColorTriplet:
        """Darken a color by a given amount.

        Args:
            amount (float, optional): The amount to darken the color. Defaults to 0.5.

        Returns:
            GradientColor: A new GradientColor object.
        """
        white = ColorTriplet(255, 255, 255)
        tint = blend_rgb(self.triplet, white, amount)
        return tint

    @property
    def rgb_text(self) -> Text:
        """Return the RGB color string as a rich Text object."""
        return self.colorize_triplet(True)

    def __rich__(self) -> Panel:
        """Return a rich table representation of the gradient color."""
        _dark_style = Style(color=RichColor.from_triplet(self.darken(0.5)))
        table = Table(
            show_header=False,
            show_footer=False,
            show_edge=True,
            show_lines=False,
            box=HEAVY,
            border_style=f"bold {self.hex}",
            expand=False,
            # row_styles = self.row_styles
        )

        table.add_column("attribute", justify="right")
        table.add_column(
            "value",
            style=Style(color=f"{self.hex}", bgcolor=self.contrast.hex),
            justify="left",
        )

        # Key Styles
        key_style_even: Style = Style(
            color="#FFFFFF",
            bgcolor=RichColor.from_triplet(self.triplet),
            bold=True,
            italic=True,
        )
        key_style_odd: Style = Style(
            color=f"{self.hex}",
            bgcolor=RichColor.from_triplet(
                blend_rgb(self.triplet, self.contrast, 0.85)
            ),
            bold=True,
            italic=True,
        )

        # Mode
        mode_key = Text("Mode", style=key_style_odd, justify="right")
        mode = f"[b {self.hex}]Mode[/][#cfcfff].[/][i #7FD6E8]GradientColor[/]"
        table.add_row(mode_key, mode)

        # Hex
        hex_str = str(self.hex).upper()
        hex_key = Text("HEX", style=key_style_even, justify="right")
        table.add_row(hex_key, Text(hex_str, style=f"bold {self.hex}"))

        # RGB
        rgb_key = Text("RGB", style=key_style_odd, justify="right")
        table.add_row(rgb_key, self.colorize_triplet(rgb=True))

        # ColorTriplet
        triplet_key = Text("ColorTriplet", style=key_style_even, justify="right")
        table.add_row(triplet_key, self.colorize_triplet())

        title = self.color_title()
        _dark_style = Style(color=RichColor.from_triplet(self.darken(0.5)))
        sub_panel = Panel(
            table, title=title, expand=False, box=HEAVY, border_style=_dark_style
        )
        _darker_style = Style(color=RichColor.from_triplet(self.darken(0.75)))
        panel = Panel(sub_panel, box=SQUARE, border_style=_darker_style, expand=False)
        return panel

    def colorize_triplet(
        self, rgb: bool = False, *, justify: JustifyMethod = "right"
    ) -> Text:
        """Format a ColorTriplet as a rich.text.Text object.

        Args:
            rgb (bool, optional): Whether to return the RGB value. Defaults to False.

        Returns:
            Text: A colored Text object.
        """
        prefix: str = "rgb" if rgb else "ColorTriplet"
        left_str: str = "("
        right_str: str = ")"
        comma_str: str = ","
        left = Text(left_str, style="bold #ffffff")
        right = Text(right_str, style="bold #ffffff")
        comma = Text(comma_str, style="bold #ffffff")

        pad = self.pad_value
        return Text.assemble(
            *[
                Text(prefix, style=f"bold {self.hex}"),
                left,
                Text(f"{pad(self.triplet.red)}", style="bold #ff0000"),
                comma,
                Text(f"{pad(self.triplet.green)}", style="bold #00ff00"),
                comma,
                Text(f"{pad(self.triplet.blue)}", style="bold #00afff"),
                right,
            ]
        )

    def color_title(self) -> Text:
        """Generate a title bar for the color."""

        name = self.name.capitalize()
        length = len(name)
        # Calculate
        if length % 2 == 1:
            name = f"{name} "  # makes length even
            length += 1
        padding: int = (38 - length) / 2  # type: ignore
        pad = " " * int(padding)
        color = RichColor.from_triplet(
            blend_rgb(self.triplet, ColorTriplet(red=0, green=0, blue=0))
        )
        bg_color = RichColor.from_triplet(
            blend_rgb(self.triplet, ColorTriplet(red=255, green=255, blue=255), 0.5)
        )
        return Text(
            f"{pad}{name}{pad}", style=Style(color=color, bgcolor=bg_color, bold=True)
        )

    @staticmethod
    def pad_value(value: str | int) -> str:
        """Pad the value with spaces."""
        if isinstance(value, int):
            str_value = str(value)
        elif isinstance(value, str):
            str_value = value
        else:
            raise TypeError(f"Expected str or int, got {type(value)}")
        if len(str_value) < 3:
            return f'{" " * (3 - len(str_value))}{str_value}'
        return str_value

    @staticmethod
    def get_title() -> Text:
        """Generate a colored text title."""
        return Text.assemble(
            *[
                Text("G", style=Style(color="#ff00ff", bold=True)),
                Text("r", style=Style(color="#cf00ff", bold=True)),
                Text("a", style=Style(color="#af00ff", bold=True)),
                Text("d", style=Style(color="#8f00ff", bold=True)),
                Text("i", style=Style(color="#6f00ff", bold=True)),
                Text("e", style=Style(color="#4f00ff", bold=True)),
                Text("n", style=Style(color="#2f00ff", bold=True)),
                Text("t", style=Style(color="#0000ff", bold=True)),
                Text("C", style=Style(color="#00ccff", bold=True)),
                Text("o", style=Style(color="#00aaff", bold=True)),
                Text("l", style=Style(color="#0088ff", bold=True)),
                Text("o", style=Style(color="#006fff", bold=True)),
                Text("r", style=Style(color="#004fff", bold=True)),
                Text("s", style=Style(color="#002fff", bold=True)),
            ]
        )

    @classmethod
    def color_table(cls) -> Table:
        """Generate a table of gradient colors."""
        table = Table(title=cls.get_title(), box=SQUARE, expand=False)
        table.add_column("Sample", justify="center", style="bold")
        table.add_column("Name", justify="left", style="bold")
        table.add_column("Hex", justify="center", style="bold")
        table.add_column("RGB", justify="center", style="bold")
        table.add_column("ColorTriplet", justify="center", style="bold")
        for name, hex, rgb, triplet in zip(cls.NAMES, cls.HEX, cls.RGB, cls.TRIPLETS):
            sample = Text(" " * 10, style=Style(bgcolor=hex, bold=True))
            name_text = Text(
                str(name).capitalize(), style=f"bold {hex}", justify="left"
            )
            hex_text = Text(hex.upper(), style=f"bold {hex}")
            rgb_text = cls.triplet_to_rgb(triplet)
            triplet_text = cls.format_triplet(triplet)
            table.add_row(sample, name_text, hex_text, rgb_text, triplet_text)
        return table

    @staticmethod
    def triplet_to_rgb(triplet: ColorTriplet, justify: JustifyMethod = "left") -> Text:
        """Format an RGB string as a rich Text object."""
        left_str: str = "("
        right_str: str = ")"
        comma_str: str = ","
        left = Text(left_str, style="bold #ffffff")
        right = Text(right_str, style="bold #ffffff")
        comma = Text(comma_str, style="bold #ffffff")

        pad = GradientColor.pad_value
        return Text.assemble(
            *[
                Text("rgb", style=f"bold {triplet.hex}"),
                left,
                Text(f"{pad(triplet.red)}", style="bold #ff0000"),
                comma,
                Text(f"{pad(triplet.green)}", style="bold #00ff00"),
                comma,
                Text(f"{pad(triplet.blue)}", style="bold #00afff"),
                right,
            ]
        )

    def as_title(self, color: str, console: Console = console) -> Text:
        """Capitalize, format, and color a gradient color's name.

        Returns:
            text: Colorized gradient_color's capitalized name.
        """
        return Text(self.name.capitalize(), style=f"bold {self.hex}")

    @classmethod
    def format_triplet(cls, triplet: ColorTriplet) -> Text:
        """Format a ColorTriplet as a rich Text object."""
        left_str: str = "("
        right_str: str = ")"
        comma_str: str = ","
        left = Text(left_str, style="bold #ffffff")
        right = Text(right_str, style="bold #ffffff")
        comma = Text(comma_str, style=f"bold {triplet.hex}")

        return Text.assemble(
            *[
                Text("ColorTriplet", style=f"bold {triplet.hex}"),
                left,
                Text(f"{cls.pad_value(triplet.red)}", style="bold #FF0000"),
                comma,
                Text(f"{cls.pad_value(triplet.green)}", style="bold #00AF00"),
                comma,
                Text(f"{cls.pad_value(triplet.blue)}", style="bold #00AFFF"),
                right,
            ],
            justify="left",
        )


def hex_str(value: ColorTriplet) -> str:
    """Return the RGB color string."""

    red: str = f"{value.red:02X}"
    green: str = f"{value.green:02X}"
    blue: str = f"{value.blue:02X}"
    hex: str = f"#{red}{green}{blue}"
    return hex


def hex_text(value: ColorTriplet) -> Text:
    """Return the RGB color string as a rich Text object."""
    hex = hex_str(value).upper()
    return Text(hex, style=f"bold {hex}")


def print_color_table(save: bool = False) -> None:
    if save:
        console = Console(record=True)
    else:
        console = Console()

    console.line(2)
    console.print(GradientColor.color_table(), justify="center")
    console.line(2)

    if save:
        console.save_svg(
            "docs/img/gc_color_table.svg",
            title="Gradient Color Table",
        )


if __name__ == "__main__":  # pragma: no cover
    for color in GradientColor.NAMES:
        console.print(GradientColor(color))
