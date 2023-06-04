import colorsys
import re
from enum import Enum, auto
from typing import Tuple
from collections.abc import ABC, abstractmethod

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

from maxgradient.theme import GradientTheme
from maxgradient.log import Log
from maxgradient._abcolor import ABColor, Mode
from maxgradient._rich import RICH, RICHHEX, RICHRGB, get_rich_color, rich_table
from maxgradient._x11 import X11, X11HEX, X11RGB, get_x11_color, x11_table

console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
install_rich_traceback(console=console)
log = Log(console=console)

class Color(ABColor):
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
    COLOR: Tuple[str, ...] = (
        "magenta",
        "violet",
        "purple",
        "blue",
        "lightblue",
        "cyan",
        "lime",
        "yellow",
        "orange",
        "red"
    )
    HEX: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#0088ff",
        "#00ffff",
        "#00ff00",
        "#ffff00",
        "#ff8800",
        "#ff0000"
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
        "rgb(255, 0, 0)"
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
        (255, 0, 0)
    )
    def __init__(self, color: "Color"|str|Tuple[int, int, int]) -> None:
        """A color to make gradients with."""
        super().__init__(color):
        if isinstance(color, Color):
            self.parse_color(color)
        elif isinstance(color, str):
            if not self.parse_named(color):
            