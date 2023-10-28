"""Types for theme.py"""
from maxgradient.highlighter import RegexHighlighter as RegexHighlighter
from rich.style import Style, StyleType
from rich.table import Table as Table
from rich.terminal_theme import TerminalTheme
from rich.theme import Theme
from typing import Dict, Mapping, Optional

class GradientTheme(Theme):
    styles: Dict[str, Style]
    def __init__(
        self,
        styles: Optional[Mapping[str, StyleType]] = ...,
        inherit: bool = ...) -> None: ...
    def __rich__(self) -> str: ...
    def __getitem__(self, name: str) -> Style: ...
    @classmethod
    def get_theme_table(cls) -> Table: ...

class GradientTerminalTheme(TerminalTheme):
    def __init__(self) -> None: ...
