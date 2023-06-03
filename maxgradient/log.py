from __future__ import annotations

import re
from datetime import datetime
from functools import partial, wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import loguru
from loguru import logger
from rich import inspect
from rich.abc import RichRenderable
from rich.console import Console, ConsoleOptions, RenderResult
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback

from maxgradient.theme import GradientTheme

CWD = Path.cwd()
DEBUG_LOG = CWD / "logs" / "debug.log"
INFO_LOG = CWD / "logs" / "info.log"
FORMAT = "{time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}"

console = Console(theme=GradientTheme(), highlighter=ReprHighlighter())
install_rich_traceback(console=console)
RICH = logger.level("RICH", no=24, icon="🌈")

def log_func(*, entry:bool=True, exit:bool=True, level="RICH"):
    def wrapper(func):
        name = func.__name__
        @wraps(func)
        def wrapped(*args, **kwargs):
            log_ = logger.opt(depth=1)
            if entry:
                log_.log(level, f"Entering `{name}` (args={args}, kwargs={kwargs}))")
            result = func(*args, **kwargs)
            if exit:
                log_.log(level, f"Exiting `{name}` (result={result})")
            return result
        return wrapped
    return wrapper

class Log:
    def __init__(self, console: Console) -> None:
        logger.remove()
        logger.configure(
            handlers=[
                dict(
                    sink=DEBUG_LOG,
                    level="DEBUG",
                    format=FORMAT,
                    colorize=True,
                ),
                dict(
                    sink=INFO_LOG,
                    level="INFO",
                    format=FORMAT,
                    colorize=True,
                ),
                dict(
                    # sink=lambda msg: console.log(Message(msg), log_locals=True, highlight=True),
                    sink=self.rich_sink,
                    level="RICH",
                    filter=self._rich_filter,
                    colorize=True,
                    format="{message}",
                    diagnose=True,
                    catch=True,
                    backtrace=True,
                ),
                dict(
                    sink=self.rich_sink,
                    level="WARNING",
                    filter=self._rich_filter,
                    colorize=True,
                    format="{message}",
                    diagnose=True,
                    catch=True,
                    backtrace=True,
                )
            ]
        )
        console.clear()
        console.line(2)
        self.logger = logger.opt(depth=1, record=True)

    # def __getattr__(self, name: str) -> Any:
    #     return getattr(self.logger, name)

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

    def log(self, msg: RichRenderable) -> None:
        """Log to console.

        Args:
            msg (str): Message to log.
        """
        self.logger.log("RICH", msg)

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
            for index, group in enumerate(num_match.groups()):
                if len(group) > 2:
                    time_str = time_str.replace(group, f"[bold #008300]{group[0:2]}[/]")
                time_str = time_str.replace(group, f"[bold #008300]{group}[/]")
        time_str = time_str.replace(":", "[bold #ddffdd]:[/]")
        time = time_str.replace("PM", "[bold dim #ddffdd]PM[/]")
        file = f"[bold #ff00ff]{str(record['file'].name)}[/]"
        line = f"[bold #00ffff]Line {int(record['line'])}[/]"
        msg = str(record["message"])

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
        # for k, v in record.items():
        #     log_table.add_row(k.capitalize(), v)
        console.print(
            log_table,
            justify="left",
            width=int(console.width * 0.8),
        )

    @staticmethod
    def _rich_filter(record: loguru.Record) -> bool:
        """Filter out rich logs."""
        return record["level"].name == "RICH"


    def func(self, *, entry=True, exit=True, level="DEBUG"):

        def wrapper(func):
            name = func.__name__

            @wraps(func)
            def wrapped(*args, **kwargs):
                decorator_logger = self.logger.opt(depth=1)
                if entry:
                    decorator_logger.log(level, f"Entering '{name}' (args={args}, kwargs={kwargs}")
                result = func(*args, **kwargs)
                if exit:
                    decorator_logger.log(level, f"Exiting '{name}' (result={result})")
                return result

            return wrapped

        return wrapper

log = Log(console)

@log.func()
def test_logger():
    log = Log(console)
    log.info("Initialize DEBUG Log")
    log.debug("Initialize INFO Log")
    log.log("Initialize RICH Log")

if __name__ == "__main__":
    test_logger()
