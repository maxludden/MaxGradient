"""RGB Color Class"""
import re
from functools import _lru_cache_wrapper
from random import choice
from re import Match, Pattern
from typing import Any, Optional, Tuple

from rich.box import HEAVY_EDGE
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from maxgradient._mode import Mode
from maxgradient._rich_color import Rich

console = Console()


class InvalidComponent(ValueError):
    pass


class ColorParseError(ValueError):
    pass


class RGB:
    """RGB Color Class"""

    REGEX: Pattern[str] = re.compile(
        r"r?g?b? ?\((?P<red>\d+\.?\d*)[ ,]? ?(?P<green>\d+\.?\d*)[ ,]? ?(?P<blue>\d+\.?\d*)\)"
    )

    def __init__(self, rgb: str) -> None:
        """Create a new RGB object."""
        self.original: str | _lru_cache_wrapper = rgb
        self.value = rgb

    @property
    def original(self) -> str:  # type: ignore
        """Return the original RGB color string."""
        return self._original

    @original.setter
    def original(self, rgb: str) -> None:  # type: ignore
        """Validate and initialize the rgb value."""
        assert isinstance(rgb, str)
        self._original = rgb

    @property
    def red(self) -> int:  # type: ignore
        """Return the red component of the RGB color."""
        return self._red

    @red.setter
    def red(self, red: int | str) -> None:  # type: ignore
        """Set the red component of the RGB color."""
        self._red: int = self._parse_component(red)

    @property
    def green(self) -> int:  # type: ignore
        """Return the green component of the RGB color."""
        return self._green

    @green.setter
    def green(self, green: int | str) -> None:  # type: ignore
        """Set the green component of the RGB color."""
        self._green: int = self._parse_component(green)

    @property
    def blue(self) -> int:  # type: ignore
        """Return the blue component of the RGB color."""
        return self._blue

    @blue.setter
    def blue(self, blue: int | str) -> None:  # type: ignore
        """Set the blue component of the RGB color."""
        self._blue = self._parse_component(blue)

    @property
    def value(self) -> str:
        """Return the RGB color string."""

        return self._value

    @value.setter
    def value(self, rgb: str) -> None:
        """Validate and initialize the rgb value."""

        assert rgb is not None, "RGB value cannot be None"
        parsed_rgb = self.parse(rgb)
        if parsed_rgb is None:
            raise ValueError(f"Invalid RGB color: {rgb}")
        else:
            self._value: str = parsed_rgb

    @property
    def as_hex(self) -> str:
        """Return the RGB color string."""

        red: str = f"{self.red:02X}"
        green: str = f"{self.green:02X}"
        blue: str = f"{self.blue:02X}"
        hex: str = f"#{red}{green}{blue}"
        return hex

    @property
    def as_tuple(self) -> Tuple[int, int, int]:
        """Return the RGB color as a tuple."""
        return (int(self.red), int(self.green), int(self.blue))

    @property
    def mode(self) -> Mode:
        """Return the color mode."""
        return Mode.RGB

    @staticmethod
    def _parse_component(component: str | int) -> int:
        """Parse a string component to an integer."""
        if isinstance(component, str):
            try:
                component = int(component.strip())
            except ValueError:
                component = int(float(str(component).strip()) * 255)
            return component
        elif isinstance(component, int):
            try:
                component = int(component)
            except ValueError:
                component = int(float(component) * 255)
            return component
        else:
            raise TypeError(f"Invalid component type: {type(component)}")

    def parse(self, rgb: str) -> str:
        """Parse a string to validate it is a rgb color. If it is, \
            convert the string to a tuple of integers and return it."""
        rgb_match: Optional[Match] = self.REGEX.match(rgb)
        if rgb_match:
            red: str = rgb_match.group("red")
            self.red: int = self.validate_component(red)
            green: str = rgb_match.group("green")
            self.green: int = self.validate_component(green)
            blue: str = rgb_match.group("blue")
            self.blue: int = self.validate_component(blue)

            return f"rgb({self.red}, {self.green}, {self.blue})"
        raise ColorParseError(f"Invalid RGB color: {rgb}")

    def validate_component(self, value: str) -> int:
        """Return the interger if the component value is between 0 and 1 or 0 255.

        Args:
            value (str): the string match of a component value.
        """
        if "." in value:
            try:
                float_number = float(value)
                if float_number < 0.0:
                    raise InvalidComponent(
                        f"Invalid component: Float value is less than 0.0: {float_number}"
                    )
                elif float_number > 1.0:
                    raise InvalidComponent(
                        f"Invalid component: Float value is greater than 1.0: {float_number}"
                    )
                else:
                    return int(float_number * 255)
            except InvalidComponent as ic:
                raise InvalidComponent(
                    f"Invalid float component value: {value}"
                ) from ic
            except ValueError as ve:
                raise InvalidComponent(
                    f"Invalid float component value: {value}"
                ) from ve
            except Exception as e:
                raise InvalidComponent(
                    f"Invalid component value. Exception: {value}"
                ) from e
        else:
            try:
                int_number = int(value)
                if int_number < 0:
                    raise InvalidComponent(
                        f"Invalid component: Integer value is less than 0: {int_number}"
                    )
                elif int_number > 255:
                    raise InvalidComponent(
                        f"Invalid component: Integer value is greater than 255: {int_number}"
                    )
                else:
                    return int_number
            except InvalidComponent as ic:
                raise InvalidComponent(
                    f"Invalid float component value: {value}"
                ) from ic
            except ValueError as ve:
                raise InvalidComponent(
                    f"Invalid integer component value: {value}"
                ) from ve
            except Exception as e:
                raise InvalidComponent(
                    f"Invalid component value. Exception: {value}"
                ) from e

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __rich_repr__(self) -> Text:
        """Return a rich Text object."""

        rgb = Text("rgb", style=f"bold italic {self.as_hex}")
        left_paren = Text("(", style=f"{self.as_hex}")
        comma = Text(", ", style=f"{self.as_hex}")
        red = Text(f"{self.red}", style="bold #ff4444")
        green = Text(f"{self.green}", style="bold #44ff44")
        blue = Text(f"{self.blue}", style="bold #4444ff")
        right_paren = Text(")", style=f"{self.as_hex}")
        rgb_list = [rgb, left_paren, red, comma, green, comma, blue, right_paren]
        return Text.assemble(*rgb_list)

    def __rich__(self) -> Panel:
        """Return a rich Panel object."""
        rgb_text = self.__rich_repr__()
        return Panel(
            rgb_text,
            border_style=f"bold {self.as_hex}",
            expand=False,
            box=HEAVY_EDGE,
        )

    def __eq__(self, other: Any) -> bool:
        """Return True if the RGB color values are equal."""
        if isinstance(other, RGB):
            return self.as_tuple == other.as_tuple
        return False

    def __hash__(self) -> int:
        """Return the hash of the RGB color."""
        hash_value = 0
        name = self._original
        for char in name:
            hash_value += ord(char)
        return hash_value

    def is_valid(self) -> bool:
        """Return True if the RGB color is valid."""

        return self.parse(self.value) is not None


if __name__ == "__main__":
    rgb_str: str = choice(Rich.RGB)
    rgb = RGB(rgb_str)
    console.print(rgb)

    console.print(f"[i dim]RGB as Hex:[/]   [b {rgb.as_hex}]{rgb.as_hex}[/]")
    console.print(f"[i dim]RGB as Tuple:[/] [b {rgb.as_hex}]{rgb.as_tuple}[/]")
