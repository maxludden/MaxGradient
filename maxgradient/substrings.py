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

    def __call__(self, paragraphs: int = 5) -> str:
        """Generate paragraphs of lorem ipsum text.

        Args:
            paragraphs (int, optional): Number of paragraphs to generate. Defaults to 5.
        """
        buffer = StringIO()
        buffer.write(lorem.paragraphs(paragraphs))
        self.text = buffer.getvalue()
        return self.text

    def get_chunk_indexes(self, print: bool = False) -> List[Tuple]:
        """Return an array of chunk sizes."""
        chunk_sizes = np.array_split(range(self.length), len(COLORS) - 1)
        chunk_indexes: List[Tuple[int, int]] = []
        for index, chunk_size in enumerate(chunk_sizes):
            start = chunk_size[0]
            end = chunk_size[-1]
            chunk_indexes.append((start, end))
            if print:
                if index == 0:
                    chunk_table = Table(
                        title="[bold dim #5f00ff]Chucked Indexes[/]\n",
                        border_style="dim #ffffff",
                        show_edge=False,
                        show_lines=False,
                        padding=(0, 1),
                        width=int(console.width * 0.3),
                    )
                    chunk_table.add_column(
                        "[bold #08f]Chunk[/]",
                        ratio=1,
                        min_width=7,
                        justify="center",
                        style="bold #00ffff",
                    )
                    chunk_table.add_column(
                        "[b i #00ff00]Start[/]",
                        ratio=7,
                        justify="center",
                        style="bold #bbffbb",
                    )
                    chunk_table.add_column(
                        "[b i #ff0000]End[/]",
                        ratio=7,
                        justify="center",
                        style="bold #ff8888",
                    )
                chunk_table.add_row(f"{index}", f"{start}", f"{end}")
                if index + 1 == len(chunk_sizes):
                    console.line(2)
                    console.print(chunk_table, justify="center")
        return chunk_indexes


if __name__ == "__main__":
    console.clear()
    console.line(3)

    # text
    TEXT = Substrings()
    console.print(TEXT, justify="center")
    TEXT.get_chunk_indexes(print=True)
