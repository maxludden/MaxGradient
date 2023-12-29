# ruff: noqa: F401
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
from rich.console import Console as RichConsole
from rich.console import (
    ConsoleOptions,
    Group,
    JustifyMethod,
    OverflowMethod,
    RenderableType,
    RenderResult,
)
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, Task
from rich.style import Style, StyleType
from rich.text import Span, Text, TextType

import maxgradient
from maxgradient import (
    Color,
    ColorList,
    Console,
    Gradient,
    GradientRule,
    GradientTerminalTheme,
    GradientTheme,
    TintList,
)

__version__ = "0.2.15"

__all__ = [
    "Color",
    "ColorList",
    "Gradient",
    "GradientRule",
    "GradientTerminalTheme",
    "GradientTheme",
    "Console",
    "ConsoleOptions",
    "Gradient",
    "GradientRule",
    "GradientTheme",
    "GradientTerminalTheme",
    "Group",
    "JustifyMethod",
    "Layout",
    "maxgradient",
    "OverflowMethod",
    "Panel",
    "Progress",
    "RenderableType",
    "RenderResult",
    "RichConsole",
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
        "MaxGradient is a Python library for generating gradients in the terminal.",
        justify="center",
        style="bold",
    )
    console.line(2)
