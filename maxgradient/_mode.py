"""Color Mode Enum"""
from enum import Enum
from rich.text import Text
class Mode(Enum):
    """A color mode. Used to determine how a color was parsed."""

    COLOR = "COLOR"
    NAMED = "NAMED"
    X11 = "X11"
    RICH = "RICH"
    HEX = "HEX"
    RGB = "RGB"
    RGB_TUPLE = "RGB_TUPLE"

    @property
    def color_mode(self) -> str:
        """Return the color mode."""
        if self.value == Mode.COLOR:
            return str("color")
        if self.value == Mode.NAMED:
            return str("named")
        elif self.value == Mode.X11:
            return str("x11")
        elif self.value == Mode.RICH:
            return str("rich")
        elif self.value == Mode.HEX:
            return str("hex")
        elif self.value == Mode.RGB:
            return str("rgb")
        elif self.value == Mode.RGB_TUPLE:
            return str("rgb_tuple")
        else:
            raise ValueError(f"Invalid mode: {self}")

    def __eq__(self, other: "Mode") -> bool:
        """Return True if the color mode is equal to another."""
        if isinstance(other, Mode):
            return self.value == other.value
        elif isinstance(other, str):
            return self.color_mode == other
        else:
            return False

    def __repr__(self) -> str:
        """Return a representation of the color mode."""
        return f"Mode.{str(self.value).upper()}"

    def __rich_repr__(self) -> Text:
        """Return a rich text representation of the color mode."""
        mode = Text("Mode", style="bold italic #7FD6E8")
        dot = Text(".", style="bold.white")
        value: str = str(self.value).upper()
        formatted_value = Text(value, style="bold lime")
        rich_repr = Text.assemble(mode, dot, formatted_value)
        return rich_repr

    def __rich__(self) -> Text:
        """Return a rich text representation of the color mode."""
        return self.__rich_repr__()