"""MaxGradient is a Python library for generating gradients in the terminal.

MaxGradient is a python library built on top of the great [rich](https://github.com/Textualize/rich) \
library to enable the generation of gradients in the terminal. It is inspired by the \
[lolcat](https://github.com/tehmaze/lolcat) project. MaxGradient is designed to be easy to use and \
extendable. It is also designed to be used as a library or as a command line tool.
"""
# ruff: noqa: F401
from os import environ

from dotenv import load_dotenv
from rich import inspect, print
from rich.console import ConsoleOptions, Group, RenderableType, RenderResult
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, Task
from rich.style import Style, StyleType
from rich.text import Span, Text, TextType

from maxgradient.color import Color
from maxgradient.color_list import ColorList, TintList
from maxgradient._console import Console
from maxgradient.gradient import Gradient
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.rule import GradientRule
from maxgradient.theme import GradientTerminalTheme, GradientTheme

__version__ = "0.2.4"
