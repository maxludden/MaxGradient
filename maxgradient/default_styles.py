"""A container for the default styles used by GradientConsole."""
# pylint: disable=redefined-outer-name,consider-using-dict-items
from typing import Dict, Mapping

from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.live import Live

GRADIENT_STYLES: Mapping[str, StyleType] = {
    "none": Style.null(),
    "reset": Style(
        color="default",
        bgcolor="default",
        dim=False,
        bold=False,
        italic=False,
        underline=False,
        blink=False,
        blink2=False,
        reverse=False,
        conceal=False,
        strike=False,
    ),
    "dim": Style(dim=True),
    "bright": Style(dim=False),
    "bold": Style(bold=True),
    "strong": Style(bold=True),
    "code": Style(reverse=True, bold=True),
    "italic": Style(italic=True),
    "emphasize": Style(italic=True),
    "underline": Style(underline=True),
    "blink": Style(blink=True),
    "blink2": Style(blink2=True),
    "reverse": Style(reverse=True),
    "strike": Style(strike=True),
    "white": Style(color="#ffffff"),
    "bold.white": Style(color="#ffffff", bold=True),
    "cs.white": Style(color="#ffffff", bgcolor="#ffffff", bold=True),
    "style.white": Style(color="#ffffff", bgcolor="default", bold=True),
    "bg_style.white": Style(color="#000000", bgcolor="#ffffff", bold=True),
    "lightgrey": Style(color="#dddddd"),
    "bold.lightgrey": Style(color="#dddddd", bold=True),
    "cs.lightgrey": Style(color="#dddddd", bgcolor="#dddddd", bold=True),
    "style.lightgrey": Style(color="#dddddd", bgcolor="default", bold=True),
    "bg_style.lightgrey": Style(color="#000000", bgcolor="#dddddd", bold=True),
    "lightgray": Style(color="#dddddd"),
    "bold.lightgray": Style(color="#dddddd", bold=True),
    "cs.lightgray": Style(color="#dddddd", bgcolor="#dddddd", bold=True),
    "style.lightgray": Style(color="#dddddd", bgcolor="default", bold=True),
    "bg_style.lightgray": Style(color="#000000", bgcolor="#dddddd", bold=True),
    "grey": Style(color="#888888"),
    "bold.grey": Style(color="#888888", bold=True),
    "cs.grey": Style(color="#888888", bgcolor="#888888", bold=True),
    "style.grey": Style(color="#888888", bgcolor="default", bold=True),
    "bg_style.grey": Style(color="#000000", bgcolor="#888888", bold=True),
    "gray": Style(color="#888888"),
    "bold.gray": Style(color="#888888", bold=True),
    "cs.gray": Style(color="#888888", bgcolor="#888888", bold=True),
    "style.gray": Style(color="#888888", bgcolor="default", bold=True),
    "bg_style.gray": Style(color="#000000", bgcolor="#888888", bold=True),
    "darkgrey": Style(color="#444444"),
    "bold.darkgrey": Style(color="#444444", bold=True),
    "cs.darkgrey": Style(color="#444444", bgcolor="#444444", bold=True),
    "style.darkgrey": Style(color="#444444", bgcolor="default", bold=True),
    "bg_style.darkgrey": Style(color="#ffffff", bgcolor="#444444", bold=True),
    "darkgray": Style(color="#444444"),
    "bold.darkgray": Style(color="#444444", bold=True),
    "cs.darkgray": Style(color="#444444", bgcolor="#444444", bold=True),
    "style.darkgray": Style(color="#444444", bgcolor="default", bold=True),
    "bg_style.darkgray": Style(color="#ffffff", bgcolor="#444444", bold=True),
    "black": Style(color="#000000"),
    "bold.black": Style(color="#000000", bold=True),
    "cs.black": Style(color="#000000", bgcolor="#000000", bold=True),
    "style.black": Style(color="#000000", bgcolor="default", bold=True),
    "bg_style.black": Style(color="#ffffff", bgcolor="#000000", bold=True),
    "red": Style(color="#ff0000"),
    "bold.red": Style(color="#ff0000", bold=True),
    "cs.red": Style(color="#ff0000", bgcolor="#ff0000", bold=True),
    "style.red": Style(color="#ff0000", bgcolor="default", bold=True),
    "bg_style.red": Style(color="#000000", bgcolor="#ff0000", bold=True),
    "orange": Style(color="#ff8800"),
    "bold.orange": Style(color="#ff8800", bold=True),
    "cs.orange": Style(color=None, bgcolor="#ff8800", bold=True),
    "style.orange": Style(color="#ff8800", bgcolor="default", bold=True),
    "bg_style.orange": Style(color="#000000", bgcolor="#ff8800", bold=True),
    "yellow": Style(color="#ffff00"),
    "bold.yellow": Style(color="#ffff00", bold=True),
    "cs.yellow": Style(color="#ffff00", bgcolor="#ffff00", bold=True),
    "style.yellow": Style(color="#ffff00", bgcolor="default", bold=True),
    "bg_style.yellow": Style(color="#000000", bgcolor="#ffff00", bold=True),
    "green": Style(color="#00ff00"),
    "bold.green": Style(color="#00ff00", bold=True),
    "cs.green": Style(color="#00ff00", bgcolor="#00ff00", bold=True),
    "style.green": Style(color="#00ff00", bgcolor="default", bold=True),
    "bg_style.green": Style(color="#000000", bgcolor="#00ff00", bold=True),
    "cyan": Style(color="#00ffff"),
    "bold.cyan": Style(color="#00ffff", bold=True),
    "cs.cyan": Style(color="#00ffff", bgcolor="#00ffff", bold=True),
    "style.cyan": Style(color="#00ffff", bgcolor="default", bold=True),
    "bg_style.cyan": Style(color="#000000", bgcolor="#00ffff", bold=True),
    "lightblue": Style(color="#0088ff"),
    "bold.lightblue": Style(color="#0088ff", bold=True),
    "cs.lightblue": Style(color="#0088ff", bgcolor="#0088ff", bold=True),
    "style.lightblue": Style(color="#0088ff", bgcolor="default", bold=True),
    "bg_style.lightblue": Style(color="#000000", bgcolor="#0088ff", bold=True),
    "blue": Style(color="#0000ff"),
    "bold.blue": Style(color="#0000ff", bold=True),
    "cs.blue": Style(color="#0000ff", bgcolor="#0000ff", bold=True),
    "style.blue": Style(color="#0000ff", bgcolor="default", bold=True),
    "bg_style.blue": Style(color="#ffffff", bgcolor="#0000ff", bold=True),
    "purple": Style(color="#5F00FF"),
    "bold.purple": Style(color="#5f00ff", bold=True),
    "cs.purple": Style(color="#5f00ff", bgcolor="#5f00ff", bold=True),
    "style.purple": Style(color="#5f00ff", bgcolor="default", bold=True),
    "bg_style.purple": Style(color="#ffffff", bgcolor="#5f00ff", bold=True),
    "violet": Style(color="#af00ff"),
    "bold.violet": Style(color="#af00ff", bold=True),
    "cs.violet": Style(color="#af00ff", bgcolor="#af00ff", bold=True),
    "style.violet": Style(color="#af00ff", bgcolor="default", bold=True),
    "bg_style.violet": Style(color="#000000", bgcolor="#af00ff", bold=True),
    "magenta": Style(color="#ff00ff"),
    "bold.magenta": Style(color="#ff00ff", bold=True),
    "cs.magenta": Style(color="#ff00ff", bgcolor="#ff00ff", bold=True),
    "style.magenta": Style(color="#ff00ff", bgcolor="default", bold=True),
    "bg_style.magenta": Style(color="#000000", bgcolor="#ff00ff", bold=True),
    "inspect.attr": Style(color="#ffff00", italic=True),
    "inspect.attr.dunder": Style(color="#ffff00", italic=True, dim=True),
    "inspect.callable": Style(bold=True, color="#ff0000"),
    "inspect.async_def": Style(italic=True, color="#00ffff"),
    "inspect.def": Style(italic=True, color="#00ffff"),
    "inspect.class": Style(italic=True, color="#00ffff"),
    "inspect.error": Style(bold=True, color="#ff0000"),
    "inspect.equals": Style(),
    "inspect.help": Style(color="#00ffff"),
    "inspect.doc": Style(dim=True),
    "inspect.value.border": Style(color="#00ff00"),
    "live.ellipsis": Style(bold=True, color="#ff0000"),
    "layout.tree.row": Style(dim=False, color="#ff0000"),
    "layout.tree.column": Style(dim=False, color="#0000ff"),
    "logging.keyword": Style(bold=True, color="#ffff00"),
    "logging.level.notset": Style(dim=True),
    "logging.level.debug": Style(color="#0088ff"),
    "logging.level.info": Style(color="#ff00ff"),
    "logging.level.success": Style(color="#00ff00", bold=True),
    "logging.level.warning": Style(color="#ff0000"),
    "logging.level.error": Style(color="#ff0000", bold=True),
    "logging.level.critical": Style(color="#ff0000", bold=True, reverse=True),
    "log.level": Style.null(),
    "log.time": Style(color="#00ffff", dim=True),
    "log.message": Style.null(),
    "log.path": Style(dim=True),
    "log.keyword": Style(color="#E3EC84", bold=True, italic=True),
    "log.index": Style(color="#7FD6E8", bold=True, italic=True),
    "log.separator": Style(color="#f0ffff", bold=True, italic=True),
    "syntax.class": Style(color="#7FD6E8", bold=True, italic=True),
    "repr.ellipsis": Style(color="#ffff00"),
    "repr.indent": Style(color="#00ff00", dim=True),
    "repr.error": Style(color="#ff0000", bold=True),
    "repr.str": Style(color="#00ff00", italic=False, bold=False),
    "repr.brace": Style(bold=True),
    "repr.comma": Style(bold=True),
    "repr.ipv4": Style(bold=True, color="#00ff00"),
    "repr.ipv6": Style(bold=True, color="#00ff00"),
    "repr.eui48": Style(bold=True, color="#00ff00"),
    "repr.eui64": Style(bold=True, color="#00ff00"),
    "repr.tag_start": Style(bold=True),
    "repr.tag_name": Style(color="#00ff00", bold=True),
    "repr.tag_contents": Style(color="default"),
    "repr.tag_end": Style(bold=True),
    "repr.attrib_name": Style(color="#ffff00", italic=False),
    "repr.attrib_equal": Style(bold=True),
    "repr.attrib_value": Style(color="#00ff00", italic=False),
    "repr.number": Style(
        color="#8BE8FC", bold=True, italic=False
    ),  # repr.number is identical to
    "repr.number_complex": Style(
        color="#00ffff", bold=True, italic=False
    ),  # repr.number_complex
    "repr.bool_true": Style(color="#00ff00", italic=True),
    "repr.bool_false": Style(color="#ff0000", italic=True),
    "repr.none": Style(color="#00ff00", italic=True),
    "repr.url": Style(underline=True, color="#0000ff", italic=False, bold=False),
    "repr.uuid": Style(color="#ffff00", bold=False),
    "repr.call": Style(color="#00ff00", bold=True),
    "repr.path": Style(color="#00ff00"),
    "repr.filename": Style(color="#00ff00"),
    "rule.line": Style(color="#ffffff", bold=True),
    "rule.text": Style(color="#af00ff", bold=True),
    "json.brace": Style(bold=True),
    "json.bool_true": Style(color="#00ff00", italic=True),
    "json.bool_false": Style(color="#ff0000", italic=True),
    "json.null": Style(color="#00ff00", italic=True),
    "json.number": Style(color="#8BE8FC", bold=True, italic=False),
    "json.str": Style(color="#00ff00", italic=False, bold=False),
    "json.key": Style(color="#0000ff", bold=True),
    "prompt": Style.null(),
    "prompt.choices": Style(color="#ff00ff", bold=True),
    "prompt.default": Style(color="#8BE8FC", bold=True),
    "prompt.invalid": Style(color="#ff0000"),
    "prompt.invalid.choice": Style(color="#ff0000"),
    "pretty": Style.null(),
    "scope.border": Style(color="#0000ff"),
    "scope.key": Style(color="#ffff00", italic=True),
    "scope.key.special": Style(color="#ffff00", italic=True, dim=True),
    "scope.equals": Style(color="#ff0000"),
    "table.header": Style(bold=True),
    "table.footer": Style(bold=True),
    "table.cell": Style.null(),
    "table.title": Style(italic=True),
    "table.caption": Style(italic=True, dim=True),
    "traceback.error": Style(color="#ff0000", italic=True),
    "traceback.border.syntax_error": Style(color="#ff0000"),
    "traceback.border": Style(color="#ff0000"),
    "traceback.text": Style.null(),
    "traceback.title": Style(color="#ff0000", bold=True),
    "traceback.exc_type": Style(color="#ff0000", bold=True),
    "traceback.exc_value": Style.null(),
    "traceback.offset": Style(color="#ff0000", bold=True),
    "bar.back": Style(color="grey23"),
    "bar.complete": Style(color="#646464"),
    "bar.finished": Style(color="#006a20"),
    "bar.pulse": Style(color="#f92672"),
    "progress.description": Style.null(),
    "progress.filesize": Style(color="#00ff00"),
    "progress.filesize.total": Style(color="#00ff00"),
    "progress.download": Style(color="#00ff00"),
    "progress.elapsed": Style(color="#ffff00"),
    "progress.percentage": Style(color="#ff00ff"),
    "progress.remaining": Style(color="#00ffff"),
    "progress.data.speed": Style(color="#ff0000"),
    "progress.spinner": Style(color="#00ff00"),
    "status.spinner": Style(color="#00ff00"),
    "tree": Style(),
    "tree.line": Style(),
    "markdown.paragraph": Style(),
    "markdown.text": Style(),
    "markdown.em": Style(italic=True),
    "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
    "markdown.strong": Style(bold=True),
    "markdown.code": Style(bold=True, color="#00ffff", bgcolor="black"),
    "markdown.code_block": Style(color="#00ffff", bgcolor="black"),
    "markdown.block_quote": Style(color="#00ff00"),
    "markdown.list": Style(color="#00ffff"),
    "markdown.item": Style(),
    "markdown.item.bullet": Style(color="#ffff00", bold=True),
    "markdown.item.number": Style(color="#ffff00", bold=True),
    "markdown.hr": Style(color="#ffffff"),
    "markdown.h1.border": Style(),
    "markdown.h1": Style(bold=True),
    "markdown.h2": Style(bold=True, underline=True),
    "markdown.h3": Style(bold=True),
    "markdown.h4": Style(bold=True, dim=True),
    "markdown.h5": Style(underline=True),
    "markdown.h6": Style(italic=True),
    "markdown.h7": Style(italic=True, dim=True),
    "markdown.link": Style(color="#0000ff"),
    "markdown.link_url": Style(color="#0000ff", underline=True),
    "markdown.s": Style(strike=True),
    "iso8601.date": Style(color="#0000ff"),
    "iso8601.time": Style(color="#ff00ff"),
    "iso8601.timezone": Style(color="#ffff00"),
    "rgb.red": Style(color="#ff0000", bold=True, italic=True),
    "rgb.green": Style(color="#00ff00", bold=True, italic=True),
    "rgb.blue": Style(color="#0088ff", bold=True, italic=True),
}

