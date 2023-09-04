"""Import the classes from the different modules of gradient"""
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
from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.rule import GradientRule
from maxgradient.theme import GradientTerminalTheme, GradientTheme

__version__ = "0.1.5"
