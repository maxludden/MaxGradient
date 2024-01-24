# ruff: noqa: F401
from itertools import cycle
from pathlib import Path
from random import choice, randint, sample
from typing import Any, List, Tuple, Dict, Optional

from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

from gradient.color import Color, COLORS_BY_NAME, ColorTuple


console = Console()
tr_install(console=console)

class ColorList(List[Color]):
    COLORS: Tuple[str, ...] = (
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
        "lawngreen",
        "greenyellow",
        "yellow",
        "orange",
        "orangered",
        "red",
        "deeppink",
        "hotpink"
    )

    def __init__(self, hues: int = 18, start: Optional[str] = None, invert: Optional[bool] = None, title: str = "ColorList"):
        if start:
            assert start in self.COLORS, "Invalid start color"
            self.start_index: int = self.COLORS.index(start)
        else:
            self.start_index = randint(0, len(self.COLORS) - 1)
        self.hues: int= hues
        self.title: str = title
        if invert is None:
            invert = choice([True, False])
        self.invert = invert
        _color_list1: List[str]
        _color_list2: List[str]
        if self.invert:
            _color_list1 = list(self.COLORS[:self.start_index])
            _color_list2 = list(self.COLORS[self.start_index:])
        else:
            _color_list1 = list(self.COLORS[self.start_index:])
            _color_list2 = list(self.COLORS[:self.start_index])

        color_str_list: List[str] = _color_list1 + _color_list2
        color_list = [Color(color_str) for color_str in color_str_list]
        if self.hues > len(color_list):
            color_cycle: cycle[Color] = cycle(color_list)
            super().__init__([next(color_cycle) for _ in range(self.hues)])
        else:
            super().__init__(color_list[:self.hues])


    @property
    def current_index(self) -> int:
        if not hasattr(self, "_current_index"):
            self._current_index = 0
        return self._current_index
    
    @current_index.setter
    def current_index(self, value: int) -> None:
        self._current_index = value

    def __call__(self) -> List[Color]:
        return [next(self) for _ in range(self.hues)]

    def __iter__(self) -> 'ColorList':
        return self

    def __next__(self) -> Color:
        if self.current_index >= len(self):
            self.current_index = 0  # Reset index if we reached the end
        result = self[self.current_index]
        self.current_index += 1
        return result
    
    def __repr__(self) -> str:
        return f"ColorList(hues={self.hues})"
    
    def __str__(self) -> str:
        return f"ColorList(hues={self.hues})"
    
    def __len__(self) -> int:
        return self.hues

    def __rich__(self) -> Table:
        table = Table(
            "Hex", "Name", "Hex",
            title=ColorList.colored_title(),
            show_header=False,
            expand=False,
            padding=(0, 1),
        )
        for color in self:
            table.add_row(
                Text(f" {str(color.as_named()).capitalize()} ", style=color.as_bg_style()),
                Text(str(color.hex).upper(), style=f"bold {color.as_style()}"),
                Text(color.hex.upper()
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
                Text("C", style="bold #ff00ff"),
                Text("o", style="bold #af00ff"),
                Text("l", style="bold #5f00ff"),
                Text("o", style="bold #0000ff"),
                Text("r", style="bold #005fff"),
                Text("L", style="bold #00afff"),
                Text("i", style="bold #00ffff"),
                Text("s", style="bold #00ffaf"),
                Text("t", style="bold #00ff5f")
            ]
        )

if __name__=="__main__":
    console=Console(record=True)
    console.line(2)
    start_colors = ["red", "green", "blue", "yellow"]
    console.print(
        Columns(
            [ColorList(start=color) for color in start_colors],
            equal=True,
            padding=(1,2)
        ),
        justify="center"
    )
    console.line(2)
    path: str = str((Path.cwd() / "docs" / "img" / "color_list_v2.svg"))
    
    try:
        console.save_svg(
            path,
            title="Updated Color List"   
        )
    except TypeError:
        pass
