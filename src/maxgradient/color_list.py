# ruff: noqa: F401
from itertools import cycle
from pathlib import Path
from random import choice, randint
from typing import Any, List, Tuple

from maxgradient.color import Color
from maxgradient.spectrum import Spectrum
from rich.columns import Columns
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console)


class ColorList(List[Color]):
    """Generate a list of colors for a gradient.

    Args:
        hues (int, optional): The number of colors in the gradient. Defaults to 4.
        title (str, optional): The title of the gradient. Defaults to "ColorList".

    Returns:
        List[Color]: A list of colors for the gradient.
    """

    COLORS: Tuple[str, ...] = (
        "#ff00ff",
        "#af00ff",
        "#5f00ff",
        "#0000ff",
        "#005fff",
        "#00afff",
        "#00ffff",
        "#00ffaf",
        "#00ff00",
        "#afff00",
        "#ffff00",
        "#ffaf00",
        "#ff5f00",
        "#ff0000",
        "#ff005f",
        "#ff00af",
    )

    def __init__(self, hues: int = 4, title: str = "ColorList"):
        self.start_index: int = randint(0, len(Spectrum.HEX))
        self.hues: int = hues
        self.title: str = title
        _color_list1: List[str] = list(self.COLORS[self.start_index :])
        _color_list2: List[str] = list(self.COLORS[: self.start_index])
        color_str_list: List[str] = _color_list1 + _color_list2
        color_list = [Color(color_str) for color_str in color_str_list]
        if self.hues > len(color_list):
            color_cycle: cycle[Color] = cycle(color_list)
            self._list: List[Color] = [next(color_cycle) for _ in range(self.hues)]
        else:
            self._list = color_list[: self.hues]
        super().__init__(self._list)

    def __call__(self) -> List[Color]:
        return [next(self) for _ in range(self.hues)]

    def __getitem__(self, index: int) -> Color:
        return Color(self.COLORS[index])

    def __getattribute__(self, __name: str) -> Any:
        return super().__getattribute__(__name)

    def __iter__(self) -> "ColorList":
        return self

    def __next__(self) -> Color:
        if not hasattr(self, "_color_cycle"):
            self._color_cycle = cycle(self._list)
        return next(self._color_cycle)

    def __repr__(self) -> str:
        return f"ColorList(hues={self.hues})"

    def __str__(self) -> str:
        return f"ColorList(hues={self.hues})"

    def __len__(self) -> int:
        return self.hues

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
        for color in self:
            name = color.name.capitalize()
            table.add_row(
                Text(" " * 10, style=color.bg_style),
                Text(
                    name, style=color.style
                ),
                Text(color.hex.upper(), style=color.style),
                Text(color.rgb, style=color.style),
            )
        return table

    @property
    def color_list(self) -> List[Color]:
        return self()

    @classmethod
    def colored_title(cls) -> Text:
        """Returns `ColorList` title with colors applied."""
        return Text.assemble(
            *[
                Text("C", style="bold.magenta"),
                Text("o", style="bold.violet"),
                Text("l", style="bold.purple"),
                Text("o", style="bold.blue"),
                Text("r", style="bold.lightblue"),
                Text("L", style="bold.cyan"),
                Text("i", style="bold.green"),
                Text("s", style="bold.yellow"),
                Text("t", style="bold.orange"),
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    console = Console(record=True)
    console.line(2)
    console.print(
        Columns([ColorList(18) for _ in range(4)], equal=True, padding=(1, 2)),
        justify="center",
    )
    console.line(2)
    try:
        console.save_svg(
            str(Path.cwd() / "docs" / "img" / "updated_color_list.svg"),
            title="Updated Color List",
        )
    except TypeError:
        pass
