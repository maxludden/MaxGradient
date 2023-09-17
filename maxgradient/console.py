"""This module defines a custom themed class inheriting from rich.console.Console called MaxConsole.
It also defines a metaclass Singleton to create a single global MaxConsole instance.
The MaxConsole class is a high level interface for the Console class that inherits from rich.console.Console.
It is a singleton which removes the need to pass around a console object or use the `get_console` method.
"""

import os
from datetime import datetime
from pathlib import Path
from sys import stdout
from typing import IO, Callable, List, Literal, Mapping, Optional, Tuple, Union

from dotenv import load_dotenv
from rich._export_format import CONSOLE_SVG_FORMAT
from rich._log_render import FormatTimeCallable
from rich.align import AlignMethod
from rich.console import Console as RichConsole, RenderableType
from rich.console import (
    ConsoleOptions,
    ConsoleRenderable,
    Group as RichGroup,
    RenderResult,
    RichCast,
    
)
from rich.emoji import EmojiVariant
from rich.highlighter import ColorReprHighlighter
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.terminal_theme import TerminalTheme
from rich.text import Span, Text, TextType
from rich.theme import Theme
from rich.traceback import install as install_traceback

from maxgradient.color import Color
from maxgradient.gradient import Gradient
from maxgradient.highlighter import ColorReprHighlighter
from maxgradient.rule import GradientRule, Thickness
from maxgradient.theme import GradientTerminalTheme, GradientTheme

load_dotenv()

RenderableType = ConsoleRenderable | RichCast | str
HighlighterType = Callable[[Union[str, "Text"]], "Text"]
JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


