"""Gradient logging module"""
from __future__ import annotations

# pylint: disable=E0401
import re
from datetime import datetime
from pathlib import Path

import loguru
from loguru import logger
from rich.abc import RichRenderable
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.table import Table
from rich.traceback import install as install_rich_traceback

from maxgradient.theme import GradientTheme

CWD = Path.cwd()
DEBUG_LOG = CWD / "logs" / "debug.log"
INFO_LOG = CWD / "logs" / "info.log"
FORMAT = "{time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}"

# console = GradientConsole(theme=GradientTheme(), highlighter=ReprHighlighter())
# install_rich_traceback(console=console)
RICH = logger.level("RICH", no=24, icon="🌈")


class LogConsole(Console):
    """Create a console to log with"""

    def __init__(self) -> None:
        super().__init__(theme=GradientTheme(), highlighter=ReprHighlighter())


def get_console() -> LogConsole:
    """Get console."""
    console = LogConsole()
    install_rich_traceback(console=console)
    return console


class Log:
    """Logging class"""

    def __init__(self) -> None:
        console = get_console()
        logger.remove()
        logger.configure(
            handlers=[
                {
                    "sink":DEBUG_LOG,
                    "level":"DEBUG",
                    "format":FORMAT,
                    "colorize":True,
                    "diagnose":True,
                    "backtrace":True
                },
                {
                    "sink":INFO_LOG,
                    "level":"INFO",
                    "format":FORMAT,
                    "colorize":True,
                    "diagnose":True,
                    "backtrace":True
                },
                {
                    "sink": self.rich_sink,
                    "level": "RICH",
                    "filter": self._rich_filter,
                    "colorize": True,
                    "format": "{message}",
                    "diagnose": True,
                    "catch": True,
                    "backtrace": True,
                },
                {
                    "sink": self.rich_sink,
                    "level": "WARNING",
                    "filter": self._rich_filter,
                    "colorize": True,
                    "format": "{message}",
                    "diagnose": True,
                    "catch": True,
                    "backtrace": True,
                },
                {
                    "sink": self.rich_sink,
                    "level": "ERROR",
                    "filter": self._rich_filter,
                    "colorize": True,
                    "format": "{message}",
                    "diagnose": True,
                    "catch": True,
                    "backtrace": True,
                },
                {
                    "sink": self.rich_sink,
                    "level": "CRITICAL",
                    "filter": self._rich_filter,
                    "colorize": True,
                    "format": "{message}",
                    "diagnose": True,
                    "catch": True,
                    "backtrace": True,
                }
            ]
        )
        console.clear()
        console.line(2)
        self.logger = logger.opt(depth=1, record=True)

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

    def rich(self, msg: RichRenderable) -> None:
        """Log to console.

        Args:
            msg (str): Message to log.
        """
        self.logger.log("RICH", msg)

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

    @staticmethod
    def rich_sink(message: loguru.Message) -> None:
        """Log to console.

        Args:
            message (loguru.Message): Message to log.
        """
        record = message.record
        level_name = record["level"].name
        level_icon = record["level"].icon
        if level_name == "DEBUG":
            color = "#5f00ff"
        if level_name == "INFO":
            color = "[#af00ff]"
        elif level_name == "RICH":
            color = "#ff00ff"
        elif level_name == "SUCCESS":
            color = "#00ff00"
        elif level_name == "WARNING":
            color = "#ff8800"
        elif level_name == "ERROR":
            color = "#ff0000"
        elif level_name == "CRITICAL":
            color = "#ffffff on #ff0000"
        level = f"[bold {color}]{level_icon} {level_name}[/]"
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
        file = f"[bold #ff00ff]{str(record['file'].name)}[/]"
        line = f"[bold #00ffff]Line {int(record['line'])}[/]"
        msg = f"[bold {color}]{str(record['message'])}[/]"

        headers = ["Time", "File", "Line", "Level", "Message"]
        log_table = Table(
            *headers,
            show_header=False,
            title_style="bold #ff8800",
            show_lines=True,
            show_edge=False,
            padding=(0, 1),
            # width=console.width * 0.8,
            expand=False,
        )
        log_table.add_row(time, file, line, level, msg)
        console = get_console()
        console.print(
            log_table,
            justify="left",
            width=int(console.width * 0.8),
        )

    @staticmethod
    def _rich_filter(record: loguru.Record) -> bool:
        """Filter out rich logs."""
        return record["level"].name == "RICH"

log = Log()

def test_logger():
    """Text log handlers"""

    log.info("Initialize DEBUG Log")
    log.debug("Initialize INFO Log")
    log.rich("Initialize RICH Log")
    log.warning("Initialize WARNING Log")
    log.error("Initialize ERROR Log")
    log.critical("Initialize CRITICAL Log")



if __name__ == "__main__":
    test_logger()
