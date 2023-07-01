"""Parse colors from strings."""
# pylint: disable=C0209,E0401,W0611,C0103,E0202
import colorsys
import re
from functools import lru_cache
from re import findall
from typing import Optional, Tuple

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
from snoop import snoop

from maxgradient._log import Console as LogConsole
from maxgradient._log import Log
from maxgradient._mode import Mode
from maxgradient._rich import Rich
from maxgradient._x11 import X11
from maxgradient.theme import GradientTerminalTheme, GradientTheme

console = LogConsole()
log = Log()


class GradientColor:
    mode: Mode = Mode.GC
    NAMES: Tuple[str, ...] = (
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
        "rgb(255,0,255)",
        "rgb(175,0,255)",
        "rgb(95,0,255)",
        "rgb(0,0,255)",
        "rgb(0,36,255)",
        "rgb(0,255,255)",
        "rgb(0,255,0)",
        "rgb(255,255,0)",
        "rgb(255,136,0)",
        "rgb(255,0,0)",
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

    @classmethod
    @lru_cache(maxsize=10, typed=True)
    def get_names(cls) -> Tuple[str, ...]:
        """Retrieve gradient colors."""
        return cls.NAMES

    @classmethod
    @lru_cache(maxsize=10, typed=True)
    def get_hex(cls) -> Tuple[str, ...]:
        """Retrieve gradient hex colors."""
        return cls.HEX

    @classmethod
    @lru_cache(maxsize=10, typed=True)
    def get_rgb(cls) -> Tuple[str, ...]:
        """Retrieve gradient RGB colors."""
        return cls.RGB

    @classmethod
    @lru_cache(maxsize=10, typed=True)
    def get_rgb_tuple(cls) -> Tuple[Tuple[int, int, int]]:
        """Retrieve gradient RGB tuples."""
        return cls.RGB_TUPLE

    @classmethod
    @lru_cache(maxsize=10, typed=True)
    def get_color(cls, color: str) -> Optional[Tuple[int, int, int]]:
        """Retrieve gradient RGB tuples."""
        for group in [
            cls.get_names(),
            cls.get_hex(),
            cls.get_rgb(),
            cls.get_rgb_tuple(),
        ]:
            if color in group:
                index = group.index(color)
                return cls.get_rgb_tuple()[index]
        return None

    @staticmethod
    def rgb_to_tuple(rgb: str) -> Tuple[int, int, int]:
        """Convert a rgb string to a tuple of ints"""
        log.debug(f"Converting {rgb} to tuple...")
        rgb_match = findall(r"r?g?b?\((\d+),(\d+),(\d+)\)", rgb)
        if rgb_match:
            return tuple(int(x) for x in rgb_match[0])
        raise ValueError(f"Invalid rgb string: {rgb}")

    @staticmethod
    def get_title() -> Text:
        """Generate a colored text title."""
        letter_g = Text("G", style=Style(color="#ff00ff", bold=True))
        letter_r1 = Text("r", style=Style(color="#cf00ff", bold=True))
        letter_a = Text("a", style=Style(color="#af00ff", bold=True))
        letter_d = Text("d", style=Style(color="#8f00ff", bold=True))
        letter_i = Text("i", style=Style(color="#6f00ff", bold=True))
        letter_e = Text("e", style=Style(color="#4f00ff", bold=True))
        letter_n = Text("n", style=Style(color="#2f00ff", bold=True))
        letter_t = Text("t", style=Style(color="#0000ff", bold=True))
        letter_c = Text("C", style=Style(color="#002fff", bold=True))
        letter_o = Text("o", style=Style(color="#004fff", bold=True))
        letter_l = Text("l", style=Style(color="#006fff", bold=True))
        letter_o2 = Text("o", style=Style(color="#0088ff", bold=True))
        letter_r2 = Text("r", style=Style(color="#00aaff", bold=True))
        letter_s = Text("s", style=Style(color="#00ccff", bold=True))
        title = [
            letter_g,
            letter_r1,
            letter_a,
            letter_d,
            letter_i,
            letter_e,
            letter_n,
            letter_t,
            letter_c,
            letter_o,
            letter_l,
            letter_o2,
            letter_r2,
            letter_s,
        ]
        return Text.assemble(*title)

    @classmethod
    def color_table(cls) -> Table:
        """Generate a table of gradient colors."""
        
