"""Types for default_styles.py"""
from typing import Dict, Mapping

from rich.style import Style
from rich.style import StyleType as StyleType
from rich.table import Table
from rich.text import Text

GRADIENT_STYLES: Mapping[str, StyleType]
EDITED_STYLES: Dict[str, str]

def get_default_styles() -> dict[str, Style]: ...
def formatted_title() -> Text: ...
def styles_table() -> Table: ...
def example() -> None: ...
