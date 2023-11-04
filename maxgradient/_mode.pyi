from enum import Enum
from rich.text import Text

class Mode(Enum):
    COLOR: str
    GC: str
    HEX: str
    INIT: str
    INVALID: str
    RGB: str
    RGB_TUPLE: str
    RICH_COLOR: str
    RICH: str
    X11: str
    def __eq__(self, other: Mode) -> bool: ...
    def __rich__(self) -> Text: ...
