"""Color Mode Enum"""
from enum import Enum

from rich.text import Text


class Mode(Enum):
    """A color mode. Used to determine how a color was parsed."""

    COLOR = "COLOR"
    GC = "GC"
    HEX = "HEX"
    INIT = "INIT"
    INVALID = "INVALID"
    RGB = "RGB"
    RGB_TUPLE = "RGB_TUPLE"
    RICH_COLOR = "RICH_COLOR"
    RICH = "RICH"
    X11 = "X11"

    def __eq__(self, other: "Mode") -> bool:
        """Return True if the color mode is equal to another."""
        if isinstance(other, Mode):
            return self.value == other.value
        else:
            return False

    def __repr__(self) -> str:
        """Return a representation of the color mode."""
        return f"Mode.{str(self.value).upper()}"

    def __rich__(self) -> Text:
        """Return a rich text representation of the color mode."""
        mode = Text("Mode", style="italic #7FD6E8")
        dot = Text(".", style="bold.white")
        value: str = str(self.value).upper()
        formatted_value = Text(value, style="bold.white")
        rich_repr = Text.assemble(mode, dot, formatted_value)
        return rich_repr


if __name__ == "__main__":
    from maxgradient.log import Console

    console = Console()
    console.line()
    console.print(Mode.COLOR, justify="left")
    console.line()
