from typing import NamedTuple, Tuple

from rich.text import Text


class ColorTriplet(NamedTuple):
    """The red, green, and blue components of a color."""

    red: int
    """Red component in 0 to 255 range."""
    green: int
    """Green component in 0 to 255 range."""
    blue: int
    """Blue component in 0 to 255 range."""

    @property
    def hex(self) -> str:
        """get the color triplet in CSS style."""
        red, green, blue = self
        return f"#{red:02x}{green:02x}{blue:02x}"

    @property
    def rgb(self) -> str:
        """The color in RGB format.

        Returns:
            str: An rgb color, e.g. ``"rgb(100,23,255)"``.
        """
        red, green, blue = self
        return f"rgb({red},{green},{blue})"

    @property
    def normalized(self) -> Tuple[float, float, float]:
        """Convert components into floats between 0 and 1.

        Returns:
            Tuple[float, float, float]: A tuple of three normalized color components.
        """
        red, green, blue = self
        return red / 255.0, green / 255.0, blue / 255.0

    @property
    def text(self) -> Text:
        """Return a rich.text.Text representation of the color triplet."""
        return self.as_text()

    def as_text(self) -> Text:
        """Return a rich.text.Text representation of the color triplet."""
        left_str: str = "("
        right_str: str = ")"
        comma_str: str = ","
        left = Text(left_str, style="bold #ffffff")
        right = Text(right_str, style="bold #ffffff")
        comma = Text(comma_str, style="bold #ffffff")

        return Text.assemble(
            *[
                Text("ColorTriplet", style=f"bold {self.hex}"),
                left,
                Text(f"{self.pad_value(self.red)}", style="bold #FF0000"),
                comma,
                Text(f"{self.pad_value(self.green)}", style="bold #00AF00"),
                comma,
                Text(f"{self.pad_value(self.blue)}", style="bold #00AFFF"),
                right,
            ]
        )
    
    def __rich__(self) -> Text:
        """Return a rich text representation of the color triplet."""
        return self.as_text()

    @staticmethod
    def pad_value(value: str | int) -> str:
        """Pad a value with spaces if it is less than 3 characters long.

        Args:
            value (str): The value to pad.

        Returns:
            str: The padded value.
        """
        if isinstance(value, int):
            value = str(value)
        elif not isinstance(value, str):
            raise TypeError(f"Expected str or int, got {type(value)}")
        if len(value) < 3:
            value = f"{(' ' * (3 - len(value)))}{value}"
        return value




if __name__ == "__main__":
    from rich.console import Console
    from rich.traceback import install as tr_install

    console = Console()
    tr_install(console=console)
    console.line(2)
    console.print(ColorTriplet(175, 0, 255), justify="left")
    console.line(2)
