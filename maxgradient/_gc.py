"""Parse colors from strings."""
# pylint: disable=C0209,E0401,W0611,C0103,E0202,E0611,W0622
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

from maxgradient._mode import Mode
from maxgradient._rich import Rich
from maxgradient._x11 import X11
from maxgradient.log import Console as LogConsole
from maxgradient.log import Log

console = LogConsole()
log = Log()


class GradientColor:
    """A class of colors used in automatically generating random gradients."""

    mode: Mode = Mode.GC
    NAMES: Tuple[str, ...] = (
        "magenta",
        "violet",
        "purple",
        "blue",
        "lightblue",
        "cyan",
        "green",
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
    HEX3: Tuple[str, ...] = (
        "#f0f",
        "#a0f",
        "#50f",
        "#00f",
        "#08f",
        "#0ff",
        "#0f0",
        "#ff0",
        "#f80",
        "#f00",
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
        """Retrieve gradient RGB tuples.

        Args:
            color (str): A gradient color.

        Returns:
            Optional[int]: The index of the gradient color.
        """
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
        letter_g1 = Text("G", style=Style(color="#ff00ff", bold=True))
        letter_r1 = Text("r", style=Style(color="#cf00ff", bold=True))
        letter_a1 = Text("a", style=Style(color="#af00ff", bold=True))
        letter_d1 = Text("d", style=Style(color="#8f00ff", bold=True))
        letter_i1 = Text("i", style=Style(color="#6f00ff", bold=True))
        letter_e1 = Text("e", style=Style(color="#4f00ff", bold=True))
        letter_n1 = Text("n", style=Style(color="#2f00ff", bold=True))
        letter_t1 = Text("t", style=Style(color="#0000ff", bold=True))
        letter_c1 = Text("C", style=Style(color="#00ccff", bold=True))
        letter_o1 = Text("o", style=Style(color="#00aaff", bold=True))
        letter_l1 = Text("l", style=Style(color="#0088ff", bold=True))
        letter_o2 = Text("o", style=Style(color="#006fff", bold=True))
        letter_r2 = Text("r", style=Style(color="#004fff", bold=True))
        letter_s1 = Text("s", style=Style(color="#002fff", bold=True))
        title = [
            letter_g1,
            letter_r1,
            letter_a1,
            letter_d1,
            letter_i1,
            letter_e1,
            letter_n1,
            letter_t1,
            letter_c1,
            letter_o1,
            letter_l1,
            letter_o2,
            letter_r2,
            letter_s1,
        ]
        return Text.assemble(*title)

    @classmethod
    def color_table(cls) -> Table:
        """Generate a table of gradient colors."""
        table = Table(title=cls.get_title(), box=SQUARE)
        table.add_column("Sample", justify="center", style="bold")
        table.add_column("Name", justify="center", style="bold")
        table.add_column("Hex", justify="center", style="bold")
        table.add_column("RGB", justify="center", style="bold")
        table.add_column("RGB Tuple", justify="center", style="bold")
        for x in range(10):
            hex = cls.get_hex()[x]
            table.add_row(
                Text(" " * 10, style=Style(bgcolor=hex, bold=True)),
                Text(
                    str(cls.get_names()[x]).capitalize(),
                    style=Style(color=hex, bold=True),
                ),
                Text(str(cls.get_hex()[x]), style=Style(color=hex, bold=True)),
                Text(str(cls.get_rgb()[x]), style=Style(color=hex, bold=True)),
                Text(str(cls.get_rgb_tuple()[x]), style=Style(color=hex, bold=True)),
            )
        return table

    @classmethod
    def as_title(cls, color: str) -> Text:
        """Capitalize, format, and color a gradient color's name.

        Returns:
            Text: Colorized gradient color's capitalized name.
        """
        index: int = cls.get_color(color)
        name = cls.NAMES[index]
        capital_name = name.capitalize()
        return f"[bold {color}]{capital_name}[/bold {color}]"


if __name__ == "__main__":
    console = Console()
    console.line(2)
    console.print(GradientColor.color_table(), justify="center")
    console.line(2)
