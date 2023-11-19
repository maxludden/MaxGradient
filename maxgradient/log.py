# ruff: noqa: F401
from os import getenv
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from loguru import logger, Record, Message
from rich.console import (
    Console,
    ConsoleOptions,
    Group,
    JustifyMethod,
    OverflowMethod
)
from rich.text import Text
from maxgradient.gradient import Gradient
CWD = Path.cwd()
load_dotenv(CWD / ".env")
LOG_DIR = CWD / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
console = Console()

loggers = logger.configure(
    handlers=[
        dict( # 1 - debug.log
            sink=LOG_DIR / "debug.log",
            level="DEBUG",
            format='{time:hh:mm:ss:SSS A} | {file.name: ^13} | \
                Line {line: ^5} | {level: ^8} ﰲ  {message}',
            backtrace=True,
            diagnose=True,
            colorize=True
        ),
        dict( # 2 - info.log
            sink=LOG_DIR / "info.log",
            level="INFO",
            format='{time:hh:mm:ss:SSS A} | {file.name: ^13} | \
                Line {line: ^5} | {level: ^8} ﰲ  {message}',
            backtrace=True,
            diagnose=True,
            coolorize=True
        ),
        dict( # 3 - warning.log
            sink=LOG_DIR / "warning.log",
            level="WARNING",
            format='{time:hh:mm:ss:SSS A} | {file.name: ^13} | \
                Line {line: ^5} | {level: ^8} ﰲ  {message}',
            backtrace=True,
            diagnose=True,
            colorize=True
        ),
        dict( # 4 - error.log
            sink=LOG_DIR / "error.log",
            level="ERROR",
            format='{time:hh:mm:ss:SSS A} | {file.name: ^13} | \
                Line {line: ^5} | {level: ^8} ﰲ  {message}',
            backtrace=True,
            diagnose=True,
            colorize=True
        ),
        dict( # 5 - critical.log
            sink=LOG_DIR / "critical.log",
            level="CRITICAL",
            format='{time:hh:mm:ss:SSS A} | {file.name: ^13} | \
                Line {line: ^5} | {level: ^8} ﰲ  {message}',
            backtrace=True,
            diagnose=True,
            colorize=True
        ),
        dict( # 6 - console
            sink=lambda msg: console.log(
                Gradient(
                    msg,
                    colors=[
                        '#afff00',
                        '#8ddd00',
                        '#6ccc00',
                        '#00ff00'
                    ]
                ),
                log_locals=True
            ),
            level="DEBUG",
            format='{message}',
            backtrace=True,
            diagnose=True,
            colorize=True
        )
    ]
)
