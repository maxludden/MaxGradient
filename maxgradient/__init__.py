"""MaxGradient is a Python library for styling and coloring terminal text with gradient color.\
    It is built on top of Rich, and is designed to work seamlessly with it.\
    It is a global singleton class that can be imported and used anywhere in the project and \
    used as a drop in replacement for [italic bold #00ffff]rich.console.Console[/].
    """
# pylint: disable=W0604
from rich.columns import Columns
from rich.console import Console as RichConsole
from rich.highlighter import RegexHighlighter, ReprHighlighter
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.table import Column, Table

# from maxgradient.theme import GradientTheme
from .color import Color, ColorParseError
from .color_list import ColorList
from .console import Console, JustifyMethod, OverflowMethod
from .gradient import Gradient, Text
from .log import ColorHighlighter, Log
from .rule import Rule, Thickness

__all__ = [
    "Color",
    "ColorList",
    "ColorParseError",
    "Console",
    "Gradient",
    "JustifyMethod",
    "Log",
    "OverflowMethod",
    "Rule",
    "Text",
    "Thickness",
    "Style",
    "StyleType",
    "Columns",
    "Panel",
    "Column",
    "Table",
    "ColorHighlighter"
    ]