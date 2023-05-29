"""Purpose: Color class to parse colors for a gradient."""

import colorsys
import re
from enum import Enum, auto
from pathlib import Path
from sys import path
from typing import Tuple

from rich.box import SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError
from rich.color_triplet import ColorTriplet
from rich.columns import Columns
from rich.console import Console, RenderResult
from rich.table import Table
from rich.text import Text

from maxgradient._rich import get_rich_color, rich_table
from maxgradient._x11 import get_x11_color, x11_table
from maxgradient.theme import GradientTheme

ColorType = str | Tuple[int, int, int] | RichColor

HEX_REGEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_REGEX = re.compile(r"^r?g?b?\((\d{1,3}),\s?(\d{1,3}),\s?(\d{1,3})\)$")


class Mode(Enum):
    """A color mode. Used to determine how a color was parsed."""

    NAMED = auto()
    HEX = auto()
    RGB = auto()
    X11 = auto()
    RICH = auto()

console = Console(theme=GradientTheme())

named1 = Mode.NAMED
_hex = Mode.HEX
named2 = Mode.NAMED

console.print(f"\"named1\": {named1}") # -> "named"
console.print(f"\"_hex.name\": {_hex.name}")# -> "HEX"

comparison_1 = f"[#F1FA8C]named1[/] == `named2` -> {named1 == named2.RGB}"
console.print(f"\"named1.value\": {named1.value}")== named2)