from itertools import cycle
from random import randint
from typing import List

from rich.table import Table
from rich.text import Text

from examples.color import Color


class ColorList(list):
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
        return self.color_list[0]

    def get_last_color(self):
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
                Text(str(color._original).capitalize(), style=f"bold {color.bg_style}")
            )
        return table


if __name__ == "__main__":
    from rich.console import Console
    from rich.style import Style

    from examples.color import Color
    from maxgradient.theme import GradientTheme

    console = Console(theme=GradientTheme())
    color_list = ColorList(invert=True, hues=10)
    console.line(2)
    console.print(color_list, justify="center")

    last_color = color_list.get_last_color()
    console.print(
        f"[{last_color.style}]Last Color:[/] [bold {last_color.bg_style}]{str(last_color._original).capitalize()}[/]",
        justify="center",
    )
