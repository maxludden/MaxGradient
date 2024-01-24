#ruff: noqa: F401
import colorsys
import re
from functools import singledispatchmethod
from re import Match
from typing import Any, List, Optional, Tuple, TypeAlias, Union

from rich.box import HEAVY, SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError, blend_rgb
from rich.color_triplet import ColorTriplet
from rich.columns import Columns
from rich.console import Console, JustifyMethod
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install
import numpy as np

from maxgradient._gradient_color import GradientColor
from maxgradient._hex_color import Hex
from maxgradient._mode import Mode
from maxgradient._rgb_color import RGB
from maxgradient._rich_color import Rich
from maxgradient._x11_color import X11
from maxgradient.theme import GradientTheme

console = Console()
tr_install(console=Console(), show_locals=True)
VERBOSE: bool = False
ColorType: TypeAlias = Union[Hex, RichColor, str, ColorTriplet, X11]

class Color:
    """A color that may be used to style renderables for the Console or
from which to generate a gradient. Colors can be parse from a number
of inputs:

# GradientColor

The colors from which random gradients are generated. Can be parsed
from the GradientColor's name, hex color code, RGB color code, or
ColorTriplet.

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      GradientColor Examples                       ┃
┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┫
┃  Color Names  ┃   Hex Color   ┃     RGB Color     ┃ ColorTriplet  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│       Magenta │   '#ff00ff'   │  rgb(255,0,255)   │  (255,0,255)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│        Purple │   '#af00ff'   │  rgb(175,0,255)   │  (165,0,255)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│       Violet  │   '#5f00ff'   │  rgb(95,0,255)    │  (95,0,255)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│          Blue │   '#0000ff'   │  rgb(0,0,255)     │  (0,0,255)    │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│     Lightblue │   '#005fff'   │  rgb(0,95,255)    │  (0,95,255)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│       Skyblue │   '#00afff'   │  rgb(0, 175, 255) │  (0,175,255)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│          Cyan │   '#00ffff'   │  rgb(0,255,255)   │  (0,0,255)    │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│   springgreen │   '#00ffaf'   │  rgb(0,255,175)   │  (0,255,175)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│         green │   '#00ff5f'   │  rgb(0,255,95)    │  (0,255,95)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│          lime │   '#00ff00'   │  rgb(0,255,0)     │  (0,255,0)    │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│    chartreuse │   '#5fff00'   │  rgb(95,255,0)    │  (95,255,0)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│   greenyellow │   '#afff00'   │  rgb(175,255,0)   │  (75,255,255) │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│        Yellow │   '#ffff00'   │  rgb(255,255,0)   │  (255,255,0)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│        Orange │   '#ffaf00'   │  rgb(255,175,0)   │  (255,175,0)  │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│     Orangered │   '#ff5f00'   │  rgb(255,95,0)    │  (255,95,0)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│           Red │   '#ff0000'   │  rgb(255,0,0)     │  (255,0,0)    │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│      Deeppink │   '#ff005f'   │  rgb(255,0,95)    │  (255,0,95)   │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│       Hotpink │   '#ff00af'   │  rgb(255,0,175)   │  (255,0,175)  │
└───────────────┴───────────────┴───────────────────┴───────────────┘
```

# RichColors

The rich library's:\n
    - name\n
    - hex color code\n
    - rgb color code\n
    - rich.color_triplet.ColorTriplet\n

## Examples:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      Rich Colors Examples                         ┃
┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┫
┃  Color Names  ┃   Hex Color   ┃     RGB Color     ┃ ColorTriplet  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│        Blue1  │   '#0000ff'   │  rgb(0,0,255)     │ (0,0,255)     │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│        Grey0  │   '#000000'   │  rgb(0,0,0)       │ (0,0,0)       │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│    honeydew2  │   '#d7ffd7'   │  rgb(215,255,215) │ (215,255,215) │
└───────────────┴───────────────┴───────────────────┴───────────────┘
```
For a complete list of rich colors run the following script:

    ```
    python -m maxgradient._rich
    ```

You can also visit the rich library's documentation to view all
of the colors at the following link: [rich standard colors](https://rich.readthedocs.io/en/latest/appendix/colors.html)

# X11 Colors

May be entered by their name, hex color code, or ColorTriplet.

---

## Examples:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                       X11 Colors Examples                         ┃
┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┫
┃  Color Names  ┃   Hex Color   ┃     RGB Color     ┃   RGB Tuple   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│   powderblue  │   '#b0e0e6'   │  rgb(176,224,230) │ (176,224,230) │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│       salmon  │   '#fa8072'   │  rgb(250,128,114) │ (250,128,114) │
├───────────────┼───────────────┼───────────────────┼───────────────┤
│    turquoise  │   '#40e0d0'   │  rgb(64,224,208)  │ (64,224,208)  │
└───────────────┴───────────────┴───────────────────┴───────────────┘
```
For a complete list of x11 colors run the following script:

    ```
    python -m maxgradient._x11
    ```

You can also visit the rich library's documentation to view all
of the colors at the following link: [X11 Colors](https://pdos.csail.mit.edu/~jinyang/rgb.html)
"""
    @singledispatchmethod
    def __init__(self, color) -> None:
        """A color that may be used to style renderables for the Console or from which
        to generate a gradient. Colors can be parse from a number
        of inputs: names, hex color codes, rgb color codes, or ColorTriplets."""
        
        
    @__init__.register
    def _Color(self, color: 'Color') -> None:
        """Parse a color from... a Color."""
        self.name = color.name
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
        self.mode = color.mode

    @__init__.register
    def _RichColor(self, color: RichColor) -> None:
        """Parse a color from a RichColor."""
        self.name = color.name
        index = Rich.NAMES.index(color.name)
        triplet = Rich.TRIPLETS[index]
        self.red = triplet[0]
        self.green = triplet[1]
        self.blue = triplet[2]
        self.mode = Mode.RICH

    @__init__.register
    def _ColorTriplet(self, color: ColorTriplet) -> None:
        """Parse a color from a ColorTriplet."""
        # name
        for group in [GradientColor.TRIPLETS, Rich.TRIPLETS, X11.TRIPLETS]:
            if color in group:
                index = group.index(color)
                self.name = group.NAMES[index]
            else:
                continue
        if not self.name:
            self.name = color.hex
            
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
        self.mode = Mode.COLOR_TRIPLET


    @__init__.register
    def _str(self, color: str) -> None:
        color_pallets = [GradientColor, Rich, X11]
        color_formats = [
            color.pallet.NAMES,
            color.pallet.HEX,
            color.pallet.RGB,
            color.pallet.TRIPLETS]:
                if color == format:
                    index: int = pallet.format.index(color)
                    triplet: ColorTriplet = pallet.TRIPLETS[index]
                    self.name: str = pallet.NAMES[index]
                    self.red = triplet.red
                    self.green = triplet.green
                    self.blue = triplet.green
                    self.mode = Mode.RICH
                    break
                else:
                    continue
