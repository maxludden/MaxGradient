from rich.table import Table as Table
from rich.text import Text as Text
from typing import Optional, Tuple

class X11:
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
    def rgb_to_tuple(rgb: str) -> Optional[Tuple[int, int, int]]: ...
    @staticmethod
    def get_title() -> Text: ...
    @staticmethod
    def sample_title() -> Text: ...
    def __rich__(self) -> Table: ...
    @classmethod
    def color_table(cls) -> Table: ...
    @classmethod
    def print_color_table(cls, save: bool = ...) -> None: ...
