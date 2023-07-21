"""Hex Color Class"""
import re
from random import choice
from typing import Optional, Tuple, Union

from rich.box import HEAVY_EDGE
from rich.color import ColorParseError
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text

from maxgradient._mode import Mode
from maxgradient._rich import Rich
from maxgradient.log import Log, Console

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
        log.debug(f"Called Hex.__init__({hex})")
        try:
            self.value = hex
        except HexParseError as hpe:
            raise HexParseError(f"{hex} is not a valid hex color.") from hpe

    @property
    def value(self) -> str:
        """Return the Hex color string."""
        return self._value

    @value.setter
    def value(self, hex: str) -> None:
        """Validate and initialize the hex value."""
        log.debug(f"Called Hex.value({hex})")
        valid_hex = self.parse(hex)
        if valid_hex is not None:
            self._value = valid_hex
        else:
            raise HexParseError(f"{hex} is not a valid hex color.")

    def parse(self, hex: str) -> Optional[str]:
        """Use regex to validate a string is a hex color. If it \
        is, return the formatted hex string.
        
        Args:
            string (str): The string to match.
            
        Returns:
            Optional[str]: The formatted hex string if it is a hex \
            color, else None.
        """
        log.debug(f"Called Hex.parse({hex})")
        valid_color = self.REGEX.match(hex)
        if valid_color:
            hex = valid_color.group(0)
            log.debug(f"Hex: {hex}")
            if "#" in hex:
                hex = hex[1:]

            if len(hex) == 3:
                hex = "".join([char * 2 for char in hex])
            return f"#{hex}"
        else:
            return None

    @property
    def mode(self) -> Mode:
        """Return the color mode."""
        log.debug("Called Hex.mode")
        return Mode.HEX

    @property
    def as_rgb_tuple(self) -> Tuple[int, int, int]:
        """Convert the Hex color code into an  RGB tuple."""
        log.debug("Called Hex.rgb_tuple")
        hex = self.value
        if "#" in hex:
            hex = hex[1:]
        r = int(hex[:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:], 16)
        rgb_tuple = (r, g, b)
        log.debug(f"Converted hex to rgb tuple: {rgb_tuple}")
        return (r, g, b)

    @property
    def as_rgb(self) -> str:
        """Convert the Hex color code into an RGB string."""
        log.debug("Called Hex.rgb")
        rgb_tuple = self.as_rgb_tuple
        rgb = f"rgb{rgb_tuple}"
        log.debug(f"Converted hex to rgb string: {rgb}")
        return rgb

    def __repr__(self) -> str:
        """Return a representation of the Hex object."""
        log.debug("Called Hex.__repr__()")
        return f"Hex<{self.value}>"

    def __rich_repr__(self) -> Text:
        log.debug("Called Hex.__rich_repr__()")
        return Text.assemble(
            "[bold italic white]Hex<[/]",
            f"[bold italic {self.value}]Hex[/]",
            "[bold italic white]>[/]",
        )

    def __str__(self) -> str:
        """Return the hex value."""
        log.debug("Called Hex.__str__()")
        return self.value

    def __eq__(self, other: "Hex",) -> bool: # type: ignore
        """Return True if the Hex object is equal to another."""
        log.debug(f"Called Hex.__eq__({other})")
        if isinstance(other, Hex):
            if self.value == other.value:
                return True
            else:
                return False
        else:
            return False

    def __rich__(self) -> Panel:
        """Return a rich panel representation of the Hex object."""
        log.debug("Called Hex.__rich__()")
        return Panel(
            f"[bold {self.value}]Hex: {self.value.upper()}",
            # title=f"[underline bold on {self.value}]Hex[/]",
            border_style=f"bold {self.value}",
            expand=False,
            box=HEAVY_EDGE,
        )

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
