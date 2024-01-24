"""Module for parsing colors from strings."""
# pylint: disable=C0209,E0401,W0611,C0103,E0202,E0611
import colorsys
import re
from functools import singledispatchmethod
from re import Match
from typing import Any, List, Optional, Tuple, TypeAlias, Union

# from rich import inspect
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

from maxgradient._gradient_color import GradientColor
from maxgradient._hex_color import Hex
from maxgradient._mode import Mode
from maxgradient._rgb_color import RGB
from maxgradient._rich_color import Rich
from maxgradient._x11_color import X11
from maxgradient._theme import GradientTheme

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

    def __init__(self, color: Any) -> None:
        """A color that may be used to style renderables for the Console or from which
        to generate a gradient. Colors can be parse from a number
        of inputs: names, hex color codes, rgb color codes, or ColorTriplets."""

        self.original: str = str(color)  # type: ignore

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
            self.name: str = self.generate_name(color)  # type: ignore
            self.mode: Mode = Mode.HEX
            return

        rgb_match: Match = RGB.REGEX.match(color)  # type: ignore
        if rgb_match:
            self.rgb_components(color)
            self.name: str = self.generate_name(color)  # type: ignore
            self.mode: Mode = Mode.RGB
            return

        GC = GradientColor
        for group in [GC.get_names(), GC.get_hex(), GC.get_rgb(), GC.get_triplets()]:
            if color in group:
                if VERBOSE:
                    console.print(f"Found color [b {color}]{color}[/] in {group}")
                index = group.index(color)
                triplet = GradientColor.TRIPLETS[index]
                self.red, self.green, self.blue = triplet  # type: ignore
                self.name = GradientColor.NAMES[index]  # type: ignore
                self.mode: Mode = Mode.GRADIENT_COLOR
                return

        for group in [Rich.NAMES, Rich.HEX, Rich.RGB, Rich.TRIPLETS]:
            if color in group:
                index = group.index(color)
                triplet = Rich.TRIPLETS[index]
                self.red, self.green, self.blue = triplet  # type: ignore
                self.name: str = Rich.NAMES[index]  # type: ignore
                self.mode: Mode = Mode.RICH
                return

        for group in [X11.NAMES, X11.HEX, X11.RGB, X11.TRIPLETS]:
            color = str(color).lower()
            if color in group:
                index = group.index(color)
                triplet = X11.TRIPLETS[index]
                self.red, self.green, self.blue = triplet  # type: ignore
                self.name: str = X11.NAMES[index]  # type: ignore
                self.mode: Mode = Mode.X11
                return

        raise ColorParseError(f"Unable to parse color: {color}")

    @property
    def original(self) -> str:  # type: ignore
        """Return the original color."""

        return self._original

    @original.setter
    def original(self, color: str) -> None:  # type: ignore
        """Set the original color."""

        self._original = color

    @property
    def red(self) -> int:  # type: ignore
        """Return the red value of the color."""
        return self._red

    @red.setter
    def red(self, red: int | float) -> None:  # type: ignore
        """ "Set the red value of the color."""
        if isinstance(red, float):
            red = int(red * 255)
        if isinstance(red, int):
            assert 0 <= red <= 255, f"Red value must be between 0 and 255, not {red}"
            self._red = red

    # type: ignore
    @property
    def green(self) -> int:  # type: ignore
        """Return the green value of the color."""
        return self._green

    @green.setter  # type: ignore
    def green(self, green: int | float) -> None:  # type: ignore
        """ "Set the green value of the color."""
        if isinstance(green, float):
            green = int(green * 255)
        if isinstance(green, int):
            assert (
                0 <= green <= 255
            ), f"Green value must be between 0 and 255, not {green}"
            self._green = green

    @property
    def blue(self) -> int:  # type: ignore
        """Return the blue value of the color."""
        return self._blue

    @blue.setter  # type: ignore
    def blue(self, blue: int | float) -> None:  # type: ignore
        """Set the blue value of the color."""
        if isinstance(blue, float):
            blue = int(blue * 255)
        if isinstance(blue, int):
            assert 0 <= blue <= 255, f"Blue value must be between 0 and 255, not {blue}"
            self._blue = blue

    @property
    def name(self) -> str:  # type: ignore
        """Return the name of the color."""

        return self._name

    @name.setter
    def name(self, name: str) -> None:  # type: ignore
        """Set the name of the color."""

        self._name = name

    @property
    def mode(self) -> Mode:  # type: ignore
        """Return the mode of the color."""

        return self._mode

    @mode.setter
    def mode(self, mode: Mode) -> None:  # type: ignore
        """Set the mode of the color.

        Args:
            mode (Mode): The mode of the color.
        """

        self._mode = mode

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
        """Return the rgb color code as a tuple."""
        return ColorTriplet(self.red, self.green, self.blue)  # type: ignore

    @property
    def style(self) -> Style:
        """Return the style of the color."""
        return Style(color=self.hex)

    @property
    def bg_style(self) -> Style:
        """Return a style with the color as the background."""
        foreground: RichColor = RichColor.from_triplet(self.contrast)
        return Style(color=foreground, bgcolor=self.hex)

    @classmethod
    def from_triplet(cls, triplet: ColorTriplet) -> 'Color':
        """Create a Color from a ColorTriplet."""
        return cls(hex)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self._original == other._original

    def __hash__(self):
        hash_value = 0
        name = self._original
        for char in name:
            hash_value += ord(char)
            #
        #
        return hash_value

    def __rich__(self) -> Panel:
        """Return a rich table representation of the gradient color."""
        _dark_style = Style(color=RichColor.from_triplet(self.darken(0.5)))
        table = Table(
            show_header=False,
            show_footer=False,
            show_edge=True,
            show_lines=False,
            box=HEAVY,
            border_style=f"bold {self.hex}",
            expand=False,
            # row_styles = self.row_styles
        )

        table.add_column("attribute", justify="right")
        table.add_column(
            "value",
            style=Style(color=f"{self.hex}", bgcolor=self.contrast.hex),
            justify="left",
        )

        # Key Styles
        key_style_even: Style = Style(
            color="#FFFFFF",
            bgcolor=RichColor.from_triplet(self.triplet),
            bold=True,
            italic=True,
        )
        key_style_odd: Style = Style(
            color=f"{self.hex}",
            bgcolor=RichColor.from_triplet(
                blend_rgb(self.triplet, self.contrast, 0.85)
            ),
            bold=True,
            italic=True,
        )

        # Mode
        mode_key = Text("Mode", style=key_style_odd, justify="right")
        mode = f"[b {self.hex}]Mode[/][#cfcfff].[/][i #7FD6E8]GradientColor[/]"
        table.add_row(mode_key, mode)

        # Hex
        hex_str = str(self.hex).upper()
        hex_key = Text("HEX", style=key_style_even, justify="right")
        table.add_row(hex_key, Text(hex_str, style=f"bold {self.hex}"))

        # RGB
        rgb_key = Text("RGB", style=key_style_odd, justify="right")
        table.add_row(rgb_key, self.colorize_triplet(rgb=True))

        # ColorTriplet
        triplet_key = Text("ColorTriplet", style=key_style_even, justify="right")
        table.add_row(triplet_key, self.colorize_triplet())

        title = self.color_title()
        _dark_style = Style(color=RichColor.from_triplet(self.darken(0.5)))
        sub_panel = Panel(
            table, title=title, expand=False, box=HEAVY, border_style=_dark_style
        )
        _darker_style = Style(color=RichColor.from_triplet(self.darken(0.75)))
        panel = Panel(sub_panel, box=SQUARE, border_style=_darker_style, expand=False)
        return panel

    def colorize_triplet(
        self, rgb: bool = False, *, justify: JustifyMethod = "right"
    ) -> Text:
        """Format a ColorTriplet as a rich.text.Text object.

        Args:
            rgb (bool, optional): Whether to return the RGB value. Defaults to False.

        Returns:
            Text: A colored Text object.
        """
        prefix: str = "rgb" if rgb else "ColorTriplet"
        left_str: str = "("
        right_str: str = ")"
        comma_str: str = ","
        left = Text(left_str, style="bold #ffffff")
        right = Text(right_str, style="bold #ffffff")
        comma = Text(comma_str, style="bold #ffffff")

        pad = self.pad_value
        return Text.assemble(
            *[
                Text(prefix, style=f"bold {self.hex}"),
                left,
                Text(f"{pad(self.triplet.red)}", style="bold #ff0000"),
                comma,
                Text(f"{pad(self.triplet.green)}", style="bold #00ff00"),
                comma,
                Text(f"{pad(self.triplet.blue)}", style="bold #00afff"),
                right,
            ]
        )

    def __repr__(self) -> str:
        """Return the repr of the color."""
        repr = "MaxGradient.color.Color<"
        repr = f"{repr}{self.name}>"
        return repr

    def color_title(self) -> Text:
        """Generate a title bar for the color."""

        name = self.name.capitalize()  # type: ignore
        length = len(name)
        # Calculate
        if length % 2 == 1:
            name = f"{name} "  # makes length even
            length += 1
        padding: int = (38 - length) / 2  # type: ignore
        pad = " " * int(padding)
        _color = Color(self.hex).darken(0.5)
        color = RichColor.from_triplet(_color)
        _bg_color = Color(self.hex).lighten(0.5)
        bg_color = RichColor.from_triplet(_bg_color)
        
        return Text(
            f"{pad}{name}{pad}", style=Style(color=color, bgcolor=bg_color, bold=True)
        )

    @singledispatchmethod
    def generate_name(self, color) -> str:
        """Retrieve the color's name if it exists in GradientColor,\
            rich.color.Colors's Standard Library or X11 Colors. \
            Otherwise, generate a name from the color's hex value."""

        return str(color)

    @generate_name.register
    def _ColorTriplet(self, color: ColorTriplet) -> str:
        for group in [GradientColor.TRIPLETS, Rich.TRIPLETS, X11.TRIPLETS]:
            if color in group:
                index = group.index(color)
                return GradientColor.NAMES[index]
            else:
                continue
        return str(color)

    @generate_name.register
    def _Color(self, color: RichColor) -> str:
        return color.name

    @generate_name.register
    def _str(self, color: str) -> str:
        for group in [GradientColor, Rich, X11]:
            for mod in [group.NAMES, group.HEX, group.RGB]:
                if color in mod:
                    index = mod.index(color)
                    return group.NAMES[index]
                else:
                    continue
        return color

    def hex_components(self, hex_str: str) -> None:
        """Parse color components from a hex string."""

        if "#" in hex_str:
            hex_str = hex_str.replace("#", "")
        if len(hex_str) == 3:
            hex_str = "".join([char * 2 for char in hex_str])
        self.red = int(hex_str[0:2], 16)
        self.green = int(hex_str[2:4], 16)
        self.blue = int(hex_str[4:6], 16)

    def rgb_components(self, rgb_str: str) -> None:
        """Parse the components from an RGB string."""

        REGEX = re.compile(r"r?g?b? ?\((?P<red>\d+), ?(?P<green>\d+), ?(?P<blue>\d+)\)")
        match: Optional[Match] = REGEX.match(rgb_str)
        if match:
            self.red = int(match.group("red"))
            self.green = int(match.group("green"))
            self.blue = int(match.group("blue"))

    @property
    def contrast(self) -> ColorTriplet:
        """Return the color's contrast color."""
        return self.get_contrast()

    def get_contrast(self) -> ColorTriplet:
        """Generate a foreground color for the color style.

        Generate a foreground color for the color style based on the color's
        contrast ratio. If the color is dark, the foreground color will be
        white. If the color is light, the foreground color will be black.

        Returns:
            str: The foreground color.
        """

        def triplet_to_hsv(triplet: ColorTriplet) -> Tuple[float, float, float]:
            """Convert an RGB color to HSV."""
            h, s, v = colorsys.rgb_to_hsv(
                triplet.red / 255, triplet.green / 255, triplet.blue / 255
            )
            return h, s, v


        def color_distance(triplet1: ColorTriplet, triplet2: ColorTriplet):
            """Calculate the distance between two colors."""
            h1, s1, v1 = GradientColor.triplet_to_hsv(triplet1)
            h2, s2, v2 = GradientColor.triplet_to_hsv(triplet2)
            dh: float = min(abs(h1 - h2), 1 - abs(h1 - h2))
            ds: float = abs(s1 - s2)
            dv: float = abs(v1 - v2)
            color_distance: float = dh + ds + dv
            return color_distance

        def find_closest_color(triplet: ColorTriplet, color_list: List[ColorTriplet]):
            """Calculate the closest color in a list."""
            closest_color = None
            min_distance = float("inf")
            for color in color_list:
                distance = GradientColor.color_distance(triplet, color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color
            return closest_color

        closest = GradientColor.find_closest_color(
            self.triplet,
            color_list=[ColorTriplet(0, 0, 0), ColorTriplet(255, 255, 255)],
        )
        if closest == ColorTriplet(0, 0, 0):
            return ColorTriplet(255, 255, 255)
        else:
            return ColorTriplet(0, 0, 0)

    @staticmethod
    def pad_value(value: str|int) -> str:
        """Pad the value with spaces."""
        if isinstance(value, int):
            str_value = str(value)
        elif isinstance(value, str):
            str_value = value
        else:
            raise TypeError(f"Expected str or int, got {type(value)}")
        if len(str_value) < 3:
            return f'{" " * (3 - len(str_value))}{str_value}'
        return str_value

    @staticmethod
    def blend(color1: ColorTriplet, color2: ColorTriplet, amount: float) -> ColorTriplet:# type: ignore
        """Blend two colors together."""
        # validate inputs
        assert 0 <= amount <= 1, f"Amount must be between 0 and 1, not {amount}"
        for color in (color1, color2):
            assert isinstance(color, ColorTriplet), f"Expected ColorTriplet, got {type(color)}"
        if color1.red == color2.red and color1.green == color2.green and color1.blue == color2.blue:
            return color1
        if amount == 0 or amount == 1:
            return color1 if amount == 1 else color2
        # blend colors
        return blend_rgb(color1, color2, amount)
            

    def rgb_text(self) -> Text:
        """Return the rgb color code as a rich.text.Text object."""
        red_blend = Color(
            blend_rgb(
                self.triplet,
                ColorTriplet(255, 0, 0),
                0.5
            )
        ).hex
        green_blend = Color(
            blend_rgb(
                self.triplet,
                ColorTriplet(0, 255, 0),
                0.5
            )
        ).hex
        blue_blend = Color(
            blend_rgb(
                self.triplet,
                ColorTriplet(0, 0, 255),
                0.5
            )
        ).hex
        pad = self.pad_value
        red = Text(f"{pad(self.red)}", style=f"bold {red_blend}")
        green = Text(f"{pad(self.green)}", style=f"bold {green_blend}")
        blue = Text(f"{pad(self.blue)}", style=f"bold {blue_blend}")
        
        return Text.assemble(
            *[
                Text("rgb", style=f"bold {self.hex}"),
                Text("(", style=f"bold {self.hex}"),
                red,
                Text(",", style=f"bold {self.hex}"),
                green,
                Text(",", style=f"bold {self.hex}"),
                blue,
                Text(")", style=f"bold {self.hex}"),
            ]
        )

    def darken(self, amount: float = 0.5) -> ColorTriplet:
        """Darken a color by a given amount.

        Args:
            amount (float, optional): The amount to darken the color. Defaults to 0.5.

        Returns:
            GradientColor: A new GradientColor object.
        """
        black = ColorTriplet(0, 0, 0)
        shade = blend_rgb(self.triplet, black, amount)
        return shade

    def lighten(self, amount: float = 0.5) -> ColorTriplet:
        """Darken a color by a given amount.

        Args:
            amount (float, optional): The amount to darken the color. Defaults to 0.5.

        Returns:
            GradientColor: A new GradientColor object.
        """
        white = ColorTriplet(255, 255, 255)
        tint = blend_rgb(self.triplet, white, amount)
        return tint
    

    @classmethod
    def named_table(cls) -> Columns:
        """Return a table of named colors."""

        colors = []
        for color in GradientColor.NAMES:
            colors.append(Color(color))
        return Columns(colors, equal=True)

    @classmethod
    def color_table(cls) -> Columns:
        """Return a table of all colors."""
        tables: List[Table] = []
        for colors in [Rich, X11]:
            title = colors.get_title()  # type: ignore
            color_table_row = Table(
                title=title, show_header=True, header_style="bold.magenta"
            )
            color_table_row.add_column("Example", justify="center")
            color_table_row.add_column("Name", justify="center")
            color_table_row.add_column("Hex", justify="center")
            color_table_row.add_column("RGB", justify="center")
            color_table_row.add_column("ColorTriplet", justify="center")

            def add_row(
                color: Color, table: Table = color_table_row, end_section: bool = False
            ) -> Table:
                block = Text("█" * 12, style=f"bold {color.hex}")
                name = Text(color.name, style=f"bold {color.hex}")  # type: ignore
                hex_color = Text(color.hex, style=f" bold {color.hex}")
                rgb_color = color.rgb_text()
                triplet = Text.assemble(
                    *[
                        Text("(", style=f"bold {color.hex}"),
                        Text(f"{color.triplet.red}", style="bold #ff0000"),
                        Text(",", style=f"bold {color.hex}"),
                        Text(f"{color.triplet.green}", style="bold #00ff00"),
                        Text(",", style=f"bold {color.hex}"),
                        Text(f"{color.triplet.blue}", style="bold #00afff"),
                        Text(")", style=f"bold {color.hex}"),
                    ]
                )
                table.add_row(block, name, hex_color, rgb_color, triplet)
                if end_section:
                    table.add_section()
                return table

            for color in colors.NAMES:  # type: ignore
                color_table_row = add_row(cls(color), color_table_row)  # type: ignore
            tables.append(color_table_row)

        return Columns(tables, equal=True)


if __name__ == "__main__":
    console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
    console.print(Color.named_table(), justify="center")
    console.print(Color.color_table(), justify="center")
