# ruff: noqa: F401
import colorsys
import re
from enum import Enum
from functools import lru_cache, singledispatchmethod
from re import IGNORECASE, Pattern
from typing import Any, List, Tuple

import pandas as pd
import numpy as np
from numpy import array, ndarray, where
from rich import inspect
from rich.box import HEAVY, SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError, ColorType, blend_rgb
from maxgradient.color_triplet import ColorTriplet
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.traceback import install as tr_install
from snoop import snoop
from cheap_repr import register_repr, normal_repr

console = Console()
tr_install(console=console, show_locals=True)


class X11ColorParseError(ColorParseError):
    """Raised when a gradient color cannot be parsed from input."""

    pass


class Regex:
    """Regex patterns for parsing color inputs."""

    RGB: Pattern = re.compile(
        r"r?g?b? ?\((?P<red>\d+\.?\d*)[ ,]? ?(?P<green>\d+\.?\d*)[ ,]? ?(?P<blue>\d+\.?\d*)\)"
    )
    HEX: Pattern = re.compile(
        r"(#[0-9a-fA-F]{3}\b)|(#[0-9a-fA-F]{6}\b)|([0-9a-fA-F]{3}\b)|([0-9a-fA-F]{6}\b)"
    )


class X11:
    """A gradient color that can be parsed from a number of inputs."""
    NAMES: Tuple[str, ...] = (
        "aliceblue",
        "antiquewhite",
        "aqua",
        "aquamarine",
        "azure",
        "beige",
        "bisque",
        "black",
        "blanchedalmond",
        "blue",
        "blueviolet",
        "brown",
        "burlywood",
        "cadetblue",
        "chartreuse",
        "chocolate",
        "coral",
        "cornflowerblue",
        "cornsilk",
        "crimson",
        "cyan",
        "darkblue",
        "darkcyan",
        "darkgoldenrod",
        "darkgray",
        "darkgreen",
        "darkgrey",
        "darkkhaki",
        "darkmagenta",
        "darkolivegreen",
        "darkorange",
        "darkorchid",
        "darkred",
        "darksalmon",
        "darkseagreen",
        "darkslateblue",
        "darkslategray",
        "darkslategrey",
        "darkturquoise",
        "darkviolet",
        "deeppink",
        "deepskyblue",
        "dimgray",
        "dimgrey",
        "dodgerblue",
        "firebrick",
        "floralwhite",
        "forestgreen",
        "fuchsia",
        "gainsboro",
        "ghostwhite",
        "gold",
        "goldenrod",
        "gray",
        "green",
        "greenyellow",
        "grey",
        "honeydew",
        "hotpink",
        "indianred",
        "indigo",
        "ivory",
        "khaki",
        "lavender",
        "lavenderblush",
        "lawngreen",
        "lemonchiffon",
        "lightblue",
        "lightcoral",
        "lightcyan",
        "lightgoldenrodyellow",
        "lightgray",
        "lightgreen",
        "lightgrey",
        "lightpink",
        "lightsalmon",
        "lightseagreen",
        "lightskyblue",
        "lightslategray",
        "lightslategrey",
        "lightsteelblue",
        "lightyellow",
        "green",
        "greengreen",
        "linen",
        "magenta",
        "maroon",
        "mediumaquamarine",
        "mediumblue",
        "mediumorchid",
        "mediumpurple",
        "mediumseagreen",
        "mediumslateblue",
        "mediumspringgreen",
        "mediumturquoise",
        "mediumvioletred",
        "midnightblue",
        "mintcream",
        "mistyrose",
        "moccasin",
        "navajowhite",
        "navy",
        "oldlace",
        "olive",
        "olivedrab",
        "orange",
        "orangered",
        "orchid",
        "palegoldenrod",
        "palegreen",
        "paleturquoise",
        "palevioletred",
        "papayawhip",
        "peachpuff",
        "peru",
        "pink",
        "plum",
        "powderblue",
        "purple",
        "red",
        "rosybrown",
        "royalblue",
        "saddlebrown",
        "salmon",
        "sandybrown",
        "seagreen",
        "seashell",
        "sienna",
        "silver",
        "skyblue",
        "slateblue",
        "slategray",
        "slategrey",
        "snow",
        "springgreen",
        "steelblue",
        "tan",
        "teal",
        "thistle",
        "tomato",
        "turquoise",
        "violet",
        "wheat",
        "white",
        "whitesmoke",
        "yellow",
        "yellowgreen",
    )
    HEX: Tuple[str, ...] = (
        "#F0F8FF",
        "#FAEBD7",
        "#00FFFF",
        "#7FFFD4",
        "#F0FFFF",
        "#F5F5DC",
        "#FFE4C4",
        "#000000",
        "#FFEBCD",
        "#0000FF",
        "#8A2BE2",
        "#A52A2A",
        "#DEB887",
        "#5F9EA0",
        "#7FFF00",
        "#D2691E",
        "#FF7F50",
        "#6495ED",
        "#FFF8DC",
        "#DC143C",
        "#00FFFF",
        "#00008B",
        "#008B8B",
        "#B8860B",
        "#A9A9A9",
        "#006400",
        "#A9A9A9",
        "#BDB76B",
        "#8B008B",
        "#556B2F",
        "#FF8C00",
        "#9932CC",
        "#8B0000",
        "#E9967A",
        "#8FBC8F",
        "#483D8B",
        "#2F4F4F",
        "#2F4F4F",
        "#00CED1",
        "#9400D3",
        "#FF1493",
        "#00BFFF",
        "#696969",
        "#696969",
        "#1E90FF",
        "#B22222",
        "#FFFAF0",
        "#228B22",
        "#FF00FF",
        "#DCDCDC",
        "#F8F8FF",
        "#FFD700",
        "#DAA520",
        "#808080",
        "#008000",
        "#ADFF2F",
        "#808080",
        "#F0FFF0",
        "#FF69B4",
        "#CD5C5C",
        "#4B0082",
        "#FFFFF0",
        "#F0E68C",
        "#E6E6FA",
        "#FFF0F5",
        "#7CFC00",
        "#FFFACD",
        "#ADD8E6",
        "#F08080",
        "#E0FFFF",
        "#FAFAD2",
        "#D3D3D3",
        "#90EE90",
        "#D3D3D3",
        "#FFB6C1",
        "#FFA07A",
        "#20B2AA",
        "#87CEFA",
        "#778899",
        "#778899",
        "#B0C4DE",
        "#FFFFE0",
        "#00FF00",
        "#32CD32",
        "#FAF0E6",
        "#FF00FF",
        "#800000",
        "#66CDAA",
        "#0000CD",
        "#BA55D3",
        "#9370DB",
        "#3CB371",
        "#7B68EE",
        "#00FA9A",
        "#48D1CC",
        "#C71585",
        "#191970",
        "#F5FFFA",
        "#FFE4E1",
        "#FFE4B5",
        "#FFDEAD",
        "#000080",
        "#FDF5E6",
        "#808000",
        "#6B8E23",
        "#FFA500",
        "#FF4500",
        "#DA70D6",
        "#EEE8AA",
        "#98FB98",
        "#AFEEEE",
        "#DB7093",
        "#FFEFD5",
        "#FFDAB9",
        "#CD853F",
        "#FFC0CB",
        "#DDA0DD",
        "#B0E0E6",
        "#5f00ff",
        "#FF0000",
        "#BC8F8F",
        "#4169E1",
        "#8B4513",
        "#FA8072",
        "#F4A460",
        "#2E8B57",
        "#FFF5EE",
        "#A0522D",
        "#C0C0C0",
        "#87CEEB",
        "#6A5ACD",
        "#708090",
        "#708090",
        "#FFFAFA",
        "#00FF7F",
        "#4682B4",
        "#D2B48C",
        "#008080",
        "#D8BFD8",
        "#FF6347",
        "#40E0D0",
        "#af00ff",
        "#F5DEB3",
        "#FFFFFF",
        "#F5F5F5",
        "#FFFF00",
        "#9ACD32",
    )

    RGB: Tuple[str, ...] = (
        "rgb(240,248,255)",
        "rgb(250,235,215)",
        "rgb(0,255,255)",
        "rgb(127,255,212)",
        "rgb(240,255,255)",
        "rgb(245,245,220)",
        "rgb(255,228,196)",
        "rgb(0,0,0)",
        "rgb(255,235,205)",
        "rgb(0,0,255)",
        "rgb(138,43,226)",
        "rgb(165,42,42)",
        "rgb(222,184,135)",
        "rgb(95,158,160)",
        "rgb(127,255,0)",
        "rgb(210,105,30)",
        "rgb(255,127,80)",
        "rgb(100,149,237)",
        "rgb(255,248,220)",
        "rgb(220,20,60)",
        "rgb(0,255,255)",
        "rgb(0,0,139)",
        "rgb(0,139,139)",
        "rgb(184,134,11)",
        "rgb(169,169,169)",
        "rgb(0,100,0)",
        "rgb(169,169,169)",
        "rgb(189,183,107)",
        "rgb(139,0,139)",
        "rgb(85,107,47)",
        "rgb(255,140,0)",
        "rgb(153,50,204)",
        "rgb(139,0,0)",
        "rgb(233,150,122)",
        "rgb(143,188,143)",
        "rgb(72,61,139)",
        "rgb(47,79,79)",
        "rgb(47,79,79)",
        "rgb(0,206,209)",
        "rgb(148,0,211)",
        "rgb(255,20,147)",
        "rgb(0,191,255)",
        "rgb(105,105,105)",
        "rgb(105,105,105)",
        "rgb(30,144,255)",
        "rgb(178,34,34)",
        "rgb(255,250,240)",
        "rgb(34,139,34)",
        "rgb(255,0,255)",
        "rgb(220,220,220)",
        "rgb(248,248,255)",
        "rgb(255,215,0)",
        "rgb(218,165,32)",
        "rgb(128,128,128)",
        "rgb(0,128,0)",
        "rgb(173,255,47)",
        "rgb(128,128,128)",
        "rgb(240,255,240)",
        "rgb(255,105,180)",
        "rgb(205,92,92)",
        "rgb(75,0,130)",
        "rgb(255,255,240)",
        "rgb(240,230,140)",
        "rgb(230,230,250)",
        "rgb(255,240,245)",
        "rgb(124,252,0)",
        "rgb(255,250,205)",
        "rgb(173,216,230)",
        "rgb(240,128,128)",
        "rgb(224,255,255)",
        "rgb(250,250,210)",
        "rgb(211,211,211)",
        "rgb(144,238,144)",
        "rgb(211,211,211)",
        "rgb(255,182,193)",
        "rgb(255,160,122)",
        "rgb(32,178,170)",
        "rgb(135,206,250)",
        "rgb(119,136,153)",
        "rgb(119,136,153)",
        "rgb(176,196,222)",
        "rgb(255,255,224)",
        "rgb(0,255,0)",
        "rgb(50,205,50)",
        "rgb(250,240,230)",
        "rgb(255,0,255)",
        "rgb(128,0,0)",
        "rgb(102,205,170)",
        "rgb(0,0,205)",
        "rgb(186,85,211)",
        "rgb(147,112,219)",
        "rgb(60,179,113)",
        "rgb(123,104,238)",
        "rgb(0,250,154)",
        "rgb(72,209,204)",
        "rgb(199,21,133)",
        "rgb(25,25,112)",
        "rgb(245,255,250)",
        "rgb(255,228,225)",
        "rgb(255,228,181)",
        "rgb(255,222,173)",
        "rgb(0,0,128)",
        "rgb(253,245,154)",
        "rgb(128,128,0)",
        "rgb(107,142,35)",
        "rgb(255,165,0)",
        "rgb(255,69,0)",
        "rgb(218,112,214)",
        "rgb(238,232,170)",
        "rgb(152,251,152)",
        "rgb(175,238,238)",
        "rgb(219,112,147)",
        "rgb(255,239,213)",
        "rgb(255,218,185)",
        "rgb(205,133,63)",
        "rgb(255,192,203)",
        "rgb(221,160,221)",
        "rgb(176,224,230)",
        "rgb(95,0,255)",
        "rgb(255,0,0)",
        "rgb(188,143,143)",
        "rgb(65,105,225)",
        "rgb(139,69,19)",
        "rgb(250,128,114)",
        "rgb(244,164,96)",
        "rgb(46,139,87)",
        "rgb(255,245,238)",
        "rgb(160,82,45)",
        "rgb(192,192,192)",
        "rgb(135,206,235)",
        "rgb(106,90,205)",
        "rgb(112,128,144)",
        "rgb(112,128,144)",
        "rgb(255,250,250)",
        "rgb(0,255,127)",
        "rgb(70,130,180)",
        "rgb(210,180,140)",
        "rgb(0,128,128)",
        "rgb(216,191,216)",
        "rgb(255,99,71)",
        "rgb(64,224,208)",
        "rgb(175,0,255)",
        "rgb(245,222,179)",
        "rgb(255,255,255)",
        "rgb(245,245,245)",
        "rgb(255,255,0)",
        "rgb(154,205,50)",
    )

    TRIPLETS: Tuple[ColorTriplet, ...] = (
                ColorTriplet(240, 248, 255),
        ColorTriplet(250, 235, 215),
        ColorTriplet(0, 255, 255),
        ColorTriplet(127, 255, 212),
        ColorTriplet(240, 255, 255),
        ColorTriplet(245, 245, 220),
        ColorTriplet(255, 228, 196),
        ColorTriplet(0, 0, 0),
        ColorTriplet(255, 235, 205),
        ColorTriplet(0, 0, 255),
        ColorTriplet(138, 43, 226),
        ColorTriplet(165, 42, 42),
        ColorTriplet(222, 184, 135),
        ColorTriplet(95, 158, 160),
        ColorTriplet(127, 255, 0),
        ColorTriplet(210, 105, 30),
        ColorTriplet(255, 127, 80),
        ColorTriplet(100, 149, 237),
        ColorTriplet(255, 248, 220),
        ColorTriplet(220, 20, 60),
        ColorTriplet(0, 255, 255),
        ColorTriplet(0, 0, 139),
        ColorTriplet(0, 139, 139),
        ColorTriplet(184, 134, 11),
        ColorTriplet(169, 169, 169),
        ColorTriplet(0, 100, 0),
        ColorTriplet(169, 169, 169),
        ColorTriplet(189, 183, 107),
        ColorTriplet(139, 0, 139),
        ColorTriplet(85, 107, 47),
        ColorTriplet(255, 140, 0),
        ColorTriplet(153, 50, 204),
        ColorTriplet(139, 0, 0),
        ColorTriplet(233, 150, 122),
        ColorTriplet(143, 188, 143),
        ColorTriplet(72, 61, 139),
        ColorTriplet(47, 79, 79),
        ColorTriplet(47, 79, 79),
        ColorTriplet(0, 206, 209),
        ColorTriplet(148, 0, 211),
        ColorTriplet(255, 20, 147),
        ColorTriplet(0, 191, 255),
        ColorTriplet(105, 105, 105),
        ColorTriplet(105, 105, 105),
        ColorTriplet(30, 144, 255),
        ColorTriplet(178, 34, 34),
        ColorTriplet(255, 250, 240),
        ColorTriplet(34, 139, 34),
        ColorTriplet(255, 0, 255),
        ColorTriplet(220, 220, 220),
        ColorTriplet(248, 248, 255),
        ColorTriplet(255, 215, 0),
        ColorTriplet(218, 165, 32),
        ColorTriplet(128, 128, 128),
        ColorTriplet(0, 128, 0),
        ColorTriplet(173, 255, 47),
        ColorTriplet(128, 128, 128),
        ColorTriplet(240, 255, 240),
        ColorTriplet(255, 105, 180),
        ColorTriplet(205, 92, 92),
        ColorTriplet(75, 0, 130),
        ColorTriplet(255, 255, 240),
        ColorTriplet(240, 230, 140),
        ColorTriplet(230, 230, 250),
        ColorTriplet(255, 240, 245),
        ColorTriplet(124, 252, 0),
        ColorTriplet(255, 250, 205),
        ColorTriplet(173, 216, 230),
        ColorTriplet(240, 128, 128),
        ColorTriplet(224, 255, 255),
        ColorTriplet(250, 250, 210),
        ColorTriplet(211, 211, 211),
        ColorTriplet(144, 238, 144),
        ColorTriplet(211, 211, 211),
        ColorTriplet(255, 182, 193),
        ColorTriplet(255, 160, 122),
        ColorTriplet(32, 178, 170),
        ColorTriplet(135, 206, 250),
        ColorTriplet(119, 136, 153),
        ColorTriplet(119, 136, 153),
        ColorTriplet(176, 196, 222),
        ColorTriplet(255, 255, 224),
        ColorTriplet(0, 255, 0),
        ColorTriplet(50, 205, 50),
        ColorTriplet(250, 240, 230),
        ColorTriplet(255, 0, 255),
        ColorTriplet(128, 0, 0),
        ColorTriplet(102, 205, 170),
        ColorTriplet(0, 0, 205),
        ColorTriplet(186, 85, 211),
        ColorTriplet(147, 112, 219),
        ColorTriplet(60, 179, 113),
        ColorTriplet(123, 104, 238),
        ColorTriplet(0, 250, 154),
        ColorTriplet(72, 209, 204),
        ColorTriplet(199, 21, 133),
        ColorTriplet(25, 25, 112),
        ColorTriplet(245, 255, 250),
        ColorTriplet(255, 228, 225),
        ColorTriplet(255, 228, 181),
        ColorTriplet(255, 222, 173),
        ColorTriplet(0, 0, 128),
        ColorTriplet(253, 245, 154),
        ColorTriplet(128, 128, 0),
        ColorTriplet(107, 142, 35),
        ColorTriplet(255, 165, 0),
        ColorTriplet(255, 69, 0),
        ColorTriplet(218, 112, 214),
        ColorTriplet(238, 232, 170),
        ColorTriplet(152, 251, 152),
        ColorTriplet(175, 238, 238),
        ColorTriplet(219, 112, 147),
        ColorTriplet(255, 239, 213),
        ColorTriplet(255, 218, 185),
        ColorTriplet(205, 133, 63),
        ColorTriplet(255, 192, 203),
        ColorTriplet(221, 160, 221),
        ColorTriplet(176, 224, 230),
        ColorTriplet(95, 0, 255),
        ColorTriplet(255, 0, 0),
        ColorTriplet(188, 143, 143),
        ColorTriplet(65, 105, 225),
        ColorTriplet(139, 69, 19),
        ColorTriplet(250, 128, 114),
        ColorTriplet(244, 164, 96),
        ColorTriplet(46, 139, 87),
        ColorTriplet(255, 245, 238),
        ColorTriplet(160, 82, 45),
        ColorTriplet(192, 192, 192),
        ColorTriplet(135, 206, 235),
        ColorTriplet(106, 90, 205),
        ColorTriplet(112, 128, 144),
        ColorTriplet(112, 128, 144),
        ColorTriplet(255, 250, 250),
        ColorTriplet(0, 255, 127),
        ColorTriplet(70, 130, 180),
        ColorTriplet(210, 180, 140),
        ColorTriplet(0, 128, 128),
        ColorTriplet(216, 191, 216),
        ColorTriplet(255, 99, 71),
        ColorTriplet(64, 224, 208),
        ColorTriplet(175, 0, 255),
        ColorTriplet(245, 222, 179),
        ColorTriplet(255, 255, 255),
        ColorTriplet(245, 245, 245),
        ColorTriplet(255, 255, 0),
        ColorTriplet(154, 205, 50)
    )

    def __init__(self, color: Any) -> None:
        """Initialize a X11 color from a color input.

        Args:
            color (ColorType): A color input that can be parsed into a GradientColor.
        """
        index = self.find_index(color)
        self.name = self.NAMES[index]
        triplet: ColorTriplet = self.TRIPLETS[index]
        self.red = triplet[0]
        self.green = triplet[1]
        self.blue = triplet[2]

    def find_index(self, color: Any) -> int:
        for group in [self.NAMES,self.HEX,self.RGB, self.TRIPLETS]:
            if color in group:
                self.index = group.index(color)
                return self.index
            else:
                continue
        raise ValueError(f"Color {color} not found in X11 colors.")
    
    @property
    def index(self) -> int:
        """The index of the color in the X11 array."""
        
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """Set the index of the color in the X11 array."""
        if value < 0 or value > len(self.NAMES):
            raise ValueError("Index must be between 0 and 255.")
        self._index = value

    @property
    def name(self) -> str:
        """The name of the color."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the color."""
        self._name = value

    @property
    def red(self) -> int:
        """The red component of the color."""
        return self._red
    
    @red.setter
    def red(self, value: int) -> None:
        """Set the red component of the color."""
        if value < 0 or value > 255:
            raise ValueError("Red component must be between 0 and 255.")
        self._red = value
        
    @property
    def green(self) -> int:
        """The green component of the color."""
        return self._green
    
    @green.setter
    def green(self, value: int) -> None:
        """Set the green component of the color."""
        if value < 0 or value > 255:
            raise ValueError("Green component must be between 0 and 255.")
        self._green = value
        
    @property
    def blue(self) -> int:
        """The blue component of the color."""
        return self._blue
    
    @blue.setter
    def blue(self, value: int) -> None:
        """Set the blue component of the color."""
        if value < 0 or value > 255:
            raise ValueError("Blue component must be between 0 and 255.")
        self._blue = value
        

    @property
    def hex(self) -> str:
        """Return the hex color code."""
        red_str = f"{self.red:02X}"
        green_str = f"{self.green:02X}"
        blue_str = f"{self.blue:02X}"
        return f"#{red_str}{green_str}{blue_str}"

    @property
    def rgb(self) -> str:
        """Return the rgb color code."""
        return f"rgb({self.red},{self.green},{self.blue})"

    @property
    def triplet(self) -> ColorTriplet:
        """Return the color triplet."""
        return ColorTriplet(self.red, self.green, self.blue)

    def __repr__(self) -> str:
        """Return a string representation of the GradientColor."""
        return f"X11<{self.name}>"

    def __str__(self) -> str:
        """Return the colors name."""
        return str(self.name)

    def __eq__(self, other: Any) -> bool:
        """Return True if the GradientColor is equal to other."""
        if isinstance(other, X11):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __rich__(self) -> Panel:
        """Return a rich Table representation of the GradientColor."""
        table = Table(box=HEAVY, border_style=f"bold {self.hex}", show_header=False)
        table.add_column("Attribute", justify="right", style=f"i on {self.hex}")
        table.add_column("Value", justify="left", style=f"bold {self.hex}")
        table.add_row("Index", f"{self.index}")
        table.add_row("Hex", self.hex)
        table.add_row("RGB", self.rgb)
        title_pad = (22 - len(self.name)) // 2
        pad = title_pad * " "
        return Panel(
            table,
            title=f"[bold reverse]{pad}{self.name.capitalize()}{pad}[/]",
            border_style=f"bold {self.hex}",
            box=SQUARE,
            expand=False,
        )

register_repr(X11)(normal_repr)

if __name__ == "__main__":
    from random import randint, choice
    random_index = randint(0, len(X11.NAMES) - 1)
    format = choice(["NAMES", "HEX", "RGB", "TRIPLETS"])
    color = getattr(X11, format)[random_index]
    x11 = X11(color)
    console.print(x11)
