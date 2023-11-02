"""Types for _gc.py"""
from typing import Optional, Tuple

from rich.console import Console
from rich.table import Table
from rich.text import Text

from maxgradient._mode import Mode as Mode
from maxgradient.log import Log as Log

console: Console
log: Log

class GradientColor:
    mode: Mode
    NAMES: Tuple[str, ...]
    HEX: Tuple[str, ...]
    HEX3: Tuple[str, ...]
    RGB: Tuple[str, ...]
    RGB_TUPLE: Tuple[Tuple[int, int, int], ...]
    @classmethod
    def get_names(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_hex(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_rgb(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_rgb_tuple(cls) -> Tuple[Tuple[int, int, int]]: ...
    @classmethod
    def get_color(cls, color: str) -> Optional[Tuple[int, int, int]]: ...
    @staticmethod
    def rgb_to_tuple(rgb: str) -> Tuple[int, int, int]: ...
    @staticmethod
    def get_title() -> Text: ...
    @classmethod
    def color_table(cls) -> Table: ...
    @classmethod
    def as_title(cls, color: str) -> Text: ...

def print_color_table(save: bool = ...) -> None: ...
