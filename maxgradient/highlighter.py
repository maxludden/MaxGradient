"""Custom highlighter to support highlighting gradient colors as well as the default repr highlighting."""
# disable: pylint=[E0f04,W0012]
# disable: pylint
from typing import Tuple

from rich.columns import Columns
from rich.highlighter import RegexHighlighter, _combine_regex

# from maxgradient._gc import GradientColor as GC

NAMES: Tuple[str, ...] = (
    "magenta",
    "violet",
    "purple",
    "blue",
    "lightblue",
    "cyan",
    "green",
    "yellow",
    "orange",
    "red",
)
HEX: Tuple[str, ...] = (
    "#ff00ff",
    "#af00ff",
    "#5f00ff",
    "#0000ff",
    "#0088ff",
    "#00ffff",
    "#00ff00",
    "#ffff00",
    "#ff8800",
    "#ff0000",
)
HEX3: Tuple[str, ...] = (
    "#f0f",
    "#a0f",
    "#50f",
    "#00f",
    "#08f",
    "#0ff",
    "#0f0",
    "#ff0",
    "#f80",
    "#f00",
)
RGB: Tuple[str, ...] = (
    "rgb(255,0,255)",
    "rgb(175,0,255)",
    "rgb(95,0,255)",
    "rgb(0,0,255)",
    "rgb(0,136,255)",
    "rgb(0,255,255)",
    "rgb(0,255,0)",
    "rgb(255,255,0)",
    "rgb(255,136,0)",
    "rgb(255,0,0)",
)
RGB_TUPLE: Tuple[Tuple[int, int, int], ...] = (
    (255, 0, 255),
    (175, 0, 255),
    (95, 0, 255),
    (0, 0, 255),
    (0, 136, 255),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 136, 0),
    (255, 0, 0),
)


class ColorReprHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "bold."
    highlights = [
        r"(?P<magenta>magenta\b|#[Ff]0[Ff]\b|#[Ff]{2}00[Ff]{2}\b|r?g?b?\(255, ?0, ?255\))",
        r"(?P<violet>violet\b|#a0[Ff]\b|#a[Ff]00[Ff]{2}\b|r?g?b?\(175, ?0, ?255\))",
        r"(?P<purple>purple\b|#50[Ff]\b|#5[Ff]00[Ff]{2}\b|r?g?b?\(95, ?0, ?255\))",
        r"(?P<blue>blue\b|#00[Ff]\b|#0{4}[Ff]{2}\b|r?g?b?\(0, ?0, ?255\))",
        r"(?P<lightblue>lightblue|#08[Ff]\b|#0088[Ff]{2}|r?g?b?\(0, ?136, ?255\))",
        r"(?P<cyan>cyan|#0[Ff]{2}\b|#00[Ff]{4}|r?g?b?\(0, ?255, ?255\))",
        r"(?P<green>green|#0[Ff]0\b|#00[Ff]{2}00|r?g?b?\(0, ?255, ?0\))",
        r"(?P<green>green|#0[Ff]0\b|#00[Ff]{2}00|r?g?b?\(0, ?255, ?0\))",
        r"(?P<yellow>yellow|#[Ff]{2}0\b|#[Ff]{4}00|r?g?b?\(255, ?255, ?0\))",
        r"(?P<orange>orange|#[Ff]80\b|#[Ff]{2}8800|r?g?b?\(255, ?136, ?0\))",
        r"(?P<red>red|#[Ff]00|#[Ff]{2}0{4}\b|r?g?b?\(255, ?0, ?0\))",
        # REPR
        r"(?P<tag_start><)(?P<tag_name>[-\w.:|]*)(?P<tag_contents>[\w\W]*)(?P<tag_end>>)",
        r'(?P<attrib_name>[\w_]{1,50})=(?P<attrib_value>"?[\w_]+"?)?',
        r"(?P<brace>[][{}()])",
        _combine_regex(
            r"(?P<ipv4>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",
            r"(?P<ipv6>([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})",
            r"(?P<eui64>(?:[0-9A-Fa-f]{1,2}-){7}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){7}[0-9A-Fa-f]{1,2}|\
                (?:[0-9A-Fa-f]{4}\.){3}[0-9A-Fa-f]{4})",
            r"(?P<eui48>(?:[0-9A-Fa-f]{1,2}-){5}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){5}[0-9A-Fa-f]{1,2}|\
                (?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})",
            r"(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})",
            r"(?P<call>[\w.]*?)\(",
            r"\b(?P<bool_true>True)\b|\b(?P<bool_false>False)\b|\b(?P<none>None)\b",
            r"(?P<ellipsis>\.\.\.)",
            r"(?P<number_complex>(?<!\w)(?:\-?[0-9]+\.?[0-9]*(?:e[-+]?\d+?)?)(?:[-+](?:[0-9]+\.?[0-9]*(?:e[-+]?\d+)?))?j)",
            r"(?P<number>(?<!\w)\-?[0-9]+\.?[0-9]*(e[-+]?\d+?)?\b|0x[0-9a-fA-F]*)",
            r"(?P<path>\B(/[-\w._+]+)*\/)(?P<filename>[-\w._+]*)?",
            r"(?<![\\\w])(?P<str>b?'''.*?(?<!\\)'''|b?'.*?(?<!\\)'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
            r"(?P<url>(file|https|http|ws|wss)://[-0-9a-zA-Z$_+!`(),.?/;:&=%#]*)",
        ),
    ]


if __name__ == "__main__":
    from maxgradient.console import Console

    console = Console(highlighter=ColorReprHighlighter())

    console.print(
        "\nThis is a test of the ColorReprHighlighter",
        justify="center",
        highlight=True,
        style="bold",
    )
    # for item in [NAMES, HEX, HEX3, RGB, RGB_TUPLE]:
    colors = []
    for x in range(10):
        colors.append(f"Name:{NAMES[x]}")
        colors.append(f"3-Digit Hex:{HEX3[x]}")
        colors.append(f"Hex:{HEX[x]}")
        colors.append(f"RGB:{RGB[x]}")
        colors.append(f"RGB Tuple:{RGB_TUPLE[x]}")
    console.line(2)
    console.print(
        Columns(colors, equal=True, padding=(1, 8)),
        justify="center",
        width=150,
        highlight=True,
        style="bold",
    )
    console.line(2)
    console.print(
        f"The colors that are used to make up a gradient are {', '.join(NAMES)}",
        highlight=True,
    )
