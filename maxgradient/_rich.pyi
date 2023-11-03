"""Types for _rich.py"""
from maxgradient.log import Log
from rich.table import Table
from rich.text import Text
from rich.console import Console
from typing import Tuple, Optional

console: Console
log: Log

class Rich:
    NAMES: Tuple[str, ...]
    HEX: Tuple[str, ...]
    RGB: Tuple[str, ...]
    RGB_TUPLE: Tuple[Tuple[int, int, int], ...]
    @classmethod
    def get_names(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_hex(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_rgb(cls) -> Tuple[str, ...]: ...
    @classmethod
    def get_color(cls, color: str) -> Optional[Tuple[int, int, int]]: ...
    @staticmethod
    def rgb_to_tuple(rgb: str) -> Tuple[int, int, int]: ...
    @staticmethod
    def get_title() -> Text: ...
    @staticmethod
    def sample_title() -> Text: ...
    @staticmethod
    def name_title() -> Text: ...
    @staticmethod
    def hex_title() -> Text: ...
    @staticmethod
    def rgb_title() -> Text: ...
    @classmethod
    def color_table(cls) -> Table: ...
    @classmethod
    def print_class_table(cls, save: bool = ...) -> None: ...
