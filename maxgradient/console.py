"""MaxConsole is a custom themed class inheriting from rich.console.Console."""
# pylint: disable=E0401, R0913, R0914
import os
from datetime import datetime
from typing import IO, Callable, List, Literal, Mapping, Optional, Tuple, Union

from rich._log_render import FormatTimeCallable
from rich.console import Console as RichConsole
from rich.console import ConsoleRenderable, RichCast
from rich.emoji import EmojiVariant
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.text import Span, Text
from rich.theme import Theme
from rich.traceback import install as install_traceback

# from maxgradient.color import Color
from maxgradient.gradient import Gradient
from maxgradient.theme import GradientTheme
from maxgradient.color import Color

RenderableType = ConsoleRenderable | RichCast | str
HighlighterType = Callable[[Union[str, "Text"]], "Text"]
JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


class Singleton(type):
    """A metaclass to create a single global MaxConsole instance."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Console(RichConsole, metaclass=Singleton):
    """A custom-themed high level interface for the GradientConsole class that \
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
            None for Max's default theme.
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
        file: Optional[IO[str]] = None,
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
        highlighter: Optional[HighlighterType] = ReprHighlighter(),
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
        """Return a gradient used by the console."""
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
            )
        )

    @staticmethod
    def get_title() -> Text:
        """Print out `MaxConsole` in a manual gradient"""
        return Gradient(
            "GradientConsole",
            colors=["#5f00ff", "#af00ff", "#ff00ff"],
            style="bold italic"
        )
    @classmethod
    def generate_example(cls) -> Text:
        """Generate an explanation of MaxConsole for demonstration."""
        rich = Gradient(
            "rich.console.Console",
            colors=["#0000ff", "#0044ff", "#1199ff", "#44bbff", "#66ffff"],
            style="bold italic"
        )
        text1 = Text(" is a custom themed terminal console class inheriting from")
        text2 = Text.from_markup(". It is a [i #66EE35] global singleton [/]class that can be \
imported and used anywhere in the project and used as a drop in replacement for "
        )
        text3 = Text(".")
        combine_explanation = Text.assemble(
            cls.get_title(),
            text1,
            rich,
            text2,
            rich,
            text3
        )
        return combine_explanation


if __name__ == "__main__":
    console = Console()
    example = console.generate_example()
    title = console.get_title()
    console.line(2)
    console.print(
        Panel(
            example,
            width=100,
        ),
        justify="center",
    )
    console.line()
