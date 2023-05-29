import re
from functools import lru_cache
from typing import Tuple, Optional

from rich.style import Style
from rich.table import Table
from rich.text import Text

X11: Tuple[str, ...] = (
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
    "lime",
    "limegreen",
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
X11HEX: Tuple[str, ...] = (
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
X11RGB: Tuple[str, ...] = (
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


@lru_cache(maxsize=147, typed=True)
def get_x11_colors() -> Tuple[str, ...]:
    return X11


@lru_cache(maxsize=147, typed=True)
def get_x11_hex_colors() -> Tuple[str, ...]:
    return X11HEX


@lru_cache(maxsize=147, typed=True)
def get_x11_rgb_colors() -> Tuple[str, ...]:
    return X11RGB


@lru_cache(maxsize=10)
def get_x11_color(color: str) -> Optional[str]:
    """Parse X11 colors for color"""
    if color in get_x11_colors():
        index = get_x11_colors().index(color)
        rgb = get_x11_rgb_colors()[index]
        return rgb
    elif color in get_x11_hex_colors():
        index = get_x11_hex_colors().index(color)
        rgb = get_x11_rgb_colors()[index]
        return rgb
    elif color in get_x11_rgb_colors():
        index = get_x11_rgb_colors().index(color)
        rgb = get_x11_rgb_colors()[index]
        return rgb
    else:
        return None


def get_title() -> Text:
    """Generate a colored text title."""
    x11 = Text("X11 ", style=Style(color="#ff00ff", bold=True))
    letter_c = Text("C", style=Style(color="#ff0000", bold=True))
    letter_o = Text("o", style=Style(color="#ff8800", bold=True))
    letter_l = Text("l", style=Style(color="#ffff00", bold=True))
    letter_o2 = Text("o", style=Style(color="#00ff00", bold=True))
    letter_r = Text("r", style=Style(color="#00ffff", bold=True))
    letter_s = Text("s", style=Style(color="#0088ff", bold=True))
    title = [x11, letter_c, letter_o, letter_l, letter_o2, letter_r, letter_s]
    return Text.assemble(*title)


def x11_table() -> Table:
    from rich.table import Table

    title = get_title()
    table = Table(title=title, show_header=True, header_style="bold.magenta")
    table.add_column("Example")
    table.add_column("Name")
    table.add_column("Hex")
    table.add_column("RGB")
    block = Text("█" * 12, style="bold")
    for index in range(147):
        color = X11[index]
        hex = X11HEX[index]
        rgb = X11RGB[index]
        table.add_row(
            f"[{hex}]{block}",
            f"[{hex}]{color}[/]",
            f"[{hex}]{hex}[/]",
            f"[{hex}]{rgb}[/]",
        )
    return table


if __name__ == "__main__":
    from rich.console import Console

    from maxgradient.theme import GradientTheme

    console = Console(theme=GradientTheme(), record=True)
    console.print(x11_table(), justify="center")
    console.save_svg("x11_colors.svg")
