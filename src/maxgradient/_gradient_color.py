"""Parse colors from strings."""
from typing import List, NamedTuple, Tuple
from re import compile, Pattern, IGNORECASE

from rich.box import SQUARE
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text

from maxgradient.color_triplet import ColorTriplet

console = Console()
RGB_REGEX: Pattern[str] = compile(
    r"r?g?b?\((?P<red>\d+),(?P<green>\d+),(?P<blue>\d+)\)"
)

class GradientColor(NamedTuple):
    name: str
    hex: str
    rgb: str
    triplet: ColorTriplet

    def __rich__(self) -> Table:
        """Return a rich table representation of the gradient color."""
        table = Table(box=SQUARE)
        table.add_column("Sample", justify="center")
        table.add_column("Name", justify="left")
        table.add_column("Hex", justify="center")
        table.add_column("RGB", justify="left")
        table.add_row(
            Text(" " * 10, style=Style(bgcolor=self.hex, bold=True)),
            Text(str(self.name).capitalize(), style=Style(color=self.hex, bold=True)),
            Text(str(self.hex).upper(), style=Style(color=self.hex, bold=True)),
            Text(str(self.rgb), style=Style(color=self.hex, bold=True))
        )
        return table


class GradientColors(List):
    """A class of colors used in automatically generating random gradients."""

    index: int = 0
    NAMES: Tuple[str, ...] = (
        "magenta",
        "purple",
        "blueviolet",
        "blue",
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
        "orangered",
        "red",
        "deeppink",
        "hotpink",
    )
    HEX: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#005fff",
        "#00afff",
        "#00ffff",
        "#00ffaf",
        "#00ff5f",
        "#00ff00",
        "#5fff00",
        "#afff00",
        "#ffff00",
        "#ffaf00",
        "#ff5f00",
        "#ff0000",
        "#ff005f",
        "#ff00af",
    )
    RGB: Tuple[str, ...] = (
        "rgb(255, 0, 255)",
        "rgb(175, 0, 255)",
        "rgb(95, 0, 255)",
        "rgb(0, 0, 255)",
        "rgb(0, 95, 255)",
        "rgb(0, 175, 255)",
        "rgb(0, 255, 255)",
        "rgb(0, 255, 175)",
        "rgb(0, 255, 95)",
        "rgb(0, 255, 0)",
        "rgb(95, 255, 0)",
        "rgb(175, 255, 0)",
        "rgb(255, 255, 0)",
        "rgb(255, 175, 0)",
        "rgb(255, 95, 0)",
        "rgb(255, 0, 0)",
        "rgb(255, 0, 95)",
        "rgb(255, 0, 175)",
    )
    TRIPLETS: Tuple[ColorTriplet, ...] = (
        ColorTriplet(255, 0, 255),
        ColorTriplet(175, 0, 255),
        ColorTriplet(95, 0, 255),
        ColorTriplet(0, 0, 255),
        ColorTriplet(0, 95, 255),
        ColorTriplet(0, 175, 255),
        ColorTriplet(0, 255, 255),
        ColorTriplet(0, 255, 175),
        ColorTriplet(0, 255, 95),
        ColorTriplet(0, 255, 0),
        ColorTriplet(95, 255, 0),
        ColorTriplet(175, 255, 0),
        ColorTriplet(255, 255, 0),
        ColorTriplet(255, 175, 0),
        ColorTriplet(255, 95, 0),
        ColorTriplet(255, 0, 0),
        ColorTriplet(255, 0, 95),
        ColorTriplet(255, 0, 175),
    )

    def __init__(self) -> None:
        super().__init__(
            [
                GradientColor(name, hex, rgb, triplet)
                for name, hex, rgb, triplet in zip(
                    self.NAMES, self.HEX, self.RGB, self.TRIPLETS
                )
            ]
        )

    def __getitem__(self, index: int) -> GradientColor:
        return super().__getitem__(index)

    def __len__(self) -> int:
        """Return the length of the GradientColors object."""
        return len(self)

    def __str__(self) -> str:
        """String representation of the object#"""
        return f"GradientColors<{', '.join([color.name for color in self])}"

    def __repr__(self) -> str:
        """Object representation for debugging"""
        return f"GradientColors<{', '.join([color.name for color in self])}"

    def __contains__(self, item: GradientColor) -> bool:
        """Check if an item is present in the object"""
        if not isinstance(item, GradientColor):
            return False
        else:
            return item in self

    def __rich__(self) -> Table:
        """Return a rich table representation of the gradient colors."""
        from rich.console import Console
        from rich.traceback import install as tr_install
        
        console = Console()
        tr_install(console=console)
        width = console.width-4
        
        console.print(f"Width: {width}")
        grid = Table(
            expand=True,
            width=width,
            padding=(0, 2)
        )
        grid.add_column("Sample", justify="center", width=15)
        grid.add_column("Name", justify="left", width=15)
        grid.add_column("Hex", justify="center", width=11)
        grid.add_column("RGB", justify="left", width=17)
        grid.add_column("ColorTriplet", justify="left", width=27)
        for name, hex, rgb, triplet in zip(
            self.NAMES, self.HEX, self.RGB, self.TRIPLETS
        ):
            grid.add_row(
                Text(" " * 10, style=Style(bgcolor=hex, bold=True)),
                Text(str(name).capitalize(), style=Style(color=hex, bold=True)),
                Text(str(hex).upper(), style=Style(color=hex, bold=True)),
                Text(str(rgb), style=Style(color=hex, bold=True)),
                triplet.as_text(),
            )
        return grid


    @classmethod
    def get_names(cls) -> Tuple[str, ...]:
        """Retrieve gradient colors."""
        return cls.NAMES

    @classmethod
    def get_hex(cls) -> Tuple[str, ...]:
        """Retrieve gradient hex colors."""
        return cls.HEX

    @classmethod
    def get_rgb(cls) -> Tuple[str, ...]:
        """Retrieve gradient RGB colors."""
        return cls.RGB

    @classmethod
    def get_triplets(cls) -> Tuple[Tuple[int, int, int], ...]:
        """Retrieve gradient RGB tuples."""
        return cls.TRIPLETS

    @classmethod
    def get_color(cls, color: str) -> Tuple[int, int, int]:
        """Retrieve gradient RGB tuples.

        Args:
            color (str): A gradient color.

        Returns:
            int: The index of the gradient color.
        """
        for group in [
            cls.get_names(),
            cls.get_hex(),
            cls.get_rgb(),
            cls.get_triplets(),
        ]:
            if color in group:
                index = group.index(color)
                return cls.get_triplets()[index]
            else:
                raise ValueError(f"Invalid Color: {color} not in any color group.")

        raise ValueError(f"Invalid color: {color}")

    @staticmethod
    def rgb_to_tuple(rgb: str) -> Tuple[int, int, int]:
        """Convert a rgb string to a tuple of ints"""
        rgb_match = RGB_REGEX.search(rgb, IGNORECASE)
        if rgb_match:
            red: int = int(rgb_match.group("red"))
            green: int = int(rgb_match.group("green"))
            blue: int = int(rgb_match.group("blue"))
            return (red, green, blue)
        raise ValueError(f"Invalid rgb string: {rgb}")

    @staticmethod
    def get_title() -> Text:
        """Generate a colored text title."""
        return Text.assemble(
            *[
                Text("G", style=Style(color="#ff00ff", bold=True)),
                Text("r", style=Style(color="#cf00ff", bold=True)),
                Text("a", style=Style(color="#af00ff", bold=True)),
                Text("d", style=Style(color="#8f00ff", bold=True)),
                Text("i", style=Style(color="#6f00ff", bold=True)),
                Text("e", style=Style(color="#4f00ff", bold=True)),
                Text("n", style=Style(color="#2f00ff", bold=True)),
                Text("t", style=Style(color="#0000ff", bold=True)),
                Text("C", style=Style(color="#00ccff", bold=True)),
                Text("o", style=Style(color="#00aaff", bold=True)),
                Text("l", style=Style(color="#0088ff", bold=True)),
                Text("o", style=Style(color="#006fff", bold=True)),
                Text("r", style=Style(color="#004fff", bold=True)),
                Text("s", style=Style(color="#002fff", bold=True)),
            ]
        )

    @classmethod
    def color_table(cls) -> Table:
        """Generate a table of gradient colors."""
        table = Table(title=cls.get_title(), box=SQUARE, expand=True)
        table.add_column("Sample", justify="center", style="bold")
        table.add_column("Name", justify="left", style="bold")
        table.add_column("Hex", justify="center", style="bold")
        table.add_column("RGB", justify="left", style="bold")
        table.add_column("ColorTriplet", justify="left", style="bold", width=56)
        for x in range(10):
            hex = cls.get_hex()[x]
            table.add_row(
                Text(" " * 10, style=Style(bgcolor=hex, bold=True)),
                Text(
                    str(cls.get_names()[x]).capitalize(),
                    style=Style(color=hex, bold=True),
                ),
                Text(str(cls.get_hex()[x]), style=Style(color=hex, bold=True)),
                Text(str(cls.get_rgb()[x]), style=Style(color=hex, bold=True))
            )
        return table

    @classmethod
    def as_title(cls, color: str, console: Console = console) -> Text:
        """Capitalize, format, and color a gradient color's name.

        Returns:
            text: Colorized gradient_color's capitalized name.
        """
        color = str(color).lower()
        parsed_color: str = ""
        if color in cls.NAMES:
            return Text(f"[bold {color}]{str(color).capitalize()}[/bold {color}]")
        else:
            for group in [cls.HEX, cls.RGB, cls.TRIPLETS]:
                if color in group:
                    index = group.index(color)
                    parsed_color = cls.NAMES[index]
                    break
                else:
                    continue
            return Text(
                f"[bold {parsed_color}]{str(parsed_color).capitalize()}[/bold {parsed_color}]"
            )


def print_color_table(save: bool = False) -> None:
    if save:
        console = Console(record=True, width=80)
    else:
        console = Console()

    console.line(2)
    console.print(GradientColors(), justify="center")
    console.line(2)

    if save:
        console.save_svg(
            "docs/img/gc_color_table.svg",
            title="Gradient Color Table",
        )


if __name__ == "__main__":
    print_color_table(True)
