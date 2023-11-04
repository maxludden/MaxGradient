from _typeshed import Incomplete
from rich.highlighter import RegexHighlighter
from typing import Tuple

NAMES: Tuple[str, ...]
HEX: Tuple[str, ...]
HEX3: Tuple[str, ...]
RGB: Tuple[str, ...]
RGB_TUPLE: Tuple[Tuple[int, int, int], ...]

class ColorReprHighlighter(RegexHighlighter):
    base_style: str
    highlights: Incomplete
