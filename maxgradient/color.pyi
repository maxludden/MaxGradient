from typing import Any, Tuple, Union

from rich.color import Color as RichColor
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from maxgradient._hex import Hex as Hex
from maxgradient._mode import Mode as Mode
from maxgradient._rgb import RGB as RGB
from maxgradient._rich import Rich as Rich
from maxgradient._x11 import X11 as X11
from maxgradient.theme import GradientTheme as GradientTheme

console: Console
VERBOSE: bool
ColorType: Union[Hex, "Color", RichColor, str, Tuple[int, int, int], X11]

class Color:
    def __init__(self, color: Any) -> None: ...
    @property
    def original(self) -> str: ...
    @property
    def red(self) -> int: ...
    @property
    def green(self) -> int: ...
    @property
    def blue(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def mode(self) -> Mode: ...
    @property
    def hex(self) -> str: ...
    @property
    def rgb(self) -> str: ...
    @property
    def rgb_tuple(self) -> Tuple[int, int, int]: ...
    @property
    def style(self) -> Style: ...
    @property
    def bg_style(self) -> Style: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self): ...
    def __rich__(self) -> Panel: ...
    def color_title(self) -> Text: ...
    def generate_name(self, color: Any) -> str: ...
    def hex_components(self, hex_str: str) -> None: ...
    def rgb_components(self, rgb_str: str) -> None: ...
    def get_contrast(self) -> str: ...
    def lighten(self, percent: float = ...) -> str: ...
    def darken(self, percent: float = ...) -> str: ...
    @classmethod
    def named_table(cls) -> Columns: ...
    @classmethod
    def color_table(cls) -> Columns: ...