# ruff: noqa: F401
import colorsys
import re
from enum import Enum
from functools import lru_cache, singledispatchmethod
from re import IGNORECASE, Pattern
from typing import Any, List, Tuple

import numpy as np
from numpy import array, ndarray, where
from rich import inspect
from rich.box import HEAVY, SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError, ColorType, blend_rgb
from rich.color_triplet import ColorTriplet
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console, show_locals=True)


class GradientColorParseError(ColorParseError):
    """Raised when a gradient color cannot be parsed from input."""

    pass


class Regex:
    """Regex patterns for parsing color inputs."""

    RGB: Pattern = re.compile(
        r"r?g?b? ?\((?P<red>\d+\.?\d*)[ ,]? ?(?P<green>\d+\.?\d*)[ ,]? ?(?P<blue>\d+\.?\d*)\)"
    )
    HEX: Pattern = re.compile(
        r"(#[0-9a-fA-F]{3}\b)|(#[0-9a-fA-F]{6}\b)|([0-9a-fA-F]{3}\b)|([0-9a-fA-F]{6}\b)"
    )


class GradientColor:
    """A gradient color that can be parsed from a number of inputs."""

    NAMES: np.ndarray = np.array(
        [
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
        ]
    )
    HEX: np.ndarray = np.array(
        [
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
        ]
    )
    RGB: np.ndarray = np.array(
        [
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
        ]
    )
    TRIPLETS: np.ndarray = np.array(
        [
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
        ]
    )

    def __init__(self, color: Any) -> None:
        """Initialize a GradientColor from a color input.

        Args:
            color (ColorType): A color input that can be parsed into a GradientColor.
        """
        index = self.find_index(color)
        self.index = index
        self.name = self.NAMES[index]
        triplet: ColorTriplet = self.TRIPLETS[index]
        self.red = triplet[0]
        self.green = triplet[1]
        self.blue = triplet[2]

    @classmethod
    def find_index(cls, color) -> int:
        if color in cls.NAMES:
            return np.where(cls.NAMES == color)[0][0]
        elif color in cls.HEX:
            return np.where(cls.HEX == color)[0][0]
        elif color in cls.RGB:
            return np.where(cls.RGB == color)[0][0]
        elif color in cls.TRIPLETS:
            return np.where((cls.TRIPLETS == color).all(axis=1))[0][0]
        else:
            raise ValueError(f"Color {color} not found in any array.")

    @property
    def hex(self) -> str:
        """Return the hex color code."""
        red_str = f"{self.red:02X}"
        green_str = f"{self.green:02X}"
        blue_str = f"{self.blue:02X}"
        return f"#{red_str}{green_str}{blue_str}"

    @property
    def rgb(self) -> str:
        """Return the rgb color code."""
        return f"rgb({self.red},{self.green},{self.blue})"

    @property
    def triplet(self) -> ColorTriplet:
        """Return the color triplet."""
        return ColorTriplet(self.red, self.green, self.blue)

    def __repr__(self) -> str:
        """Return a string representation of the GradientColor."""
        return f"GradientColor<{self.name}>"

    def __str__(self) -> str:
        """Return the colors name."""
        return self.name

    def __eq__(self, other: Any) -> bool:
        """Return True if the GradientColor is equal to other."""
        if isinstance(other, GradientColor):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __rich__(self) -> Panel:
        """Return a rich Table representation of the GradientColor."""
        table = Table(box=HEAVY, border_style=f"bold {self.hex}", show_header=False, width=40)
        table.add_column("Attribute", justify="right", style=f"i on {self.hex}")
        table.add_column("Value", justify="left", style=f"bold {self.hex}")
        table.add_row("Mode", "[i #dddddd]Mode[/][b #ff00ff].[/][#7fafff]GRADIENT_COLOR[/]")
        table.add_row("Index", f"{self.index}")
        table.add_row("Hex", self.hex)
        table.add_row("RGB", self.rgb)
        title_pad = (30 - len(self.name)) // 2
        pad = title_pad * " "
        return Panel(
            table,
            title=f"[bold reverse]{pad}{self.name.capitalize()}{pad}[/]",
            border_style=f"bold dim {self.hex}",
            box=SQUARE,
            expand=False,
        )


if __name__ == "__main__":
    console.print(GradientColor("rgb(255, 95, 0)"))
    
