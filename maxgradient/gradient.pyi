"""Types for gradient.py"""
import re
from maxgradient.color import Color as Color, ColorParseError as ColorParseError
from maxgradient.color_list import ColorList as ColorList
from maxgradient.highlighter import ColorReprHighlighter as ColorReprHighlighter
from maxgradient.log import Log
from nptyping import NDArray as NDArray, Shape as Shape
from rich.console import Console, ConsoleOptions
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType as StyleType
from rich.text import Span, Text
from typing import Any, Iterable, List, Optional, Tuple, Union, Literal


JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]
GradientMethod = Literal["default", "list", "mono", "rainbow"]

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"
WHITESPACE_REGEX: re.Pattern
VERBOSE: bool
console: Console
log: Log

class Gradient(Text):
    colors: List[Color]
    def __init__(
        self,
        text: Optional[str | Text] = ...,
        colors: Optional[List[Color | Tuple | str] | str] = ...,
        rainbow: bool = ...,
        invert: bool = ...,
        hues: Optional[int] = ...,
        color_sample: bool = ...,
        style: StyleType = ...,
        *,
        justify: Optional[str] = ...,
        overflow: Optional[str] = ...,
        no_wrap: Optional[bool] = ...,
        end: str = ...,
        tab_size: Optional[int] = ...,
        spans: Optional[List[Span]] = ...) -> None: ...
    def __add__(self, other: Any) -> Text: ...
    def __eq__(self, other: object) -> bool: ...
    def __contains__(self, other: object) -> bool: ...
    def __getitem__(self, slice: Union[int, slice]) -> Text: ...
    @property
    def cell_len(self) -> int: ...
    @property
    def text(self) -> str: ...
    @property
    def hues(self) -> int: ...
    @property
    def color_sample(self) -> bool: ...
    @property
    def style(self) -> Style: ...
    def get_colors(
        self,
        input_colors: Optional[str | List[Color | Tuple | str]],
        rainbow: bool,
        invert: bool) -> List[Color]: ...
    def mono(self, color: str | Color) -> List[Color]: ...
    def validate_colors(self, colors: Optional[List[Color]]) -> bool: ...
    def generate_gradient_substrings(self, verbose: bool = ...) -> List[Span]: ...
    def clean_spans(self, gradient_string: Text) -> List[Span]: ...
    def generate_text(self) -> str: ...
    def generate_indexes(self, verbose: bool = ...) -> List[List[int]]: ...
    def generate_substrings(self, indexes: List[List[int]], text: str) -> List[str]: ...
    def generate_substring(self, index: List[int], text: str) -> str: ...
    def __rich_console__(
        self,
        console: Console,
        options: ConsoleOptions) -> Iterable[Segment]: ...
    def __rich_measure__(
        self,
        console: Console,
        options: ConsoleOptions) -> Measurement: ...
    def render(
        self,
        console: Console,
        end: str = ...) -> Iterable['Segment']: ...
    def as_text(self) -> Text: ...

def strip_control_codes(text: str) -> str: ...
def pick_bool(value: Optional[bool], default: bool, fallback: bool) -> bool: ...
