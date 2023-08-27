"""Hex Color Class"""
# pylint: disable=C0103
import re
from random import choice
from typing import Tuple

from rich.box import HEAVY_EDGE
from rich.panel import Panel
from rich.text import Text

from maxgradient._mode import Mode
from maxgradient._rich import Rich
from maxgradient.log import Console, Log

console = Console()
log = Log()


class HexParseError(ValueError):
    """Unable to parse input as a hex color."""


class Hex:
    """A class to work with Hex colors."""

    REGEX = re.compile(
        r"(#[0-9a-fA-F]{3}\b)|(#[0-9a-fA-F]{6}\b)|([0-9a-fA-F]{3}\b)|([0-9a-fA-F]{6}\b)"
    )

    def __init__(self, hex: str) -> None:
        """Create a new Hex object."""
        self.value = hex

    @property
    def value(self) -> str:
        """Return the Hex color string."""
        return self._value

    @value.setter
    def value(self, hex: str) -> None:
        """Validate and initialize the hex value."""
        if hex.startswith("#"):
            hex = hex[1:]
        if len(hex) == 3:
            hex = "".join([char * 2 for char in hex])
        try:
            int(hex, 16)
        except ValueError as ve:
            raise HexParseError(f"{hex} is not a valid hex color.") from ve
        self._value = f"#{hex}"

    @property
    def mode(self) -> Mode:
        """Return the color mode."""
        return Mode.HEX

    @property
    def as_rgb_tuple(self) -> Tuple[int, int, int]:
        """Convert the Hex color code into an  RGB tuple."""
        hex = self.value
        if "#" in hex:
            hex = hex[1:]
        red = int(hex[:2], 16)
        green = int(hex[2:4], 16)
        blue = int(hex[4:], 16)
        rgb_tuple = (red, green, blue)
        return (red, green, blue)

    @property
    def as_rgb(self) -> str:
        """Convert the Hex color code into an RGB string."""
        rgb_tuple = self.as_rgb_tuple
        rgb = f"rgb{rgb_tuple}"
        return rgb

    def __repr__(self) -> str:
        """Return a representation of the Hex object."""
        return f"Hex<{self.value}>"

    def __rich_repr__(self) -> Text:
        return Text.assemble(
            "[bold italic white]Hex<[/]",
            f"[bold italic {self.value}]Hex[/]",
            "[bold italic white]>[/]",
        )

    def __str__(self) -> str:
        """Return the hex value."""
        return self.value

    def __eq__(self, other: object) -> bool:
        """Return True if the Hex object is equal to another."""
        if isinstance(other, Hex):
            return self.value == other.value
        else:
            return False

    def __rich__(self) -> Panel:
        """Return a rich panel representation of the Hex object."""
        return Panel(
            f"[bold {self.value}]Hex: {self.value.upper()}",
            border_style=f"bold {self.value}",
            expand=False,
            box=HEAVY_EDGE,
        )

    def is_valid(self) -> bool:
        """Return True if the Hex is valid."""
        return self.REGEX.match(self.value) is not None

    # def print_rich_hex(self) -> None:
    #     """Print a rich representation of all the Hex colors."""
    #     HEX_COLORS = Rich.HEX
    #     panels: list[Panel] = []
    #     for index, color in enumerate(HEX_COLORS):
    #         msg1 = f"[i white]Color[/] [bold cyan]{index}[/][i white]:[/]"
    #         msg2 = f"[bold {color}]{color}[/]"
    #         hex = Hex(color)
    #         panels.append(hex.hex_panel())
    #     columns = Columns(panels, equal=True)
    #     console.print(columns)


if __name__ == "__main__":
    console = Console()
    RANDOM_HEX_STRING = choice(Rich.HEX)
    RANDOM_HEX = Hex(RANDOM_HEX_STRING)
    console.print(RANDOM_HEX)
    console.print(f"[bold {RANDOM_HEX.value}]{RANDOM_HEX.as_rgb}[/]")
    console.print(f"[bold {RANDOM_HEX.value}]{RANDOM_HEX.as_rgb_tuple}[/]")
