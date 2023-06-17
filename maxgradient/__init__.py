"""MaxGradient is a Python library for styling and coloring terminal text with gradient color.\
    It is built on top of Rich, and is designed to work seamlessly with it.\
    It is a global singleton class that can be imported and used anywhere in the project and \
    used as a drop in replacement for [italic bold #00ffff]rich.console.Console[/].
    """
from maxgradient.color import Color
from maxgradient.gradient import Gradient

# pylint: disable=W0604
from maxgradient.log import Log, LogConsole

# from maxgradient.console import Console

__all__ = [
    "_gradient_substring",
    "_mode",
    "_rich",
    "_x11",
    "color_list",
    "color",
    "console",
    "default_styles",
    "gradient",
    "log",
    "panel",
    "theme"
]