""" A dictionary that contains if a style is new, edited, or\
    unchanged in comparison to rich.rich.default_style """
EDITED_STYLES: Dict[str, str] = {
    "none": "[dim]Unchanged[/dim]",
    "reset": "[dim]Unchanged[/dim]",
    "dim": "[dim]Unchanged[/dim]",
    "bright": "[dim]Unchanged[/dim]",
    "bold": "[dim]Unchanged[/dim]",
    "strong": "[dim]Unchanged[/dim]",
    "code": "[dim]Unchanged[/dim]",
    "italic": "[dim]Unchanged[/dim]",
    "emphasize": "[dim]Unchanged[/dim]",
    "underline": "[dim]Unchanged[/dim]",
    "blink": "[dim]Unchanged[/dim]",
    "blink2": "[dim]Unchanged[/dim]",
    "reverse": "[dim]Unchanged[/dim]",
    "strike": "[dim]Unchanged[/dim]",
    "black": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.black": ":star: [bold #e1b400]New[/] :star:",
    "cs.black": ":star: [bold #e1b400]New[/] :star:",
    "style.black": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.black": ":star: [bold #e1b400]New[/] :star:",
    "darkgrey": ":star: [bold #e1b400]New[/] :star:",
    "bold.darkgrey": ":star: [bold #e1b400]New[/] :star:",
    "cs.darkgrey": ":star: [bold #e1b400]New[/] :star:",
    "style.darkgrey": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.darkgrey": ":star: [bold #e1b400]New[/] :star:",
    "darkgray": ":star: [bold #e1b400]New[/] :star:",
    "bold.darkgray": ":star: [bold #e1b400]New[/] :star:",
    "cs.darkgray": ":star: [bold #e1b400]New[/] :star:",
    "style.darkgray": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.darkgray": ":star: [bold #e1b400]New[/] :star:",
    "grey": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.grey": ":star: [bold #e1b400]New[/] :star:",
    "cs.grey": ":star: [bold #e1b400]New[/] :star:",
    "style.grey": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.grey": ":star: [bold #e1b400]New[/] :star:",
    "gray": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.gray": ":star: [bold #e1b400]New[/] :star:",
    "cs.gray": ":star: [bold #e1b400]New[/] :star:",
    "style.gray": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.gray": ":star: [bold #e1b400]New[/] :star:",
    "lightgrey": ":star: [bold #e1b400]New[/] :star:",
    "bold.lightgrey": ":star: [bold #e1b400]New[/] :star:",
    "cs.lightgrey": ":star: [bold #e1b400]New[/] :star:",
    "style.lightgrey": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.lightgrey": ":star: [bold #e1b400]New[/] :star:",
    "lightgray": ":star: [bold #e1b400]New[/] :star:",
    "bold.lightgray": ":star: [bold #e1b400]New[/] :star:",
    "cs.lightgray": ":star: [bold #e1b400]New[/] :star:",
    "style.lightgray": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.lightgray": ":star: [bold #e1b400]New[/] :star:",
    "cs.white": ":star: [bold #e1b400]New[/] :star:",
    "style.white": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.white": ":star: [bold #e1b400]New[/] :star:",
    "white": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.white": ":star: [bold #e1b400]New[/] :star:",
    "red": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.red": ":star: [bold #e1b400]New[/] :star:",
    "cs.red": ":star: [bold #e1b400]New[/] :star:",
    "style.red": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.red": ":star: [bold #e1b400]New[/] :star:",
    "orange": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.orange": ":star: [bold #e1b400]New[/] :star:",
    "cs.orange": ":star: [bold #e1b400]New[/] :star:",
    "style.orange": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.orange": "star: [bold #e1b400]New[/] :star:",
    "yellow": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.yellow": ":star: [bold #e1b400]New[/] :star:",
    "cs.yellow": ":star: [bold #e1b400]New[/] :star:",
    "style.yellow": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.yellow": ":star: [bold #e1b400]New[/] :star:",
    "green": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.green": ":star: [bold #e1b400]New[/] :star:",
    "cs.green": ":star: [bold #e1b400]New[/] :star:",
    "style.green": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.green": ":star: [bold #e1b400]New[/] :star:",
    "cyan": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.cyan": ":star: [bold #e1b400]New[/] :star:",
    "cs.cyan": ":star: [bold #e1b400]New[/] :star:",
    "style.cyan": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.cyan": ":star: [bold #e1b400]New[/] :star:",
    "lightblue": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.lightblue": ":star: [bold #e1b400]New[/] :star:",
    "cs.lightblue": ":star: [bold #e1b400]New[/] :star:",
    "style.lightblue": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.lightblue": ":star: [bold #e1b400]New[/] :star:",
    "blue": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.blue": ":star: [bold #e1b400]New[/] :star:",
    "cs.blue": ":star: [bold #e1b400]New[/] :star:",
    "style.blue": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.blue": ":star: [bold #e1b400]New[/] :star:",
    "purple": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.purple": ":star: [bold #e1b400]New[/] :star:",
    "cs.purple": ":star: [bold #e1b400]New[/] :star:",
    "style.purple": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.purple": ":star: [bold #e1b400]New[/] :star:",
    "violet": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.violet": ":star: [bold #e1b400]New[/] :star:",
    "cs.violet": ":star: [bold #e1b400]New[/] :star:",
    "style.violet": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.violet": ":star: [bold #e1b400]New[/] :star:",
    "magenta": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bold.magenta": ":star: [bold #e1b400]New[/] :star:",
    "cs.magenta": ":star: [bold #e1b400]New[/] :star:",
    "style.magenta": ":star: [bold #e1b400]New[/] :star:",
    "bg_style.magenta": ":star: [bold #e1b400]New[/] :star:",
    "inspect.attr": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.attr.dunder": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.callable": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.async_def": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.def": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.class": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.error": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.equals": "[dim]Unchanged[/dim]",
    "inspect.help": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "inspect.doc": "[dim]Unchanged[/dim]",
    "inspect.value.border": "[dim]Unchanged[/dim]",
    "live.ellipsis": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "layout.tree.row": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "layout.tree.column": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.keyword": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.notset": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.debug": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.info": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.success": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.warning": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.error": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "logging.level.critical": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "log.level": "[dim]Unchanged[/dim]",
    "log.time": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "log.message": "[dim]Unchanged[/dim]",
    "log.path": "[dim]Unchanged[/dim]",
    "log.keyword": ":star: [bold #e1b400]New[/] :star:",
    "log.index": ":star: [bold #e1b400]New[/] :star:",
    "log.separator": ":star: [bold #e1b400]New[/] :star:",
    "syntax.class": ":star: [bold #e1b400]New[/] :star:",
    "repr.ellipsis": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.indent": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.error": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.str": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.brace": "[dim]Unchanged[/dim]",
    "repr.comma": "[dim]Unchanged[/dim]",
    "repr.ipv4": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.ipv6": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.eui48": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.eui64": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.tag_start": "[dim]Unchanged[/dim]",
    "repr.tag_name": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.tag_contents": "[dim]Unchanged[/dim]",
    "repr.tag_end": "[dim]Unchanged[/dim]",
    "repr.attrib_name": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.attrib_equal": "[dim]Unchanged[/dim]",
    "repr.attrib_value": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.number": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.number_complex": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.bool_true": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.bool_false": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.none": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.url": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.uuid": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.call": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.path": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "repr.filename": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "rule.line": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "rule.text": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.brace": "[dim]Unchanged[/dim]",
    "json.bool_true": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.bool_false": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.null": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.number": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.str": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "json.key": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "prompt": "[dim]Unchanged[/dim]",
    "prompt.choices": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "prompt.default": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "prompt.invalid": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "prompt.invalid.choice": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "pretty": "[dim]Unchanged[/dim]",
    "scope.border": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "scope.key": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "scope.key.special": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "scope.equals": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "table.header": "[dim]Unchanged[/dim]",
    "table.footer": "[dim]Unchanged[/dim]",
    "table.cell": "[dim]Unchanged[/dim]",
    "table.title": "[dim]Unchanged[/dim]",
    "table.caption": "[dim]Unchanged[/dim]",
    "traceback.error": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "traceback.border.syntax_error": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "traceback.border": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "traceback.text": "[dim]Unchanged[/dim]",
    "traceback.title": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "traceback.exc_type": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "traceback.exc_value": "[dim]Unchanged[/dim]",
    "traceback.offset": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bar.back": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bar.complete": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bar.finished": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "bar.pulse": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.description": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.filesize": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.filesize.total": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.download": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.elapsed": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.percentage": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.remaining": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.data.speed": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "progress.spinner": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "status.spinner": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "tree": "[dim]Unchanged[/dim]",
    "tree.line": "[dim]Unchanged[/dim]",
    "markdown.paragraph": "[dim]Unchanged[/dim]",
    "markdown.text": "[dim]Unchanged[/dim]",
    "markdown.em": "[dim]Unchanged[/dim]",
    "markdown.emph": "[dim]Unchanged[/dim]",
    "markdown.strong": "[dim]Unchanged[/dim]",
    "markdown.code": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.code_block": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.block_quote": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.list": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.item": "[dim]Unchanged[/dim]",
    "markdown.item.bullet": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.item.number": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.hr": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.h1.border": "[dim]Unchanged[/dim]",
    "markdown.h1": "[dim]Unchanged[/dim]",
    "markdown.h2": "[dim]Unchanged[/dim]",
    "markdown.h3": "[dim]Unchanged[/dim]",
    "markdown.h4": "[dim]Unchanged[/dim]",
    "markdown.h5": "[dim]Unchanged[/dim]",
    "markdown.h6": "[dim]Unchanged[/dim]",
    "markdown.h7": "[dim]Unchanged[/dim]",
    "markdown.link": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.link_url": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "markdown.s": "[dim]Unchanged[/dim]",
    "iso8601.date": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "iso8601.time": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "iso8601.timezone": ":paintbrush: [bold #ffffff]Color Corrected[/]",
    "rgb.red": ":star: [bold #e1b400]New[/] :star:",
    "rgb.green": ":star: [bold #e1b400]New[/] :star:",
    "rgb.blue": ":star: [bold #e1b400]New[/] :star:",
}


def get_default_styles():
    """Retrieve the defaults styles from GRADIENT_STYLES."""
    return GRADIENT_STYLES


def formatted_title() -> Text:
    """Create a vibrant title for the styles table.

    Returns:
        Text: the colorful title
    """
    letters = (
        Text("Gr", style="bold #ff0000"),
        Text("ad", style="bold #ff8800"),
        Text("ie", style="bold #ffff00"),
        Text("nt", style="bold #00ff00"),
        Text("Th", style="bold #00ffff"),
        Text("e", style="bold #0088ff"),
        Text("m", style="bold #5f00ff"),
        Text("e", style="bold #af00ff"),
    )
    return Text.assemble(*letters)


def styles_table() -> Table:
    """Generate a table to display all styles, examples of how to call each,
    and if each style is new, or updated from rich, or unchanged."""
    table = Table(
        title=formatted_title(),
        border_style="bold.white",
        caption="These styles are used when instantiating gradient.gradient.GradientTheme.",
        caption_style="dim",
        caption_justify="right",
    )
    table.add_column("[bold.cyan]Styles[/]", justify="right", vertical="middle")
    table.add_column(
        "[bold.cyan]Description[/]",
        justify="left",
        width=70,
        vertical="middle",
    )
    table.add_column("[bold.cyan]Updated[/]", justify="center", vertical="middle")

    for (
        style_name
    ) in GRADIENT_STYLES.keys():  # pylint: disable=consider-iterating-dictionary
        style = GRADIENT_STYLES.get(style_name)
        style_string = str(style)
        if "grey" in style_name:
            style_string = f"{style_string} [dim]*Supports alternate spelling[/dim]"
        if "dark_grey" in style_name or "dark_gray" in style_name:
            continue
        if "gray" in style_name:
            continue
        edited = EDITED_STYLES.get(style_name)
        table.add_row(Text(style_name, style=style), style_string, edited)
        if style_name == "none" or style_name == "reset":
            table.add_section()

    return table


def example() -> None:
    """Print the styles table to the console."""
    with Live(refresh_per_second=10):
        theme = Theme(GRADIENT_STYLES)
        console = Console(theme=theme)
        console.line(3)
        console.print(styles_table(), justify="center")
        console.line(3)


if __name__ == "__main__":
    example()
