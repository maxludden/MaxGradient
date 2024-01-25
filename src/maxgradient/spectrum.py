from __future__ import annotations

# ruff: noqa: F401
import math
import re
from colorsys import hls_to_rgb, rgb_to_hls
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    cast,
)

from pydantic import GetJsonSchemaHandler
from pydantic._internal import _repr
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
from pydantic_extra_types.color import ColorTuple, ColorType
from rich.color import Color as RichColor
from rich.color import ColorParseError, blend_rgb
from rich.color_triplet import ColorTriplet
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install

from maxgradient.color import RGBA, Color

console = Console()
tr_install(console=console, show_locals=True)


class Spectrum(List[Color]):
    def __init__(self) -> None:
        HEX = (
            "#FF00FF",
            "#AF00FF",
            "#5F00FF",
            "#0000FF",
            "#0055FF",
            "#0087FF",
            "#00C3FF",
            "#00FFFF",
            "#00FFAF",
            "#00FF7D",
            "#00FF00",
            "#87FF00",
            "#AFFF00",
            "#FFFF00",
            "#FFAF00",
            "#FF8700",
            "#FF4B00",
            "#FF0000",
            "#FF005F",
        )
        global COLORS
        COLORS = [Color(hex) for hex in HEX]
        super().__init__()
        self.append(COLORS)

    def __rich__(self) -> Table:
        table = Table(
            "[b i #ffffff]Sample[/]",
            "[b i #ffffff]Name[/]",
            "[b i #ffffff]Hex[/]",
            "[b i #ffffff]RGB[/]",
            title="Gradient Colors",
            show_footer=False,
            show_header=True,
        )
        for color in COLORS:
            table.add_row(
                Text(" " * 10, style=color.as_bg_style(bold=True)),
                Text(
                    str(color.as_named(fallback=True)), style=color.as_style(bold=True)
                ),
                Text(str(color.hex).upper(), style=color.as_style(bold=True)),
                Text(str(color.as_rgb()), style=color.as_bg_style(bold=True)),
            )
        return table


if __name__ == "__main__":
    console = Console()
    console.print(Spectrum())
