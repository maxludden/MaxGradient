"""Purpose: Contains a tuple of all the colors that the Rich library supports."""
# pylint: disable=E0401
from functools import lru_cache
from re import findall
from typing import Tuple

from rich.style import Style
from rich.table import Table
from rich.text import Text

from maxgradient.log import Console, Log, Optional

console = Console()
log = Log()


class Rich:
    """Rich standard colors."""

    NAMES: Tuple[str, ...] = (
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "bright_black",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
        "bright_white",
        "grey0",
        "navy_blue",
        "dark_blue",
        "blue3",
        "blue1",
        "dark_green",
        "deep_sky_blue4",
        "dodger_blue3",
        "dodger_blue2",
        "green4",
        "spring_green4",
        "turquoise4",
        "deep_sky_blue3",
        "dodger_blue1",
        "dark_cyan",
        "light_sea_green",
        "deep_sky_blue2",
        "deep_sky_blue1",
        "green3",
        "spring_green3",
        "cyan3",
        "dark_turquoise",
        "turquoise2",
        "green1",
        "spring_green2",
        "spring_green1",
        "medium_spring_green",
        "cyan2",
        "cyan1",
        "purple4",
        "purple3",
        "blue_violet",
        "grey37",
        "medium_purple4",
        "slate_blue3",
        "royal_blue1",
        "chartreuse4",
        "pale_turquoise4",
        "steel_blue",
        "steel_blue3",
        "cornflower_blue",
        "dark_sea_green4",
        "cadet_blue",
        "sky_blue3",
        "chartreuse3",
        "sea_green3",
        "aquamarine3",
        "medium_turquoise",
        "steel_blue1",
        "sea_green2",
        "sea_green1",
        "dark_slate_gray2",
        "dark_red",
        "dark_magenta",
        "orange4",
        "light_pink4",
        "plum4",
        "medium_purple3",
        "slate_blue1",
        "wheat4",
        "grey53",
        "light_slate_grey",
        "medium_purple",
        "light_slate_blue",
        "yellow4",
        "dark_sea_green",
        "light_sky_blue3",
        "sky_blue2",
        "chartreuse2",
        "pale_green3",
        "dark_slate_gray3",
        "sky_blue1",
        "chartreuse1",
        "light_green",
        "aquamarine1",
        "dark_slate_gray1",
        "deep_pink4",
        "medium_violet_red",
        "dark_violet",
        "purple",
        "medium_orchid3",
        "medium_orchid",
        "dark_goldenrod",
        "rosy_brown",
        "grey63",
        "medium_purple2",
        "medium_purple1",
        "dark_khaki",
        "navajo_white3",
        "grey69",
        "light_steel_blue3",
        "light_steel_blue",
        "dark_olive_green3",
        "dark_sea_green3",
        "light_cyan3",
        "light_sky_blue1",
        "green_yellow",
        "dark_olive_green2",
        "pale_green1",
        "dark_sea_green2",
        "pale_turquoise1",
        "red3",
        "deep_pink3",
        "magenta3",
        "dark_orange3",
        "indian_red",
        "hot_pink3",
        "hot_pink2",
        "orchid",
        "orange3",
        "light_salmon3",
        "light_pink3",
        "pink3",
        "plum3",
        "violet",
        "gold3",
        "light_goldenrod3",
        "tan",
        "misty_rose3",
        "thistle3",
        "plum2",
        "yellow3",
        "khaki3",
        "light_yellow3",
        "grey84",
        "light_steel_blue1",
        "yellow2",
        "dark_olive_green1",
        "dark_sea_green1",
        "honeydew2",
        "light_cyan1",
        "red1",
        "deep_pink2",
        "deep_pink1",
        "magenta2",
        "magenta1",
        "orange_red1",
        "indian_red1",
        "hot_pink",
        "medium_orchid1",
        "dark_orange",
        "salmon1",
        "light_coral",
        "pale_violet_red1",
        "orchid2",
        "orchid1",
        "orange1",
        "sandy_brown",
        "light_salmon1",
        "light_pink1",
        "pink1",
        "plum1",
        "gold1",
        "light_goldenrod2",
        "navajo_white1",
        "misty_rose1",
        "thistle1",
        "yellow1",
        "light_goldenrod1",
        "khaki1",
        "wheat1",
        "cornsilk1",
        "grey100",
        "grey3",
        "grey7",
        "grey11",
        "grey15",
        "grey19",
        "grey23",
        "grey27",
        "grey30",
        "grey35",
        "grey39",
        "grey42",
        "grey46",
        "grey50",
        "grey54",
        "grey58",
        "grey62",
        "grey66",
        "grey70",
        "grey74",
        "grey78",
        "grey82",
        "grey85",
        "grey89",
        "grey93",
    )
    HEX: Tuple[str, ...] = (
        "#010101",
        "#FF0000",
        "#00FF00",
        "#FFFF00",
        "#0000FF",
        "#FF00FF",
        "#00FFFF",
        "#FFFFFF",
        "#2D2D2D",
        "#D20000",
        "#00D200",
        "#D2D200",
        "#0000D2",
        "#D200D2",
        "#00D2D2",
        "#D2D2D2",
        "#000000",
        "#00005f",
        "#000087",
        "#0000d7",
        "#0000ff",
        "#005f00",
        "#005faf",
        "#005fd7",
        "#005fff",
        "#008700",
        "#00875f",
        "#008787",
        "#0087d7",
        "#0087ff",
        "#00af87",
        "#00afaf",
        "#00afd7",
        "#00afff",
        "#00d700",
        "#00d75f",
        "#00d7af",
        "#00d7d7",
        "#00d7ff",
        "#00ff00",
        "#00ff5f",
        "#00ff87",
        "#00ffaf",
        "#00ffd7",
        "#00ffff",
        "#5f00af",
        "#5f00d7",
        "#5f00ff",
        "#5f5f5f",
        "#5f5f87",
        "#5f5fd7",
        "#5f5fff",
        "#5f8700",
        "#5f8787",
        "#5f87af",
        "#5f87d7",
        "#5f87ff",
        "#5faf5f",
        "#5fafaf",
        "#5fafd7",
        "#5fd700",
        "#5fd787",
        "#5fd7af",
        "#5fd7d7",
        "#5fd7ff",
        "#5fff5f",
        "#5fffaf",
        "#5fffff",
        "#870000",
        "#8700af",
        "#875f00",
        "#875f5f",
        "#875f87",
        "#875fd7",
        "#875fff",
        "#87875f",
        "#878787",
        "#8787af",
        "#8787d7",
        "#8787ff",
        "#87af00",
        "#87af87",
        "#87afd7",
        "#87afff",
        "#87d700",
        "#87d787",
        "#87d7d7",
        "#87d7ff",
        "#87ff00",
        "#87ff87",
        "#87ffd7",
        "#87ffff",
        "#af005f",
        "#af0087",
        "#af00d7",
        "#af00ff",
        "#af5faf",
        "#af5fd7",
        "#af8700",
        "#af8787",
        "#af87af",
        "#af87d7",
        "#af87ff",
        "#afaf5f",
        "#afaf87",
        "#afafaf",
        "#afafd7",
        "#afafff",
        "#afd75f",
        "#afd787",
        "#afd7d7",
        "#afd7ff",
        "#afff00",
        "#afff5f",
        "#afff87",
        "#afffaf",
        "#afffff",
        "#d70000",
        "#d70087",
        "#d700d7",
        "#d75f00",
        "#d75f5f",
        "#d75f87",
        "#d75faf",
        "#d75fd7",
        "#d78700",
        "#d7875f",
        "#d78787",
        "#d787af",
        "#d787d7",
        "#d787ff",
        "#d7af00",
        "#d7af5f",
        "#d7af87",
        "#d7afaf",
        "#d7afd7",
        "#d7afff",
        "#d7d700",
        "#d7d75f",
        "#d7d7af",
        "#d7d7d7",
        "#d7d7ff",
        "#d7ff00",
        "#d7ff87",
        "#d7ffaf",
        "#d7ffd7",
        "#d7ffff",
        "#ff0000",
        "#ff005f",
        "#ff00af",
        "#ff00d7",
        "#ff00ff",
        "#ff5f00",
        "#ff5f87",
        "#ff5fd7",
        "#ff5fff",
        "#ff8700",
        "#ff875f",
        "#ff8787",
        "#ff87af",
        "#ff87d7",
        "#ff87ff",
        "#ffaf00",
        "#ffaf5f",
        "#ffaf87",
        "#ffafaf",
        "#ffafd7",
        "#ffafff",
        "#ffd700",
        "#ffd787",
        "#ffd7af",
        "#ffd7d7",
        "#ffd7ff",
        "#ffff00",
        "#ffff5f",
        "#ffff87",
        "#ffffaf",
        "#ffffd7",
        "#ffffff",
        "#080808",
        "#121212",
        "#1c1c1c",
        "#262626",
        "#303030",
        "#3a3a3a",
        "#444444",
        "#4e4e4e",
        "#585858",
        "#626262",
        "#6c6c6c",
        "#767676",
        "#808080",
        "#8a8a8a",
        "#949494",
        "#9e9e9e",
        "#a8a8a8",
        "#b2b2b2",
        "#bcbcbc",
        "#c6c6c6",
        "#d0d0d0",
        "#dadada",
        "#e4e4e4",
        "#eeeeee",
    )
    RGB: Tuple[str, ...] = (
        "rgb(1,1,1)",
        "rgb(255,0,0)",
        "rgb(0,255,0)",
        "rgb(255,255,0)",
        "rgb(0,0,255)",
        "rgb(255,0,255)",
        "rgb(0,255,255)",
        "rgb(255,255,255)",
        "rgb(45,45,45)",
        "rgb(210,0,0)",
        "rgb(0,210,0)",
        "rgb(210,210,0)",
        "rgb(0,0,210)",
        "rgb(210,0,210)",
        "rgb(0,210,210)",
        "rgb(210,210,210)",
        "rgb(0,0,0)",
        "rgb(0,0,95)",
        "rgb(0,0,135)",
        "rgb(0,0,215)",
        "rgb(0,0,255)",
        "rgb(0,95,0)",
        "rgb(0,95,175)",
        "rgb(0,95,215)",
        "rgb(0,95,255)",
        "rgb(0,135,0)",
        "rgb(0,135,95)",
        "rgb(0,135,135)",
        "rgb(0,135,215)",
        "rgb(0,135,255)",
        "rgb(0,175,135)",
        "rgb(0,175,175)",
        "rgb(0,175,215)",
        "rgb(0,175,255)",
        "rgb(0,215,0)",
        "rgb(0,215,95)",
        "rgb(0,215,175)",
        "rgb(0,215,215)",
        "rgb(0,215,255)",
        "rgb(0,255,0)",
        "rgb(0,255,95)",
        "rgb(0,255,135)",
        "rgb(0,255,175)",
        "rgb(0,255,215)",
        "rgb(0,255,255)",
        "rgb(95,0,175)",
        "rgb(95,0,215)",
        "rgb(95,0,255)",
        "rgb(95,95,95)",
        "rgb(95,95,135)",
        "rgb(95,95,215)",
        "rgb(95,95,255)",
        "rgb(95,135,0)",
        "rgb(95,135,135)",
        "rgb(95,135,175)",
        "rgb(95,135,215)",
        "rgb(95,135,255)",
        "rgb(95,175,95)",
        "rgb(95,175,175)",
        "rgb(95,175,215)",
        "rgb(95,215,0)",
        "rgb(95,215,135)",
        "rgb(95,215,175)",
        "rgb(95,215,215)",
        "rgb(95,215,255)",
        "rgb(95,255,95)",
        "rgb(95,255,175)",
        "rgb(95,255,255)",
        "rgb(135,0,0)",
        "rgb(135,0,175)",
        "rgb(135,95,0)",
        "rgb(135,95,95)",
        "rgb(135,95,135)",
        "rgb(135,95,215)",
        "rgb(135,95,255)",
        "rgb(135,135,95)",
        "rgb(135,135,135)",
        "rgb(135,135,175)",
        "rgb(135,135,215)",
        "rgb(135,135,255)",
        "rgb(135,175,0)",
        "rgb(135,175,135)",
        "rgb(135,175,215)",
        "rgb(135,175,255)",
        "rgb(135,215,0)",
        "rgb(135,215,135)",
        "rgb(135,215,215)",
        "rgb(135,215,255)",
        "rgb(135,255,0)",
        "rgb(135,255,135)",
        "rgb(135,255,215)",
        "rgb(135,255,255)",
        "rgb(175,0,95)",
        "rgb(175,0,135)",
        "rgb(175,0,215)",
        "rgb(175,0,255)",
        "rgb(175,95,175)",
        "rgb(175,95,215)",
        "rgb(175,135,0)",
        "rgb(175,135,135)",
        "rgb(175,135,175)",
        "rgb(175,135,215)",
        "rgb(175,135,255)",
        "rgb(175,175,95)",
        "rgb(175,175,135)",
        "rgb(175,175,175)",
        "rgb(175,175,215)",
        "rgb(175,175,255)",
        "rgb(175,215,95)",
        "rgb(175,215,135)",
        "rgb(175,215,215)",
        "rgb(175,215,255)",
        "rgb(175,255,0)",
        "rgb(175,255,95)",
        "rgb(175,255,135)",
        "rgb(175,255,175)",
        "rgb(175,255,255)",
        "rgb(215,0,0)",
        "rgb(215,0,135)",
        "rgb(215,0,215)",
        "rgb(215,95,0)",
        "rgb(215,95,95)",
        "rgb(215,95,135)",
        "rgb(215,95,175)",
        "rgb(215,95,215)",
        "rgb(215,135,0)",
        "rgb(215,135,95)",
        "rgb(215,135,135)",
        "rgb(215,135,175)",
        "rgb(215,135,215)",
        "rgb(215,135,255)",
        "rgb(215,175,0)",
        "rgb(215,175,95)",
        "rgb(215,175,135)",
        "rgb(215,175,175)",
        "rgb(215,175,215)",
        "rgb(215,175,255)",
        "rgb(215,215,0)",
        "rgb(215,215,95)",
        "rgb(215,215,175)",
        "rgb(215,215,215)",
        "rgb(215,215,255)",
        "rgb(215,255,0)",
        "rgb(215,255,135)",
        "rgb(215,255,175)",
        "rgb(215,255,215)",
        "rgb(215,255,255)",
        "rgb(255,0,0)",
        "rgb(255,0,95)",
        "rgb(255,0,175)",
        "rgb(255,0,215)",
        "rgb(255,0,255)",
        "rgb(255,95,0)",
        "rgb(255,95,135)",
        "rgb(255,95,215)",
        "rgb(255,95,255)",
        "rgb(255,135,0)",
        "rgb(255,135,95)",
        "rgb(255,135,135)",
        "rgb(255,135,175)",
        "rgb(255,135,215)",
        "rgb(255,135,255)",
        "rgb(255,175,0)",
        "rgb(255,175,95)",
        "rgb(255,175,135)",
        "rgb(255,175,175)",
        "rgb(255,175,215)",
        "rgb(255,175,255)",
        "rgb(255,215,0)",
        "rgb(255,215,135)",
        "rgb(255,215,175)",
        "rgb(255,215,215)",
        "rgb(255,215,255)",
        "rgb(255,255,0)",
        "rgb(255,255,95)",
        "rgb(255,255,135)",
        "rgb(255,255,175)",
        "rgb(255,255,215)",
        "rgb(255,255,255)",
        "rgb(8,8,8)",
        "rgb(18,18,18)",
        "rgb(28,28,28)",
        "rgb(38,38,38)",
        "rgb(48,48,48)",
        "rgb(58,58,58)",
        "rgb(68,68,68)",
        "rgb(78,78,78)",
        "rgb(88,88,88)",
        "rgb(98,98,98)",
        "rgb(108,108,108)",
        "rgb(118,118,118)",
        "rgb(128,128,128)",
        "rgb(138,138,138)",
        "rgb(148,148,148)",
        "rgb(158,158,158)",
        "rgb(168,168,168)",
        "rgb(178,178,178)",
        "rgb(188,188,188)",
        "rgb(198,198,198)",
        "rgb(208,208,208)",
        "rgb(218,218,218)",
        "rgb(228,228,228)",
        "rgb(238,238,238)",
    )

    RGB_TUPLE: Tuple[Tuple[int, int, int], ...] = (
        (1, 1, 1),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
        (45, 45, 45),
        (210, 0, 0),
        (0, 210, 0),
        (210, 210, 0),
        (0, 0, 210),
        (210, 0, 210),
        (0, 210, 210),
        (210, 210, 210),
        (0, 0, 0),
        (0, 0, 95),
        (0, 0, 135),
        (0, 0, 215),
        (0, 0, 255),
        (0, 95, 0),
        (0, 95, 175),
        (0, 95, 215),
        (0, 95, 255),
        (0, 135, 0),
        (0, 135, 95),
        (0, 135, 135),
        (0, 135, 215),
        (0, 135, 255),
        (0, 175, 135),
        (0, 175, 175),
        (0, 175, 215),
        (0, 175, 255),
        (0, 215, 0),
        (0, 215, 95),
        (0, 215, 175),
        (0, 215, 215),
        (0, 215, 255),
        (0, 255, 0),
        (0, 255, 95),
        (0, 255, 135),
        (0, 255, 175),
        (0, 255, 215),
        (0, 255, 255),
        (95, 0, 175),
        (95, 0, 215),
        (95, 0, 255),
        (95, 95, 95),
        (95, 95, 135),
        (95, 95, 215),
        (95, 95, 255),
        (95, 135, 0),
        (95, 135, 135),
        (95, 135, 175),
        (95, 135, 215),
        (95, 135, 255),
        (95, 175, 95),
        (95, 175, 175),
        (95, 175, 215),
        (95, 215, 0),
        (95, 215, 135),
        (95, 215, 175),
        (95, 215, 215),
        (95, 215, 255),
        (95, 255, 95),
        (95, 255, 175),
        (95, 255, 255),
        (135, 0, 0),
        (135, 0, 175),
        (135, 95, 0),
        (135, 95, 95),
        (135, 95, 135),
        (135, 95, 215),
        (135, 95, 255),
        (135, 135, 95),
        (135, 135, 135),
        (135, 135, 175),
        (135, 135, 215),
        (135, 135, 255),
        (135, 175, 0),
        (135, 175, 135),
        (135, 175, 215),
        (135, 175, 255),
        (135, 215, 0),
        (135, 215, 135),
        (135, 215, 215),
        (135, 215, 255),
        (135, 255, 0),
        (135, 255, 135),
        (135, 255, 215),
        (135, 255, 255),
        (175, 0, 95),
        (175, 0, 135),
        (175, 0, 215),
        (175, 0, 255),
        (175, 95, 175),
        (175, 95, 215),
        (175, 135, 0),
        (175, 135, 135),
        (175, 135, 175),
        (175, 135, 215),
        (175, 135, 255),
        (175, 175, 95),
        (175, 175, 135),
        (175, 175, 175),
        (175, 175, 215),
        (175, 175, 255),
        (175, 215, 95),
        (175, 215, 135),
        (175, 215, 215),
        (175, 215, 255),
        (175, 255, 0),
        (175, 255, 95),
        (175, 255, 135),
        (175, 255, 175),
        (175, 255, 255),
        (215, 0, 0),
        (215, 0, 135),
        (215, 0, 215),
        (215, 95, 0),
        (215, 95, 95),
        (215, 95, 135),
        (215, 95, 175),
        (215, 95, 215),
        (215, 135, 0),
        (215, 135, 95),
        (215, 135, 135),
        (215, 135, 175),
        (215, 135, 215),
        (215, 135, 255),
        (215, 175, 0),
        (215, 175, 95),
        (215, 175, 135),
        (215, 175, 175),
        (215, 175, 215),
        (215, 175, 255),
        (215, 215, 0),
        (215, 215, 95),
        (215, 215, 175),
        (215, 215, 215),
        (215, 215, 255),
        (215, 255, 0),
        (215, 255, 135),
        (215, 255, 175),
        (215, 255, 215),
        (215, 255, 255),
        (255, 0, 0),
        (255, 0, 95),
        (255, 0, 175),
        (255, 0, 215),
        (255, 0, 255),
        (255, 95, 0),
        (255, 95, 135),
        (255, 95, 215),
        (255, 95, 255),
        (255, 135, 0),
        (255, 135, 95),
        (255, 135, 135),
        (255, 135, 175),
        (255, 135, 215),
        (255, 135, 255),
        (255, 175, 0),
        (255, 175, 95),
        (255, 175, 135),
        (255, 175, 175),
        (255, 175, 215),
        (255, 175, 255),
        (255, 215, 0),
        (255, 215, 135),
        (255, 215, 175),
        (255, 215, 215),
        (255, 215, 255),
        (255, 255, 0),
        (255, 255, 95),
        (255, 255, 135),
        (255, 255, 175),
        (255, 255, 215),
        (255, 255, 255),
        (8, 8, 8),
        (18, 18, 18),
        (28, 28, 28),
        (38, 38, 38),
        (48, 48, 48),
        (58, 58, 58),
        (68, 68, 68),
        (78, 78, 78),
        (88, 88, 88),
        (98, 98, 98),
        (108, 108, 108),
        (118, 118, 118),
        (128, 128, 128),
        (138, 138, 138),
        (148, 148, 148),
        (158, 158, 158),
        (168, 168, 168),
        (178, 178, 178),
        (188, 188, 188),
        (198, 198, 198),
        (208, 208, 208),
        (218, 218, 218),
        (228, 228, 228),
        (238, 238, 238),
    )

    @classmethod
    @lru_cache(maxsize=203, typed=True)
    def get_names(cls) -> Tuple[str, ...]:
        """Retrieve rich colors"""
        return Rich.NAMES

    @classmethod
    @lru_cache(maxsize=203, typed=True)
    def get_hex(cls) -> Tuple[str, ...]:
        """Retrieve rich hex colors"""
        return Rich.HEX

    @classmethod
    @lru_cache(maxsize=203, typed=True)
    def get_rgb(cls) -> Tuple[str, ...]:
        """Retrieve rich rgb colors"""
        return Rich.RGB

    @classmethod
    @lru_cache(maxsize=10, typed=False)
    def get_color(cls, color: str) -> Optional[Tuple[int, int, int]]:
        """Parse rich colors for color"""
        for group in [cls.get_names(), cls.get_hex(), cls.get_rgb()]:
            if color in group:
                index = group.index(color)
                rgb = cls.get_rgb()[index]
                return tuple(map(int, rgb[4:-1].split(",")))
        return None

    @staticmethod
    def rgb_to_tuple(rgb: str) -> Tuple[int, int, int]:
        """Convert a rgb string to a tuple of ints"""
        log.debug(f"Converting {rgb} to tuple...")
        rgb_match = findall(r"r?g?b?\((\d+),(\d+),(\d+)\)", rgb)
        if rgb_match:
            return tuple(int(x) for x in rgb_match[0])
        raise ValueError(f"Invalid rgb string: {rgb}")

    @staticmethod
    def get_title() -> Text:
        """Generate a colored text title."""
        letter_r1 = Text("R", style=Style(color="#0000FF", bold=True))
        letter_i = Text("i", style=Style(color="#5F00FF", bold=True))
        letter_c1 = Text("c", style=Style(color="#AF00FF", bold=True))
        letter_h = Text("h", style=Style(color="#FF00FF", bold=True))
        letter_c2 = Text("C", style=Style(color="#ff0000", bold=True))
        letter_o = Text("o", style=Style(color="#ff8800", bold=True))
        letter_l = Text("l", style=Style(color="#ffff00", bold=True))
        letter_o2 = Text("o", style=Style(color="#00ff00", bold=True))
        letter_r2 = Text("r", style=Style(color="#00ffff", bold=True))
        letter_s = Text("s", style=Style(color="#0088ff", bold=True))
        title = [
            letter_r1,
            letter_i,
            letter_c1,
            letter_h,
            letter_c2,
            letter_o,
            letter_l,
            letter_o2,
            letter_r2,
            letter_s,
        ]
        return Text.assemble(*title)

    @staticmethod
    def sample_title() -> Text:
        """Generate a colored header."""
        sample = [
            Text("S", style="bold #0000FF"),
            Text("a", style="bold #5F00FF"),
            Text("m", style="bold #AF00FF"),
            Text("p", style="bold #FF00FF"),
            Text("l", style="bold #ff0000"),
            Text("e", style="bold #ff8800"),
        ]
        return Text.assemble(*sample)

    @staticmethod
    def name_title() -> Text:
        """Generate a colored header."""
        name = [
            Text("N", style="bold #FFFF00"),
            Text("a", style="bold #00FF00"),
            Text("m", style="bold #00FFFF"),
            Text("e", style="bold #0088FF"),
        ]
        return Text.assemble(*name)

    @staticmethod
    def hex_title() -> Text:
        """Generate a colored header."""
        hex_letters = [
            Text("H", style="bold #0000FF"),
            Text("e", style="bold #5F00FF"),
            Text("x", style="bold #AF00FF"),
        ]
        return Text.assemble(*hex_letters)

    @staticmethod
    def rgb_title() -> Text:
        """Generate a colored header."""
        rgb = [
            Text("R", style="bold #FF00FF"),
            Text("G", style="bold #ff0000"),
            Text("B", style="bold #ff8800"),
        ]
        return Text.assemble(*rgb)

    @classmethod
    def color_table(cls) -> Table:
        """Return a table of the rich library's Standard Colors."""
        color_block = "█" * 10
        NAMES = cls.get_names()
        HEX = cls.get_hex()
        RGB = cls.get_rgb()
        color_table = Table(
            title=cls.get_title(),
            show_header=True,
            border_style="dim white",
            expand=False,
            show_lines=False,
            padding=(0, 2),
        )
        sample_text: Text = cls.sample_title()
        color_table.add_column(sample_text, width=14, justify="center", style="bold")
        name_text: Text = cls.name_title()
        color_table.add_column(name_text, width=18, justify="left", style="bold")
        hex_text: Text = cls.hex_title()
        color_table.add_column(hex_text, width=10, justify="center", style="bold")
        rgb_text: Text = cls.rgb_title()
        color_table.add_column(rgb_text, width=16, justify="left", style="bold")
        for index, _ in enumerate(HEX):
            color_name = str(NAMES[index]).capitalize()
            color_hex = str(HEX[index]).upper()
            color_rgb = str(RGB[index]).lower()
            color_table.add_row(
                Text(color_block, style=color_hex),
                Text(color_name, style=color_hex),
                Text(color_hex, style=color_hex),
                Text(color_rgb, style=color_hex),
            )

        return color_table


if __name__ == "__main__":
    console.print(Rich.color_table(), justify="center")
