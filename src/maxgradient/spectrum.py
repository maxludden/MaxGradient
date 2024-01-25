from __future__ import annotations

from typing import List, Tuple

from rich.color import Color
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console, show_locals=True)


class Spectrum(List[Color]):
    """The colors from which to create random gradients."""

    NAMES: Tuple[str, ...] = (
        "magenta",
        "purple",
        "blueviolet",
        "blue",
        "babyblue",
        "lightblue",
        "skyblue",
        "cyan",
        "springgreen",
        "green",
        "lime",
        "chartreuse",
        "greenyellow",
        "yellow",
        "orange",
        "darkorange",
        "tomato",
        "red",
        "deeppink",
        "hotpink",
    )

    HEX = (
        "#FF00FF",
        "#AF00FF",
        "#5F00FF",
        "#0000FF",
        "#0055FF",
        "#0087FF",
        "#00C3FF",
        "#00FFFF",
        "#00FFAF",
        "#00FF7D",
        "#00FF00",
        "#87FF00",
        "#AFFF00",
        "#FFFF00",
        "#FFAF00",
        "#FF8700",
        "#FF4B00",
        "#FF0000",
        "#FF005F",
    )

    def __init__(self) -> None:
        global COLORS
        COLORS = [Color.parse(hex) for hex in self.HEX]
        super().__init__(COLORS)

    def __rich__(self) -> Table:
        table = Table(
            "[b i #ffffff]Sample[/]",
            "[b i #ffffff]Name[/]",
            "[b i #ffffff]Hex[/]",
            "[b i #ffffff]RGB[/]",
            title="Gradient Colors",
            show_footer=False,
            show_header=True,
        )
        for color in COLORS:
            assert color.triplet, "ColorTriplet must not be None"
            triplet = color.triplet
            hex_str = triplet.hex.upper()
            if hex_str in [
                "#AF00FF",
                "#5F00FF",
                "#0000FF",
                "#0055FF",
            ]:
                foreground = "#ffffff"
            else:
                foreground = "#000000"
            bgstyle = Style(color=foreground, bgcolor=hex_str, bold=True)
            style = Style(color=hex_str, bold=True)
            index = self.HEX.index(hex_str)
            name = self.NAMES[index].capitalize()
            table.add_row(
                Text(" " * 10, style=bgstyle),
                Text(name, style=style),
                Text(hex_str, style=style),
                Text(triplet.rgb, style=style),
            )
        return table


if __name__ == "__main__":
    console = Console()
    console.print(Spectrum(), justify="center")
    console.print(Spectrum(), justify="center")
