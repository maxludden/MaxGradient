"""Gradient logging module"""
# pylint: disable=E0401,W0611,C0103
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Self, Any

import loguru
from loguru import logger
from rich.abc import RichRenderable
from rich.console import Console as RichConsole
from rich.highlighter import ReprHighlighter, RegexHighlighter
from rich.table import Table
from rich.traceback import install as install_rich_traceback

from maxgradient.theme import GradientTheme

CWD = Path.cwd()
DEBUG_LOG = CWD / "logs" / "debug.log"
INFO_LOG = CWD / "logs" / "info.log"
FORMAT = "{time:hh:mm:ss:SSS A} | {file.name: ^13} |\
    Line {line: ^5} | {level: ^8} ﰲ  {message}"


class Singleton(type):
    """A metaclass to create a single global MaxConsole instance."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LogHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "log."
    highlights = [
        r"(?P<keyword>.+(?=\d+)) ?(?P<index>\d+)?(?P<separator>:) ",
        r"(?P<keyword>[A-Za-z_]+)(?P<separator>:) "
    ]


class LogConsole(RichConsole, metaclass=Singleton):
    """A Console to log to. Inherits from rich.console.Console.\
        This class is a singleton which removes the need to pass\
        around a console object or use the `get_console` method."""

    def __init__(self) -> None:
        super().__init__(theme=GradientTheme(), highlighter=LogHighlighter())
        install_rich_traceback(console=self)


console_ = LogConsole()


class Log:
    """Logging class of MaxGradient. It utilizes the loguru library as well as rich.\
        It can be called and used without any arguments, but it can also be\
        instantiated with a rich_level argument. This will set the level of\
        logs that are printed to the console. The default is "SUCCESS", which\
        will print all logs of level "SUCCESS" or higher. The levels are as\
        follows: \n\t- "DEBUG",\n\t- "INFO",\n\t-  "SUCCESS",\n\t-  "WARNING",\
        \n\t- "ERROR",\n\t- "CRITICAL".\n\n\tThe rich_level argument can be\
        set to any of these levels, and all logs of that level or higher will\
        be printed to the console.

        Args:
            rich_level (str, optional): The level of logs to print to the console.\
                Defaults to "SUCCESS".
            console (Console, optional): The console to use for printing. Defaults\
                to _console, which is a console with the GradientTheme and a\
                ReprHighlighter.
    """

    rich_level: str

    def __init__(
        self, console: LogConsole = console_, rich_level: str = "SUCCESS"
    ) -> None:
        self.rich_level = rich_level
        self.console: LogConsole = console
        logger.remove()
        logger.configure(
            handlers=[
                {
                    "sink": DEBUG_LOG,
                    "level": "DEBUG",
                    "format": FORMAT,
                    "colorize": True,
                    "diagnose": True,
                    "backtrace": True,
                },
                {
                    "sink": INFO_LOG,
                    "level": "INFO",
                    "format": FORMAT,
                    "colorize": True,
                    "diagnose": True,
                    "backtrace": True,
                },
                {
                    "sink": self.rich_sink,
                    "level": rich_level,
                    "filter": self.rich_filter,
                    "colorize": True,
                    "format": "{message}",
                    "diagnose": True,
                    "catch": True,
                    "backtrace": True,
                },
            ]
        )
        self.logger = logger.opt(depth=1, record=True)

    def __call__(self, *args, **kwargs) -> Self:
        return self

    @staticmethod
    def _get_level_color(record: loguru.Record) -> str:
        """Generate the color for the record's level."""
        level_name = record["level"].name
        if level_name == "DEBUG":
            return "#5f00ff"
        if level_name == "INFO":
            return "#af00ff"
        if level_name == "SUCCESS":
            return "#00ff00"
        if level_name == "WARNING":
            return "#ff8800"
        if level_name == "ERROR":
            return "#ff0000"
        if level_name == "CRITICAL":
            return "#ffffff on #ff0000"
        error_msg = "Unable to get color for level: "
        raise ValueError(f"{error_msg}{level_name}")

    @staticmethod
    def _get_icon(record: loguru.Record) -> str:
        """Generate the icon for the record's level."""
        level_name = record["level"].name
        if level_name == "DEBUG":
            return "ℹ"
        if level_name == "INFO":
            return "ℹ"
        if level_name == "SUCCESS":
            return "✔"
        if level_name == "WARNING":
            return "⚠️"
        if level_name == "ERROR":
            return "✘"
        if level_name == "CRITICAL":
            return "☠️"
        error_msg = "Unable to get icon for level: "
        raise ValueError(f"{error_msg}{level_name}")

    def _get_rich_level_no(self) -> int:
        """Filter logs to print to the console."""
        rich_level = self.rich_level
        if rich_level == "DEBUG":
            return 10
        if rich_level == "INFO":
            return 20
        if rich_level == "SUCCESS":
            return 25
        if rich_level == "WARNING":
            return 30
        if rich_level == "ERROR":
            return 40
        if rich_level == "CRITICAL":
            return 50
        raise ValueError(f"Invalid log.rich_level: {rich_level}")

    @classmethod
    def _get_level_markup(cls, record: loguru.Record) -> str:
        """Return the logging level name formatted with a color and icon."""
        _color = cls._get_level_color(record)
        _name: str = f"[{_color}]{record['level'].name: <11}[/]"
        _icon: str = f"[{_color}]{cls._get_icon(record)}[/]"

        _combo: str = f" {_icon} {_name: <9}"
        _name_length = len(_combo)
        if _name_length < 12:
            _combo = f"{_combo: ^12}"
        level_name = _combo

        markup = f"[bold {_color}]{level_name}[/]"
        return f"{markup: ^10}"

    @staticmethod
    def _get_time_markup(record: loguru.Record) -> str:
        """Format the time of the log time with color."""
        log_time: datetime = record["time"]
        time_str = f"[bold #00ff00]{log_time.strftime('%H:%M:%S:%f %p')}[/]"
        num_match = re.match(r"(\d+)]", time_str)
        if num_match:
            for _, group in enumerate(num_match.groups()):
                if len(group) > 2:
                    time_str = time_str.replace(group, f"[bold #008300]{group[0:2]}[/]")
                time_str = time_str.replace(group, f"[bold #008300]{group}[/]")
        time_str = time_str.replace(":", "[bold #ddffdd]:[/]")
        time = time_str.replace("PM", "[bold dim #ddffdd]PM[/]")
        return time

    @staticmethod
    def _get_file_color(record: loguru.Record) -> str:
        """Return the color given the record's file."""
        _file = record["file"].name
        file_colors = {
            "logger.py": "#ffccff",
            "_gradient_substring.py": "#ffbbff",
            "_gradient.py": "#ff99ff",
            "_mode.py": "#ff55ff",
            "_x11.py": "#ff00ff",
            "_rich.py": "#af00ff",
            "color_list.py": "#5f00ff",
            "color.py": "#0000ff",
            "console.py": "#0044ff",
            "default_styles.py": "#0088ff",
            "gradient.py": "#00ffff",
            "log.py": "#00ff88",
            "theme.py": "#00ff00",
            "panel.py": "#66ff00",
        }
        if _file in file_colors.keys():  # pylint: disable=C0201
            return file_colors[_file]
        else:
            return "#ffff00"

    def _get_file(self, record: loguru.Record) -> str:
        """Return the file the record was logged from with color."""
        file: str = record["file"].name
        color: str = self._get_file_color(record)
        return f"[bold {color}]{file}[/]"

    @staticmethod
    def _get_line(record: loguru.Record) -> str:
        """Return the line the record was logged from with color."""
        line: int = record["line"]
        color = "#7FD6E8"
        line = f"[bold {color}]Line {line}[/]"
        return line

    @classmethod
    def _get_msg(cls, record: loguru.Record) -> str:
        """Return the message of the record with color."""
        level_color = cls._get_level_color(record)
        msg: str = record["message"]
        return f"[bold {level_color}]{msg}[/]"

    @staticmethod
    def _generate_log_table() -> Table:
        """Generate the log table."""
        headers = ["Time", "File", "Line", "Level", "Message"]
        return Table(
            *headers,
            show_header=False,
            title_style="bold #ff8800",
            show_lines=True,
            show_edge=False,
            padding=(0, 1),
            expand=False,
        )

    def rich_sink(self, message: loguru.Message, console: LogConsole = console_) -> None:
        """Log to console.

        Args:
            message (loguru.Message): Message to log.
            console (rich.console.Console, optional): Console to log to.
        """
        # format the components of the log message
        record = message.record
        level = self._get_level_markup(record)
        time: str = self._get_time_markup(record)
        file: str = self._get_file(record)
        line: str = self._get_line(record)
        msg: str = self._get_msg(record)

        # generate the log table
        log_table = self._generate_log_table()
        log_table.add_row(time, file, line, level, msg)

        # print the log table
        console.print(
            log_table,
            justify="left",
            # width=int(console.width * 0.8),
        )

    def rich_filter(self, record: loguru.Record) -> bool:
        """Filter logs to print to the console."""
        return record["level"].no >= self._get_rich_level_no()

    def debug(self, msg: str) -> None:
        """Log to debug.log

        Args:
            msg (str): Message to log.
        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log to info.log.

        Args:
            msg (str): Message to log.
        """
        self.logger.info(msg)

    def success(self, msg: str) -> None:
        """Log to success.log.

        Args:
            msg (str): Message to log.
        """
        self.logger.success(msg)

    def key(self, key:str, value: Any) -> None:
        """Log to debug.log

        Args:
            msg (str): Message to log.
        """
        key_markup = f"[bold #E3EC84]{key}[/]"
        sep = "[bold #ffffff]: [/]"
        value_markup = f"[bold #00ff00]{value}[/]"
        msg = f"{key_markup}{sep}{value_markup}"
        self.logger.debug(msg)

    def key_index(self, key:str, index: int, value: Any) -> None:
        """Log to debug.log

        Args:
            msg (str): Message to log.
        """
        key_markup = f"[bold ##E3EC84]{key}[/]"
        index_markup = f"[bold #7FD6E8] {index}[/]"
        sep = "[bold #ffffff]: [/]"
        value_markup = f"[bold #00ff00]{value}[/]"
        msg = f"{key_markup}{index_markup}{sep}{value_markup}"
        self.logger.debug(msg)

    def warning(self, msg: RichRenderable) -> None:
        """Log to console.

        Args:
            msg (str): Message to log.
        """
        self.logger.log("WARNING", msg)

    def error(self, msg: RichRenderable) -> None:
        """Log to console.

        Args:
            msg (str): Message to log.
        """
        self.logger.log("ERROR", msg)

    def critical(self, msg: RichRenderable) -> None:
        """Log to console.

        Args:
            msg (str): Message to log.
        """
        self.logger.log("CRITICAL", msg)


log = Log(console_)


def test_logger():
    """Text log handlers"""
    console_.line(2)
    text_log = Log("DEBUG")
    text_log.info("Initialize DEBUG Log")
    text_log.debug("Initialize INFO Log")
    text_log.success("Initialize SUCCESS Log")
    text_log.warning("Initialize WARNING Log")
    text_log.error("Initialize ERROR Log")
    text_log.critical("Initialize CRITICAL Log")


if __name__ == "__main__":
    test_logger()
