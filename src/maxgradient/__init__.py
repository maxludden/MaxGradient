"""MaxGradient is a Python library for generating gradients in the terminal.

MaxGradient is a python library built on top of the great \
    [rich](https://github.com/Textualize/rich) library to \
    enable the generation of gradients in the terminal. It \
    is inspired by the [lolcat](https://github.com/tehmaze/lolcat) \
    project. MaxGradient is designed to be easy to use and \
    extendable. It is also designed to be used as a library \
    or as a command line tool.
"""
# ruff: noqa: F401
from os import environ
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from rich.console import JustifyMethod, OverflowMethod, RenderableType, RenderResult
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, Task
from rich.style import Style, StyleType
from rich.text import Span, Text, TextType

from maxgradient._color_list import ColorList, TintList
from maxgradient._gradient_color import GradientColor
from maxgradient.color import Color
from maxgradient.console import Console, ConsoleOptions, Group
from maxgradient.gradient import Gradient
from maxgradient.rule import GradientRule
from maxgradient.theme import GradientTerminalTheme, GradientTheme

__version__ = "0.2.17"

__all__ = [
    "Color",
    "ColorList",
    "Gradient",
    "GradientRule",
    "GradientTerminalTheme",
    "GradientTheme",
    "GradientColor",
    "Console",
    "ConsoleOptions",
    "Gradient",
    "GradientRule",
    "GradientTheme",
    "GradientTerminalTheme",
    "Group",
    "JustifyMethod",
    "Layout",
    "OverflowMethod",
    "Panel",
    "Progress",
    "RenderableType",
    "RenderResult",
    "Span",
    "Style",
    "StyleType",
    "Task",
    "Text",
    "TextType",
    "Console",
    "TintList",
]

if __name__ == "__main__":
    console = Console()
    console.line(2)
    console.gradient(
        "MaxGradient is a python library for printing gradients in the terminal.",
        rainbow=True,
        justify="center",
        style="bold",
    )
    console.line(2)
