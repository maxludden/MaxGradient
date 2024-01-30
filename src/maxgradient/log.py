from __future__ import annotations

# ruff: noqa: F401
from os import getenv
from pathlib import Path
from typing import Any, Optional

# from loguru import logger
import loguru
from dotenv import load_dotenv
from rich.console import Console, ConsoleOptions, Group, JustifyMethod, OverflowMethod
from rich.style import Style
from rich.text import Text, TextType

logger = loguru.logger


def level_color(msg: loguru.Message) -> Style:
    """Generate a color for the logging levels.

    Args:
        level (str|int): The logging level. Can be a string or an integer.

    Returns:
        Style: A style for the logging level.

    """
    record = msg.record
    level = record["level"].name
    assert level, "No level provided."
    if isinstance(level, str):
        match level.lower():
            case "trace":
                return Style(color="#ffd4ff", bold=False, italic=False, dim=True)
            case "debug":
                return Style(color="#ff00ff", bold=False, italic=True)
            case "info":
                return Style(color="#5f00ff", bold=False, italic=False)
            case "success":
                return Style(color="#00ff00", bold=True, italic=False)
            case "warning":
                return Style(color="#ffbf00", bold=True, italic=True)
            case "error":
                return Style(color="#000000", bgcolor="#d37100", bold=True, italic=True)
            case "critical":
                return Style(
                    color="#ffeeee",
                    bgcolor="#880000",
                    bold=True,
                    italic=True,
                    blink=True,
                )
            case _:
                raise ValueError(
                    f"Level parsed incorrectly. String must be a logging \
level (`TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITIAL`), you entered: {level}"
                )
    elif isinstance(level, int):
        assert level > 0, "Level must be greater than 0."
        if level <= 5:  # trace
            return Style(color="#ffd4ff", bold=False, italic=False, dim=True)
        elif level <= 10:  # debug
            return Style(color="#ff00ff", bold=False, italic=True)
        elif level <= 20:  # info
            return Style(color="#5f00ff", bold=False, italic=False)
        elif level <= 25:  # success
            return Style(color="#00ff00", bold=True, italic=False)
        elif level <= 30:  # warning
            return Style(color="#ffbf00", bold=True, italic=True)
        elif level <= 40:  # error
            return Style(color="#000000", bgcolor="#d37100", bold=True, italic=True)
        elif level <= 50:  # critical
            return Style(
                color="#ffeeee", bgcolor="#880000", bold=True, italic=True, blink=True
            )
        else:
            raise ValueError(
                f"Level parsed incorrectly. Invalid integer: integer \
level must be a valid logging level between 0 annd 50. You entered:{level}"
            )
    else:
        raise TypeError(
            f"Level parsed incorrectly. Level must be a string or an \
integer, you entered: {level}"
        )


def logging_prompt(msg: loguru.Message) -> str:
    """Generate a prompt for the logging levels."""
    record: loguru.Record = msg.record
    level = record["level"].name
    return level


CWD = Path.cwd()
load_dotenv(CWD / ".env")
LOG_DIR = CWD / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
if len(list(LOG_DIR.iterdir())) > 5:
    log_levels: list[str] = [
        "debug.log",
        "info.log",
        "warning.log",
        "error.log",
        "critical.log",
    ]
    for level in log_levels:
        path: Path = LOG_DIR / level
        if not path.exists():
            with open(path, "w", encoding="utf-8") as outfile:
                outfile.write("")


console = Console()
FORMAT: str = """{time:hh:mm:ss:SSS A} | {file.name: ^13} |  \
    Line {line: ^5} | {level: ^8} ﰲ  {message}"""


def rich_filter(record) -> bool:
    """Filter log records to only those that have a rich message."""
    log_to_console: int = int(record["extra"]["log_to_console"])
    level = record["level"].no
    return level >= log_to_console


logger.remove()
loggers = logger.configure(
    handlers=[
        dict(  # 1 - debug.log
            sink=LOG_DIR / "debug.log",
            level="DEBUG",
            format=FORMAT,
            backtrace=True,
            diagnose=True,
            colorize=True,
        ),
        dict(  # 2 - info.log
            sink=LOG_DIR / "info.log",
            level="INFO",
            format=FORMAT,
            backtrace=True,
            diagnose=True,
            colorize=True,
        ),
        dict(  # 3 - warning.log
            sink=LOG_DIR / "warning.log",
            level="WARNING",
            format=FORMAT,
            backtrace=True,
            diagnose=True,
            colorize=True,
        ),
        dict(  # 4 - error.log
            sink=LOG_DIR / "error.log",
            level="ERROR",
            format=FORMAT,
            backtrace=True,
            diagnose=True,
            colorize=True,
        ),
        dict(  # 5 - critical.log
            sink=LOG_DIR / "critical.log",
            level="CRITICAL",
            format=FORMAT,
            backtrace=True,
            diagnose=True,
            colorize=True,
        ),
        dict(  # 6 - console
            sink=lambda msg: console.print(
                Text(
                    f"{logging_prompt(msg)}: {msg}",
                    justify="left",
                    overflow="fold",
                    style=level_color(msg),
                ),
                highlight=True,
            ),
            format="{message}",
            backtrace=True,
            diagnose=True,
            colorize=True,
            level="SUCCESS",
        ),
    ]
)
log = logger.bind(name="maxgraient")
# log.disable("maxgradient/")

if __name__ == "__main__":
    log.debug("Debug message.")
    log.info("Info message.")
    log.warning("Warning message.")
    log.error("Error message.")
    log.critical("Critical message.")
    log.success("Success message.")
    log.trace("Trace message.")
    log.opt(lazy=True).debug("Lazy message.")
    log.opt(lazy=True).info("Lazy message.")
    log.opt(lazy=True).warning("Lazy message.")
    log.opt(lazy=True).error("Lazy message.")
    log.opt(lazy=True).critical("Lazy message.")
    log.opt(lazy=True).success("Lazy message.")
    log.opt(lazy=True).trace("Lazy message.")
