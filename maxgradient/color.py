"""Module for parsing colors from strings."""
# pylint: disable=C0209,E0401,W0611,C0103,E0202,E0611
import colorsys
import re
from functools import lru_cache
from re import Match
from typing import Any, List, Optional, Tuple, Union

from rich import inspect
from rich.box import HEAVY, SQUARE
from rich.color import Color as RichColor
from rich.color import ColorParseError, ColorType
from rich.color_triplet import ColorTriplet
from rich.columns import Columns
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from maxgradient._gc import GradientColor as GC
from maxgradient._hex import Hex
from maxgradient._mode import Mode
from maxgradient._rgb import RGB
from maxgradient._rich import Rich
from maxgradient._x11 import X11
from maxgradient.log import Console, Log, watch
from maxgradient.theme import GradientTheme

console = Console()
log = Log()

VERBOSE: bool = False

ColorType = Union[Hex, "Color", RichColor, str, Tuple[int, int, int], X11]


class Color:
    """A class to represent a color that inherits and expands `rich.rich.Color` \
        to include X11 named colors as well as multiple formats of hex and rgb colors.
    """

    def __init__(self, color: Any) -> None:
        """A color that may be used to style renderables for the Console or \
        from which to generate a gradient. Colors can be parse from a number \
        of inputs:
        
1) GradientColors (str, Tuple[int,int,int]): The colors from which random\
    gradients are generated. Can be parsed from the GradientColor's name, \
    hex color code, RGB color code, or RGB tuple.
        ```         
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                      GradientColor Examples                       ┃
        ┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┫
        ┃  Color Names  ┃   Hex Color   ┃     RGB Color     ┃   RGB Tuple   ┃
        ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
        │       Magenta │   '#ff00ff'   │  rgb(255,0,255)   │  (255,0,255)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │        Purple │   '#af00ff'   │  rgb(175,0,255)   │  (165,0,255)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │       Violet  │   '#5f00ff'   │  rgb(95,0,255)    │  (95,0,255)   │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │          Blue │   '#0000ff'   │  rgb(0,0,255)     │  (0,0,255)    │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │     Lightblue │   '#0088ff'   │  rgb(0,136,255)   │  (0,136,255)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │          Cyan │   '#00ffff'   │  rgb(0,255,255)   │  (0,0,255)    │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │          green │   '#00ff00'   │  rgb(0,255,0)     │  (0,255,255)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │        Yellow │   '#ffff00'   │  rgb(255,255,0)   │  (255,255,0)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │        Orange │   '#ff8800'   │  rgb(255,255,0)   │  (255,136,0)  │
        ├───────────────┼───────────────┼───────────────────┼───────────────┤
        │           Red │   '#ff0000'   │  rgb(255,0,0)     │  (255,0,0)    │
        └───────────────┴───────────────┴───────────────────┴───────────────┘
        ```
        
2) RichColors (rich.color.Color|str|Tuple[int,int,int]): The rich library's:
- name
- hex color code
- rgb color code
- rgb tuple 
            
            Examples:

        ```     
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                      Rich Colors Examples                         ┃
        ┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┫
        ┃  Color Names  ┃   Hex Color   ┃     RGB Color     ┃   RGB Tuple   ┃
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

You can also visit the rich library's documentation to view all \
    of the colors at the following link: 
                
    https://rich.readthedocs.io/en/latest/appendix/colors.html
            
3) X11Colors (str|Tuple[int,int,int]) as color keywords (names), hex color codes, \
    or rgb tuples. 
    
            Examples:
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

You can also visit the rich library's documentation to view all \
    of the colors at the following link: 
                
    https://pdos.csail.mit.edu/~jinyang/rgb.html
"""
        log.debug("Called Color.__init__()")
        self.original: str = str(color)

        if isinstance(color, Color):
            self.name: str = color.name
            self.red: int = color.red
            self.green: int = color.green
            self.blue: int = color.blue
            self.mode: Mode = color.mode
            return

        if isinstance(color, tuple):
            color = f"rgb{color}"
        hex_match: Optional[Match] = Hex.REGEX.match(color)
        if hex_match:
            self.hex_components(color)
            self.name: str = self.generate_name(color)
            self.mode: Mode = Mode.HEX
            return

        rgb_match: Match = RGB.REGEX.match(color)
        if rgb_match:
            self.rgb_components(color)
            self.name: str = self.generate_name(color)
            self.mode: Mode = Mode.RGB
            return

        for group in [GC.NAMES, GC.HEX, GC.RGB, GC.RGB_TUPLE]:
            if color in group:
                index = group.index(color)
                rgb_tuple = GC.RGB_TUPLE[index]
                self.red, self.green, self.blue = rgb_tuple
                self.name: str = GC.NAMES[index]
                self.mode: Mode = Mode.GC
                return

        for group in [Rich.NAMES, Rich.HEX, Rich.RGB, Rich.RGB_TUPLE]:
            if color in group:
                index = group.index(color)
                rgb_tuple = Rich.RGB_TUPLE[index]
                self.red, self.green, self.blue = rgb_tuple
                self.name: str = Rich.NAMES[index]
                self.mode: Mode = Mode.RICH
                return

        for group in [X11.NAMES, X11.HEX, X11.RGB, X11.RGB_TUPLE]:
            color = str(color).lower()
            if color in group:
                index = group.index(color)
                rgb_tuple = X11.RGB_TUPLE[index]
                self.red, self.green, self.blue = rgb_tuple
                self.name: str = X11.NAMES[index]
                self.mode: Mode = Mode.X11
                return

        raise ColorParseError(f"Unable to parse color: {color}")

    @property
    @lru_cache
    def original(self) -> str:
        """Return the original color."""
        log.debug("Called Color.original.getter()")
        return self._original

    @original.setter
    def original(self, color: str) -> None:
        """Set the original color."""
        log.debug(f"Called Color.original.setter({color}")
        self._original = color

    @property
    @lru_cache
    def red(self) -> int:
        """Return the red value of the color."""
        return self._red

    @red.setter
    def red(self, red: int | float) -> None:
        """ "Set the red value of the color."""
        if isinstance(red, float):
            red = int(red * 255)
        if isinstance(red, int):
            assert 0 <= red <= 255, f"Red value must be between 0 and 255, not {red}"
            self._red = red

    @property
    @lru_cache
    def green(self) -> int:
        """Return the green value of the color."""
        return self._green

    @green.setter
    def green(self, green: int | float) -> None:
        """ "Set the green value of the color."""
        if isinstance(green, float):
            green = int(green * 255)
        if isinstance(green, int):
            assert (
                0 <= green <= 255
            ), f"Green value must be between 0 and 255, not {green}"
            self._green = green

    @property
    @lru_cache
    def blue(self) -> int:
        """Return the blue value of the color."""
        return self._blue

    @blue.setter
    def blue(self, blue: int | float) -> None:
        """Set the blue value of the color."""
        if isinstance(blue, float):
            blue = int(blue * 255)
        if isinstance(blue, int):
            assert 0 <= blue <= 255, f"Blue value must be between 0 and 255, not {blue}"
            self._blue = blue

    @property
    @lru_cache
    def name(self) -> str:
        """Return the name of the color."""
        log.debug("Called Color.name.getter()")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the color."""
        log.debug(f"Called Color.name.setter({name})")
        self._name = name

    @property
    def mode(self) -> Mode:
        """Return the mode of the color."""
        log.debug("Called Color.mode.getter()")
        return self._mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        """Set the mode of the color.

        Args:
            mode (Mode): The mode of the color.
        """
        log.debug(f"Called Color.mode.setter({mode})")
        self._mode = mode

    @property
    def hex(self) -> str:
        """Return the hex color code."""
        log.debug("Called Color.hex.getter()")
        red_str = f"{self.red:02X}"
        green_str = f"{self.green:02X}"
        blue_str = f"{self.blue:02X}"
        return f"#{red_str}{green_str}{blue_str}"

    @property
    def rgb(self) -> str:
        """Return the rgb color code."""
        log.debug("Called Color.rgb.getter()")
        return f"rgb({self.red},{self.green},{self.blue})"

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """Return the rgb color code as a tuple."""
        log.debug("Called Color.rgb_tuple.getter()")
        return (self.red, self.green, self.blue)

    @property
    def style(self) -> Style:
        """Return the style of the color."""
        log.debug("Called Color.style.getter()")
        return Style(color=self.hex)

    @property
    def bg_style(self) -> Style:
        """Return a style with the color as the background."""
        log.debug("Called Color.bg_style.getter()")
        foreground: str = self.get_contrast()
        return Style(color=foreground, bgcolor=self.hex)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self._original == other._original

    def __hash__(self):
        hash_value = 0
        name = self._original
        for char in name:
            hash_value += ord(char)
            # log.debug(f"Hashed {char} at index {index}: hash_value = {hash_value}")
        # log.debug(f"called Color.__hash__({self._original})")
        return hash_value

    def __rich__(self) -> Panel:
        """Return the rich console representation of a color."""
        log.debug("Called Color.__rich__()")
        table = Table(
            # title=self.name.capitalize(),
            show_header=False,
            show_footer=False,
            show_edge=True,
            show_lines=False,
            box=HEAVY,
            border_style=f"bold {self.style}",
            expand=False,
            width=40,
            collapse_padding=True,
            # caption=f"[dim italic]Original: {self.original}\n\n",
            # caption_justify="right"
        )

        contrast = self.get_contrast()
        table.add_column(
            "attribute", style=f"bold {contrast} on {self.bg_style}", justify="center"
        )

        table.add_column(
            "value", style=f"bold {self.style} on #000000", justify="center"
        )
        mode = self.mode
        table.add_row("Mode", mode)
        hex_str = str(self.hex).upper()
        table.add_row("HEX", hex_str)
        rgb_str = self.rgb
        table.add_row("RGB", rgb_str)
        rgb_tuple = self.rgb_tuple
        tuple_str = str(rgb_tuple)
        table.add_row("RGB Tuple", tuple_str)

        title = self.color_title()
        dark = Color(self.hex).darken(0.5)
        sub_panel = Panel(
            table,
            title=title,
            expand=False,
            box=HEAVY,
            border_style=Style(color=dark),
            subtitle=f"[i {dark}]Original: {self.original}\n\n",
            subtitle_align="right",
        )
        panel = Panel(sub_panel, border_style="#000000")
        return panel

    def color_title(self) -> Text:
        """Generate a title bar for the color."""
        log.debug("Called Color.color_title()")
        name = self.name.capitalize()
        length = len(name)
        # Calculate
        if length % 2 == 1:
            name = f"{name} "  # makes length even
            length += 1
        padding: int = (38 - length) / 2
        pad = " " * int(padding)
        color = Color(self.hex).darken(0.5)
        bg_color = Color(self.hex).lighten(0.5)
        return Text(
            f"{pad}{name}{pad}", style=Style(color=color, bgcolor=bg_color, bold=True)
        )

    def generate_name(self, color: Any) -> str:
        """Retrieve the color's name if it exists in GradientColor,\
            rich.color.Colors's Standard Library or X11 Colors. \
            Otherwise, generate a name from the color's hex value."""
        if self.rgb_tuple in GC.RGB_TUPLE:
            index = GC.RGB_TUPLE.index(self.rgb_tuple)
            return GC.NAMES[index]

        elif self.rgb_tuple in Rich.RGB_TUPLE:
            index = Rich.RGB_TUPLE.index(self.rgb_tuple)
            return Rich.NAMES[index]

        elif self.rgb_tuple in X11.RGB_TUPLE:
            index = X11.RGB_TUPLE.index(self.rgb_tuple)
            return X11.NAMES[index]

        else:
            return str(color)

    def hex_components(self, hex_str: str) -> None:
        """Parse color components from a hex string."""
        log.debug(f"Called Color.hex_components({hex_str})")
        if "#" in hex_str:
            hex_str = hex_str.replace("#", "")
        if len(hex_str) == 3:
            hex_str = "".join([char * 2 for char in hex_str])
        self.red = int(hex_str[0:2], 16)
        log.debug(f"Red: {self.red}")
        self.green = int(hex_str[2:4], 16)
        log.debug(f"Green: {self.green}")
        self.blue = int(hex_str[4:6], 16)
        log.debug(f"Blue: {self.blue}")

    def rgb_components(self, rgb_str: str) -> None:
        """Parse the components from an RGB string."""
        log.debug(f"Called Color.rgb_components({rgb_str})")
        REGEX = re.compile(
            r"r?g?b? ?\((?P<red>\d+\.?\d*)[ ,]? ?(?P<green>\d+\.?\d*)[ ,]? ?(?P<blue>\d+\.?\d*)\)"
        )
        match: Match = REGEX.match(rgb_str)
        if match:
            self.red = int(match.group("red"))
            log.debug(f"Red: {self.red}")
            self.green = int(match.group("green"))
            log.debug(f"Green: {self.green}")
            self.blue = int(match.group("blue"))
            log.debug(f"Blue: {self.blue}")

    def get_contrast(self) -> str:
        """Generate a foreground color for the color style.

        Returns:
            str: The foreground color.
        """

        def rgb_to_hsv(rgb_color: Tuple[int, int, int]):
            """Convert an RGB color to HSV."""
            r, g, b = rgb_color
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            return h, s, v

        def color_distance(rgb_color1, rgb_color2):
            """Calculate the distance between two colors."""
            h1, s1, v1 = rgb_to_hsv(rgb_color1)
            h2, s2, v2 = rgb_to_hsv(rgb_color2)
            dh = min(abs(h1 - h2), 1 - abs(h1 - h2))
            ds = abs(s1 - s2)
            dv = abs(v1 - v2)
            color_distance = dh + ds + dv
            return color_distance

        def find_closest_color(rgb_color, color_list):
            """Calculate the closest color in a list."""
            closest_color = None
            min_distance = float("inf")
            for color in color_list:
                distance = color_distance(rgb_color, color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color
            return closest_color

        closest = find_closest_color(self.rgb_tuple, [(0, 0, 0), (255, 255, 255)])
        if closest == (0, 0, 0):
            if VERBOSE:
                msg = f"[b {self.hex}]Color's contrast: [b #ffffff]White[/]"
                log.success(msg)
            else:
                log.debug(f"Contrast for Color<{self.name}> -> White")
            return "#ffffff"
        else:
            if VERBOSE:
                msg = f"[b {self.hex}]Color's contrast: [b #000000]Black[/]"
                log.success(msg)
            else:
                log.debug(f"Contrast for Color<{self.name}> -> White")
            return "#000000"

    def lighten(self, percent: float = 0.5) -> str:
        """Generate a tint of the color.

        Args:
            percent (float, optional): The percentage of the tint. \
                Defaults to 0.5.

        Returns:
            str: The tinted color as a hex string.
        """
        log.debug(f"Called Color.tint({percent})")
        rgb_tuple = self.rgb_tuple
        red, green, blue = rgb_tuple

        red_tint = int(red + (255 - red) * percent)
        red_final = f"{red_tint:02x}"

        green_tint = int(green + (255 - green) * percent)
        green_final = f"{green_tint:02x}"

        blue_tint = int(blue + (255 - blue) * percent)
        blue_final = f"{blue_tint:02x}"

        tint: str = f"#{red_final}{green_final}{blue_final}"
        log.debug(f"Tinting by {percent * 100}%: {tint}")
        return tint

    def darken(self, percent: float = 0.5) -> str:
        """Generate a tint of the color.

        Args:
            percent (float, optional): The percentage of the darkening. \
                Defaults to 0.5.

        Returns:
            str: The darkened color as a hex string.
        """
        log.debug(f"Called Color.dark({percent})")
        rgb_tuple = self.rgb_tuple
        red, green, blue = rgb_tuple

        dark_red = int(red + (0 - red) * percent)
        red_final = f"{dark_red:02x}"

        dark_green = int(green + (0 - green) * percent)
        green_final = f"{dark_green:02x}"

        dark_blue = int(blue + (0 - blue) * percent)
        blue_final = f"{dark_blue:02x}"

        dark: str = f"#{red_final}{green_final}{blue_final}"
        log.debug(f"Darken by {percent * 100}%: {dark}")
        return dark

    @classmethod
    def named_table(cls) -> Columns:
        """Return a table of named colors."""
        log.debug("Generating named color table.")
        colors = []
        for color in GC.NAMES:
            colors.append(Color(color))
        return Columns(colors, equal=True)

    @classmethod
    def color_table(cls) -> Columns:
        """Return a table of all colors."""
        tables: List[Table] = []
        for colors in [Rich, X11]:
            log.debug("Generating color table.")
            title = colors.get_title()
            table = Table(title=title, show_header=True, header_style="bold.magenta")
            table.add_column("Example", justify="center")
            table.add_column("Name", justify="center")
            table.add_column("Hex", justify="center")
            table.add_column("RGB", justify="center")
            table.add_column("RGB Tuple", justify="center")

            def add_row(
                color: Color, table: Table = table, end_section: bool = False
            ) -> Table:
                block = Text("█" * 12, style=f"bold {color.hex}")
                name = Text(color.name, style=f"bold {color.hex}")
                hex_color = Text(color.hex, style=f" bold {color.hex}")
                rgb_color = Text(color.rgb, style=f" bold {color.hex}")
                rgb_tuple = Text(str(color.rgb_tuple), style=f" bold {color.hex}")
                table.add_row(block, name, hex_color, rgb_color, rgb_tuple)
                if end_section:
                    table.add_section()
                return table

            for color in colors.NAMES:
                table = add_row(cls(color), table)
            tables.append(table)

        return Columns(tables, equal=True)


if __name__ == "__main__":
    console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
    console.print(Color.named_table(), justify="center")
    console.print(Color.color_table(), justify="center")
