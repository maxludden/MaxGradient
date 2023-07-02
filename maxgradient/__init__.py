"""MaxGradient is a Python library for styling and coloring terminal text with gradient color.\
    It is built on top of Rich, and is designed to work seamlessly with it.\
    It is a global singleton class that can be imported and used anywhere in the project and \
    used as a drop in replacement for [italic bold #00ffff]rich.console.Console[/].
    """
# pylint: disable=W0604
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table, Column
from rich.columns import Columns
from rich.highlighter import RegexHighlighter, ReprHighlighter
from rich.style import Style, StyleType

from maxgradient.theme import GradientTheme
from maxgradient.color import Color, ColorParseError
from maxgradient.console import Console, JustifyMethod, OverflowMethod
from maxgradient.gradient import Gradient, Text
from maxgradient._log import Log, LogHighlighter
