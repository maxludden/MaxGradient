import io
import sys
import time
import typing
import warnings
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from datetime import timedelta
from io import RawIOBase, UnsupportedOperation
from math import ceil
from mmap import mmap
from operator import length_hint
from os import PathLike, stat
from threading import Event, RLock, Thread
from types import TracebackType
from typing import (
    Any,
    BinaryIO,
    Callable,
    ContextManager,
    Deque,
    Dict,
    Generic,
    Iterable,
    List,
    NamedTuple,
    NewType,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from rich.columns import Columns
from rich.console import Console as RichConsole
from rich.live import Live
from rich.progress import BarColumn, GetTimeCallable, MofNCompleteColumn
from rich.progress import Progress as RichProgress
from rich.progress import (
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.style import Style, StyleType
from rich.table import Column
from rich.text import Text

from maxgradient import Console, Gradient, Log

console = Console()
log = Log()


class Progress(RichProgress):
    """Renders an auto-updating progress bar(s).

    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (Optional[float], optional): Number of times per second to refresh the progress information or None to use default (10). Defaults to None.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        redirect_stdout: (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr: (bool, optional): Enable redirection of stderr. Defaults to True.
        get_time: (Callable, optional): A callable that gets the current time, or None to use Console.get_time. Defaults to None.
        disable (bool, optional): Disable progress display. Defaults to False
        expand (bool, optional): Expand tasks table to fit width. Defaults to False.
    """

    columns: Tuple[ProgressColumn, ...] = (
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(
            spinner_name="point",
            style="#ffff00",
            finished_text=Text("✓", style="#00ff00"),
            table_column=Column(),
        ),
        BarColumn(
            bar_width=None,  # Full width progress bar
            style=Style(color="#249df1"),  # While in-progress
            complete_style=Style(color="#00ff00"),  # Done
            finished_style=Style(color="#333333"),  # After completion
            table_column=Column(ratio=3),
        ),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )

    def __init__(
        self,
        *columns: Union[str, ProgressColumn],
        console: Optional[Console | RichConsole] = Console(),
        auto_refresh: bool = True,
        refresh_per_second: float = 10,
        speed_estimate_period: float = 30.0,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        get_time: Optional[GetTimeCallable] = None,
        disable: bool = False,
        expand: bool = False,
    ) -> None:
        """Initialize a Progress instance."""
        self.columns = self.columns or self.get_default_columns()
        super().__init__(
            columns or self.get_default_columns(),  # type: ignore
            console=console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            transient=transient,
            redirect_stdout=redirect_stdout,
            redirect_stderr=redirect_stderr,
            get_time=get_time,
            disable=disable,
            expand=expand,
        )

    @classmethod
    def get_default_columns(cls) -> Tuple[ProgressColumn, ...]:
        """Get the default columns used for a new Progress instance:
           - a text column for the description (TextColumn)
           - the bar itself (BarColumn)
           - a text column showing completion percentage (TextColumn)
           - an estimated-time-remaining column (TimeRemainingColumn)
        If the Progress instance is created without passing a columns argument,
        the default columns defined here will be used.

        You can also create a Progress instance using custom columns before
        and/or after the defaults, as in this example:

            progress = Progress(
                SpinnerColumn(),
                *Progress.default_columns(),
                "Elapsed:",
                TimeElapsedColumn(),
            )

        This code shows the creation of a Progress display, containing
        a spinner to the left, the default columns, and a labeled elapsed
        time column.
        """
        return (
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(
                spinner_name="point",
                style="#ffff00",
                finished_text=Text("✓", style="#00ff00"),
                table_column=Column(),
            ),
            BarColumn(
                bar_width=None,  # Full width progress bar
                style=Style(color="#249df1"),  # While in-progress
                complete_style=Style(color="#00ff00"),  # Done
                finished_style=Style(color="#333333"),  # After completion
                table_column=Column(ratio=3),
            ),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        )


if __name__ == "__main__":
    with Progress() as progress:
        task1 = progress.add_task("Downloading...", total=1000)
        while not progress.finished:
            progress.update(task1, advance=0.5)
            time.sleep(0.1)