class Singleton(type):
    """
    A metaclass to create a single global instance of a class.

    This metaclass ensures that only one instance of a class is created and
    provides a way to access that instance globally. To use this metaclass,
    simply inherit from it and define your class as you normally would.

    Example usage:

    class MyClass(metaclass=Singleton):
        pass

    my_instance = MyClass()
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class Console(RichConsole, metaclass=Singleton):
    """A custom-themed high level interface for the Console class that \
        inherits from rich.console.Console. This class is a singleton which removes \
        the need to pass around a console object or use the `get_console` method.

    Args:
        color_system (str, optional): The color system supported \
            by your terminal, either "standard", "256" or \
            "truecolor". Leave as "auto" to autodetect.
        force_terminal (Optional[bool], optional): Enable/disable terminal \
            control codes, or None to auto-detect terminal. Defaults to None.
        force_jupyter (Optional[bool], optional): Enable/disable Jupyter \
            rendering, or None to auto-detect Jupyter. Defaults to None.
        force_interactive (Optional[bool], optional): Enable/disable \
            interactive mode, or None to auto detect. Defaults to None.
        soft_wrap (Optional[bool], optional): Set soft wrap default on \
            print method. Defaults to False.
        theme (Theme, optional): An optional style theme object, or \
            None for the default theme: GradientTheme().
        stderr (bool, optional): Use stderr rather than stdout if \
            file is not specified. Defaults to False.
        file (IO, optional): A file object where the console \
            should write to. Defaults to stdout.
        quiet (bool, Optional): Boolean to suppress all output. \
            Defaults to False.
        width (int, optional): The width of the terminal. Leave \
            as default to auto-detect width.
        height (int, optional): The height of the terminal. Leave \
            as default to auto-detect height.
        style (StyleType, optional): Style to apply to all output, \
            or None for no style. Defaults to None.
        no_color (Optional[bool], optional): Enabled no color \
            mode, or None to auto detect. Defaults to None.
        tab_size (int, optional): Number of spaces used to replace \
            a tab character. Defaults to 4.
        record (bool, optional): Boolean to enable recording of \
            terminal output,
                required to call export_html, export_svg, and \
                    export_text. Defaults to False.
        markup (bool, optional): Boolean to enable console_markup. \
            Defaults to True.
        emoji (bool, optional): Enable emoji code. Defaults to True.
        emoji_variant (str, optional): Optional emoji variant, either \
            "text" or "emoji". Defaults to None.
        highlight (bool, optional): Enable automatic highlighting. \
            Defaults to True.
        log_time (bool, optional): Boolean to enable logging of time \
            by log methods. Defaults to True.
        log_path (bool, optional): Boolean to enable the logging \
            of the caller by log. Defaults to True.
        log_time_format (Union[str, TimeFormatterCallable], optional): \
            If log_time is enabled, either string for strftime or \
                callable that formats the time. Defaults to "[%X] ".
        highlighter (HighlighterType, optional): Default highlighter.
        legacy_windows (bool, optional): Enable legacy Windows \
            mode, or None to auto detect. Defaults to None.
        safe_box (bool, optional): Restrict box options that \
            don't render on legacy Windows.
        get_datetime (Callable[[], datetime], optional): Callable \
            that gets the current time as a datetime.datetime object (used by Console.log),
            or None for datetime.now.
        get_time (Callable[[], time], optional): Callable that \
            gets the current time in seconds, default uses time.monotonic.
            """

    theme: Theme = GradientTheme()
    _environ: Mapping[str, str] = os.environ

    def __init__(
        self,
        *,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = "auto",
        force_terminal: Optional[bool] = None,
        force_jupyter: Optional[bool] = None,
        force_interactive: Optional[bool] = None,
        soft_wrap: bool = False,
        theme: Optional[Theme] = GradientTheme(),
        stderr: bool = False,
        file: Optional[IO[str]] = stdout,
        quiet: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        style: Optional[StyleType] = None,
        no_color: Optional[bool] = None,
        tab_size: int = 4,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        emoji_variant: Optional[EmojiVariant] = None,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: Union[str, FormatTimeCallable] = "[%X]",
        highlighter: Optional[HighlighterType] = ColorReprHighlighter(),
        legacy_windows: Optional[bool] = None,
        safe_box: bool = True,
        get_datetime: Optional[Callable[[], datetime]] = None,
        get_time: Optional[Callable[[], float]] = None,
        traceback: bool = True,
        _environ: Optional[Mapping[str, str]] = None,
    ):
        super().__init__(
            color_system=color_system,
            force_terminal=force_terminal,
            force_jupyter=force_jupyter,
            force_interactive=force_interactive,
            soft_wrap=soft_wrap,
            theme=theme,
            stderr=stderr,
            file=file,
            quiet=quiet,
            width=width,
            height=height,
            style=style,
            no_color=no_color,
            tab_size=tab_size,
            record=record,
            markup=markup,
            emoji=emoji,
            emoji_variant=emoji_variant,
            highlight=highlight,
            log_time=log_time,
            log_path=log_path,
            log_time_format=log_time_format,
            highlighter=highlighter,
            legacy_windows=legacy_windows,
            safe_box=safe_box,
            get_datetime=get_datetime,
            get_time=get_time,
            _environ=_environ,
        )
        if traceback:
            install_traceback(console=self)

    def __repr__(self) -> str:
        return f"<GradientConsole width={self.width} {self._color_system!s}>"

    def gradient(
        self,
        text: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = Style.null(),
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,
    ) -> None:
        """Text with gradient color / style.

        Args:
            text(`text): The text to print. Defaults to `""`.\n
            colors(`List[Optional[Color|Tuple|str|int]]`): A list of colors to use \
                for the gradient. Defaults to None.\n
            rainbow(`bool`): Whether to print the gradient text in rainbow colors\
                across the spectrum. Defaults to False.\n
            invert(`bool`): Reverse the color gradient. Defaults to False.\n
            hues(`int`): The number of colors in the gradient. Defaults to `3`.\n
            color_sample(`bool`): Replace text characters with `"█" `. Defaults\
                to False.\n
            style(`StyleType`) The style of the gradient text. Defaults to None.\n
            justify(`Optional[JustifyMethod]`): Justify method: "left", "center",\
                "full", "right". Defaults to None.\n
            overflow(`Optional[OverflowMethod]`):  Overflow method: "crop", "fold", \
                "ellipsis". Defaults to None.\n
            end (str, optional): Character to end text with. Defaults to "\\\\n".\n
            no_wrap (bool, optional): Disable text wrapping, or None for default.\
                Defaults to None.\n
            tab_size (int): Number of spaces per tab, or `None` to use\
                `console.tab_size`. Defaults to 8.\n
            spans (List[Span], optional). A list of predefined style spans.\
                Defaults to None.\n

        """
        self.print(
            Gradient(
                text=text,
                colors=colors,
                rainbow=rainbow,
                invert=invert,
                hues=hues,
                color_sample=color_sample,
                style=style,
                justify=justify,
                overflow=overflow,
                no_wrap=no_wrap,
                end=end,
                tab_size=tab_size,
                spans=spans,
            ),
            justify=justify,
        )

    def gradient_rule(
        self,
        title: TextType = "",
        *,
        gradient: bool = True,
        thickness: Thickness = "medium",
        end: str = "\n",
        align: AlignMethod = "center",
    ) -> None:
        """Draw an optionally gradient line with optional centered title.

        Args:
            title (str, optional): Text to render over the rule. Defaults to "".
            gradient (bool, optional): Whether to use a gradient for the rule. Defaults to True.
            thickness (Thickness, optional): Thickness of the rule. Defaults to "medium".
            align (str, optional): How to align the title, one of "left", "center", or "right". Defaults to "center".
            justify (str, optional): How to justify the title, one of "left", "center", or "right". Defaults to None.
        """
        rule = GradientRule(
            title=title, gradient=gradient, thickness=thickness, end=end, align=align
        )
        self.print(rule)

    def save_svg(
        self,
        path: str,
        *,
        title: str = "MaxGradient",
        theme: Optional[TerminalTheme] = GradientTerminalTheme(),
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    ) -> None:
        """Generate an SVG file from the console contents (requires record=True in Console constructor).

        Args:
            path (str): The path to write the SVG to.
            title (str, optional): The title of the tab in the output image
            theme (TerminalTheme, optional): The ``TerminalTheme`` object to use to style the terminal
            clear (bool, optional): Clear record buffer after exporting. Defaults to ``True``
            code_format (str, optional): Format string used to generate the SVG. Rich will inject a number of variables
                into the string in order to form the final SVG output. The default template used and the variables
                injected by Rich can be found by inspecting the ``console.CONSOLE_SVG_FORMAT`` variable.
            font_aspect_ratio (float, optional): The width to height ratio of the font used in the ``code_format``
                string. Defaults to 0.61, which is the width to height ratio of Fira Code (the default font).
                If you aren't specifying a different font inside ``code_format``, you probably don't need this.
            unique_id (str, optional): unique id that is used as the prefix for various elements (CSS styles, node
                ids). If not set, this defaults to a computed value based on the recorded content.
        """
        svg = self.export_svg(
            title=title,
            theme=theme,
            clear=clear,
            code_format=code_format,
            font_aspect_ratio=font_aspect_ratio,
            unique_id=unique_id,
        )
        with open(path, "wt", encoding="utf-8") as write_file:
            write_file.write(svg)

    def save_max_svg(
        self,
        path: str | Path,
        *,
        title: str = "MaxGradient",
        theme: Optional[TerminalTheme] = GradientTerminalTheme(),
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    ) -> None:
        """A shortcut to save an SVG file to the Images directory.

        Args:
            path (str | Path): The path to save the SVG file to.
            title (str, optional): The title of the exported SVG file. Defaults to "MaxGradient".
            theme (Optional[TerminalTheme], optional): The theme to use when creating the \
                SVG file. Defaults to GradientTerminalTheme().
            clear (bool, optional): Whether to clear the console before generating the SVG file. Defaults to True.
            code_format (str, optional): The format to use on the exported code. Defaults to CONSOLE_SVG_FORMAT.
            font_aspect_ratio (float, optional): The aspect ration of the exported font. Defaults to 0.61.
            unique_id (Optional[str], optional): The unique ID of the exported SVG file. Defaults to None.
        """
        if not path:
            if "MaxGradient.svg" in (Path.cwd() / "Images").iterdir():
                path = (
                    Path.cwd()
                    / "docs"
                    / "img"
                    / f"MaxGradient_{datetime.now().strftime('%Y%m%d%H%M%S')}.svg"
                )
        if title == "MaxGradient":
            title = path.stem

        svg = self.export_svg(
            title=title,
            theme=theme,
            clear=clear,
            code_format=code_format,
            font_aspect_ratio=font_aspect_ratio,
            unique_id=unique_id,
        )
        with open(path, "wt", encoding="utf-8") as write_file:
            write_file.write(svg)

    @staticmethod
    def get_title() -> Text:
        """Print out `MaxConsole` in a manual gradient"""
        return Gradient(
            "GradientConsole",
            colors=["#5f00ff", "#af00ff", "#ff00ff"],
            style="bold italic",
        )

    @classmethod
    def generate_example(cls) -> Text:
        """Generate an explanation of MaxConsole for demonstration."""
        rich = Gradient(
            "rich.console.Console",
            colors=["#0000ff", "#0044ff", "#1199ff", "#44bbff", "#66ffff"],
            style="bold italic",
        )
        text1 = Text(" is a custom themed terminal console class inheriting from")
        text2 = Text.from_markup(
            ". It is a[i #66EE35] global singleton[/] class that can be \
imported and used anywhere in the project and used as a drop in replacement for "
        )
        text3 = Text(".")
        combine_explanation = Text.assemble(
            cls.get_title(), text1, rich, text2, rich, text3
        )
        return combine_explanation


if __name__ == "__main__":
    console = Console()
    example = console.generate_example()
    title = console.get_title()
    console.line()
    console.gradient_rule("GradientConsole", thickness="medium", align="center")
    console.line()
    console.print(
        Panel(
            example,
            width=100,
        ),
        justify="center",
    )
    console.line()
