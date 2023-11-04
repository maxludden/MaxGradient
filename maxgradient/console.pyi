from _typeshed import Incomplete
from datetime import datetime
from maxgradient.color import Color as Color
from maxgradient.rule import Thickness as Thickness
from pathlib import Path
from rich._log_render import FormatTimeCallable as FormatTimeCallable
from rich.align import AlignMethod as AlignMethod
from rich.console import Console as RichConsole
from rich.emoji import EmojiVariant as EmojiVariant
from rich.style import StyleType as StyleType
from rich.terminal_theme import TerminalTheme as TerminalTheme
from rich.text import Span as Span, Text as Text, TextType as TextType
from rich.theme import Theme as Theme
from typing import Callable, IO, List, Literal, Mapping, Optional, Tuple, Union

RenderableType: Incomplete
HighlighterType: Incomplete
JustifyMethod: Incomplete
OverflowMethod: Incomplete

class Singleton(type):
    def __call__(cls, *args, **kwargs) -> None: ...

class Console(RichConsole, metaclass=Singleton):
    theme: Theme
    def __init__(self, *, color_system: Optional[Literal['auto', 'standard', '256', 'truecolor', 'windows']] = ..., force_terminal: Optional[bool] = ..., force_jupyter: Optional[bool] = ..., force_interactive: Optional[bool] = ..., soft_wrap: bool = ..., theme: Optional[Theme] = ..., stderr: bool = ..., file: Optional[IO[str]] = ..., quiet: bool = ..., width: Optional[int] = ..., height: Optional[int] = ..., style: Optional[StyleType] = ..., no_color: Optional[bool] = ..., tab_size: int = ..., record: bool = ..., markup: bool = ..., emoji: bool = ..., emoji_variant: Optional[EmojiVariant] = ..., highlight: bool = ..., log_time: bool = ..., log_path: bool = ..., log_time_format: Union[str, FormatTimeCallable] = ..., highlighter: Optional[HighlighterType] = ..., legacy_windows: Optional[bool] = ..., safe_box: bool = ..., get_datetime: Optional[Callable[[], datetime]] = ..., get_time: Optional[Callable[[], float]] = ..., traceback: bool = ..., _environ: Optional[Mapping[str, str]] = ...) -> None: ...
    def gradient(self, text: Optional[str | Text] = ..., colors: Optional[List[Color | Tuple | str]] = ..., rainbow: bool = ..., invert: bool = ..., hues: Optional[int] = ..., color_sample: bool = ..., style: StyleType = ..., *, justify: Optional[JustifyMethod] = ..., overflow: Optional[OverflowMethod] = ..., no_wrap: Optional[bool] = ..., end: str = ..., tab_size: Optional[int] = ..., spans: Optional[List[Span]] = ...) -> None: ...
    def gradient_rule(self, title: TextType = ..., *, gradient: bool = ..., thickness: Thickness = ..., end: str = ..., align: AlignMethod = ...) -> None: ...
    def save_svg(self, path: str, *, title: str = ..., theme: Optional[TerminalTheme] = ..., clear: bool = ..., code_format: str = ..., font_aspect_ratio: float = ..., unique_id: Optional[str] = ...) -> None: ...
    def save_max_svg(self, path: str | Path, *, title: str = ..., theme: Optional[TerminalTheme] = ..., clear: bool = ..., code_format: str = ..., font_aspect_ratio: float = ..., unique_id: Optional[str] = ...) -> None: ...
    @staticmethod
    def get_title() -> Text: ...
    @classmethod
    def generate_example(cls) -> Text: ...
