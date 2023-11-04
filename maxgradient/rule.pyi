from maxgradient.color import Color as Color
from maxgradient.log import Log as Log
from rich.align import AlignMethod as AlignMethod
from rich.console import Console as Console, ConsoleOptions as ConsoleOptions, RenderResult as RenderResult
from rich.jupyter import JupyterMixin
from rich.measure import Measurement as Measurement
from rich.text import Text as Text
from typing import List, Literal, Union

Thickness: Literal['thin', 'medium', 'thick']
console: Console
log = Log

class GradientRule(JupyterMixin):
    gradient: bool
    title: Union[str, Text]
    end: str
    align: AlignMethod
    left_colors: List[Color]
    right_colors: List[Color]
    def __init__(self, title: Union[str, Text] = ..., *, gradient: bool = ..., thickness: Literal['thin', 'medium', 'thick'] = ..., end: str = ..., align: AlignMethod = ...) -> None: ...
    title_text: Text
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult: ...
    side_width: int
    def center_rule(self, rule_text: Text, truncate_width: int, chars_len: int, width: int) -> Text: ...
    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement: ...
    @property
    def thickness(self) -> None: ...
    @property
    def characters(self) -> str: ...
    @classmethod
    def rule_example(cls) -> None: ...
