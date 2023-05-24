from io import StringIO
from typing import List, Tuple, Optional

import numpy as np
from cheap_repr import normal_repr, register_repr
from lorem_text import lorem
from rich import inspect, print
from rich.columns import Columns
from rich.console import Console
from rich.control import strip_control_codes
from rich.panel import Panel
from rich.style import Style, StyleStack
from rich.table import Table
from rich.layout import Layout
from rich.text import Span, Text
from snoop import pp, snoop

from maxgradient.color import Color
from maxgradient.theme import GradientTheme

register_repr(Panel)(normal_repr)

console = Console(theme=GradientTheme())
buffer = StringIO()
buffer.write(lorem.paragraphs(5))
TEXT = buffer.getvalue()
COLORS = ["red", "orange", "yellow"]
VERBOSE = True


# def split_string(string: str = TEXT, num_chunks: int = len(COLORS) - 1):
#     chunk_sizes = np.array_split(range(len(string)), num_chunks)
#     # inspect(chunk_sizes, all=True)
#     chunks = [
#         string[start:end] for start, end in zip(chunk_sizes[:-1], chunk_sizes[1:])
#     ]
#     return chunks
class Substrings:
    """A custom class to generate random text via lorem_text."""

    @property
    def text(self) -> str:
        """Return the text."""
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Set the text."""
        self._text = text

    @property
    def colors(self) -> List[Color]:
        """Return the colors."""
        return self._colors

    @colors.setter
    def colors(self, colors: List[str|Tuple[int,int,int|Color]]) -> None:
        """Validate and set the colors of each substring."""
        if colors:
            if len(colors) > 1:
                self._colors = []
                for color in colors:
                    if isinstance(color, str):
                        self._colors.append(Color(color))
                    elif isinstance(color, tuple):
                        self._colors.append(Color(color))
                    elif isinstance(color, Color):
                        self._colors.append(color)
                    else:
                        raise TypeError("Invalid color type.")
            else:
                raise ValueError(
                    f"Must provide more than one color. Colors provided: {len(colors)}"
                )
        else:
            raise ValueError("No colors provided. Must provide at least two colors.")

    @property
    def length(self) -> int:
        """Return the length of the text."""
        return len(strip_control_codes(self.text))

    def __init__(self, text: Optional[str] = None, paragraphs: int = 5) -> str:
        """Creates substrings from a string. If no string is provided, a random string is
            generated via lorem_text. Defaults to 5 paragraphs.

        Args:
            text (str, optional): A string to generate substrings from. Defaults to None.
            paragraphs (int, optional): Number of paragraphs to generate. Defaults to 5.
        """
        if text is not None:
            self.text = text
        buffer = StringIO()
        buffer.write(lorem.paragraphs(paragraphs))
        self.text = buffer.getvalue()

    def __rich__(self) -> Panel:
        """Generate a panel containing the generated text"""
        return Panel(
            Text(self.text, justify="left"),
            border_style="bold #5f00ff",
            title="[#DD88FF]Generated Text[/]",
            subtitle=f"[dim #af00ff]Text Length:[/][dim #bbbbbb] {self.length}[/]",
            subtitle_align="right",
            width=int(console.width * 0.8),
            padding=(1, 4),
        )

    def __call__(self, text: Optional[str] = None, paragraphs: int = 5) -> str:
        """Generate paragraphs of lorem ipsum text.

        Args:
            paragraphs (int, optional): Number of paragraphs to generate. Defaults to 5.
        """
        return self.__init__(paragraphs=paragraphs)

    def get_substring_indexes(self, print: bool = False) -> List[Tuple]:
        """Return an array of chunk sizes."""
        num_of_substrings=len(COLORS)-1
        substring_sizes = np.array_split(range(self.length), num_of_substrings)
        substring_indexes: List[Tuple[int, int]] = []
        for index, substring_size in enumerate(substring_sizes):
            start = substring_size[0]
            end = substring_size[-1]
            substring_indexes.append((start, end))
            if print:
                if index == 0:
                    chunk_table = Table(
                        title="[b dim #5f00ff]Substring Indexes[/]\n",
                        border_style="dim #cccccc",
                        show_edge=False,
                        show_lines=False,
                        padding=(0, 1),
                        width=int(console.width * 0.3)
                    )
                    chunk_table.add_column(
                        "[b i #0088ff]Chunk[/]",
                        ratio=1,
                        min_width=7,
                        justify="center",
                        style="bold #00ffff",
                        no_wrap=True
                    )
                    chunk_table.add_column(
                        "[b i #00ff00]Start[/]",
                        ratio=3,
                        justify="center",
                        style="bold #bbffbb",
                    )
                    chunk_table.add_column(
                        "[b i #ff0000]End[/]",
                        ratio=3,
                        justify="center",
                        style="bold #ff8888",
                    )
                chunk_table.add_row(f"{index}", f"{start}", f"{end}")
                if index + 1 == len(substring_sizes):
                    console.line(2)
                    console.print(chunk_table, justify="center")
        return substring_indexes

    def get_substrings(self, print: bool = False):
        """Return an array of substrings."""
        substring_indexes = self.get_substring_indexes()
        substrings = []
        for start, end in substring_indexes:
            substrings.append(self.text[start:end])
        if print:
            substring_panels: List[Panel] = []
            for index, substring in enumerate(substrings):
                subtitle_start = f"[dim #009C00]{substring_indexes[index][0]}[/]"
                hyphen = f"[dim #cccccc] - [/]"
                subtitle_end = f"[dim #7D0000]{substring_indexes[index][1]}[/]"
                subtitle = Text.from_markup(f"{subtitle_start}{hyphen}{subtitle_end}")
                substring_panels.append(
                    Panel(
                        Text(substring, justify="left"),
                        border_style="bold #5f00ff",
                        title=f"[b #DD88FF]Substring {index+1}[/]",
                        subtitle=subtitle,
                        subtitle_align="right",
                        width=int(console.width * 0.4),
                        padding=(1, 4),
                    )
                )
            console.print(Columns(substring_panels, equal=True), justify="center")
        return substrings

    def substring_gradients(self, print: bool = False) -> List[Text]:
        """Return an array of substrings with gradients."""
        substrings = self.get_substrings()
        substring_gradients: List[Text] = []
        for index, substring in enumerate(substrings):
            substring_gradients.append(
                Text(
                    substring,
                    style=f"bold {COLORS[index]} on {COLORS[index+1]}",
                    justify="left",
                )
            )
        if print:
            console.print(Columns(substring_gradients, equal=True), justify="center")
        return substring_gradients

if __name__ == "__main__":
    console.clear()
    console.line(3)

    # text
    TEXT = Substrings()
    console.print(TEXT, justify="center")
    TEXT.get_substring_indexes(print=True)
    TEXT.get_substrings(print=True)
