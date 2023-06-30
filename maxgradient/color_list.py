"""Generates a spectrum of colors for use in gradient generation."""
from itertools import cycle
from random import randint
from typing import List

from rich.table import Table
from rich.text import Text

from maxgradient.color import Color
from maxgradient.log import Log, LogConsole

console = LogConsole()
log = Log(console)


class ColorList(list):
    """ColorList is a list of colors. It is used to generate a spectrum of\
        colors for use in gradient generation. It consists of a list of\
        `Color` objects."""

    colors: List[str] = [
        "magenta",
        "violet",
        "purple",
        "blue",
        "lightblue",
        "cyan",
        "lime",
        "yellow",
        "orange",
        "red",
    ]

    def __init__(self, hues: int = 3, invert: bool = False):
        super().__init__()
        self.color_list: List[Color] = []
        start_index = randint(0, 9)
        random_colors: List[str] = []
        step = -1 if invert else 1
        for index in range(10):
            current = start_index + (index * step)
            if current > 9:
                current -= 10
            if current < 0:
                current += 10
            random_colors.append(self.colors[current])
        color_cycle = cycle(random_colors)
        for _ in range(hues):
            color = Color(next(color_cycle))
            self.color_list.append(color)
            if color is None:
                break
        # return self.color_list

    def __call__(self):
        return self.color_list

    def __getitem__(self, index):
        return self.color_list[index]

    def __len__(self):
        return len(self.color_list)

    def reverse(self):
        self.color_list.reverse()

    def get_first_color(self):
        """Return the first color in the list."""
        return self.color_list[0]

    def get_last_color(self):
        """Return the last color in the list."""
        return self.color_list[-1]

    @classmethod
    def colored_title(cls) -> Text:
        """Returns `ColorList` title with colors applied."""
        title = [
            Text("C", style="bold.magenta"),
            Text("o", style="bold.violet"),
            Text("l", style="bold.purple"),
            Text("o", style="bold.blue"),
            Text("r", style="bold.lightblue"),
            Text("L", style="bold.cyan"),
            Text("i", style="bold.lime"),
            Text("s", style="bold.yellow"),
            Text("t", style="bold.orange"),
        ]
        return Text.assemble(*title)

    def __rich__(self) -> Table:
        table = Table(
            title=self.colored_title(),
            show_header=False,
            expand=False,
            padding=(0, 1),
        )
        for color in self.color_list:
            table.add_row(
                Text(str(color.name).capitalize(), style=f"bold {color.bg_style}")
            )
        return table


if __name__ == "__main__":
    color_list = ColorList(invert=True, hues=10)
    console.line(2)
    console.print(color_list, justify="center")

    last_color = color_list.get_last_color()
    last_color_color = f"[{last_color.style}]{last_color.name.capitalize()}[/]"
    console.print(
        f"[{last_color.style}]Last Color:[/] {last_color_color}",
        justify="center",
    )
