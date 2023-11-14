# ruff: noqa: F401
# Display the mypy output in a table

import re
from pathlib import Path
from typing import Any, Optional
from subprocess import run, CalledProcessError, PIPE

from pendulum import datetime, now as dtnow
from rich.columns import Columns
from rich.console import Console, Group, NewLine
from rich.table import Table
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from loguru import logger
from pydantic import BaseModel, Field

# Create a Console instance
console = Console()
console.line(2)
mypy_output = Path.cwd() / "logs" / "mypy_output.txt"
ERROR_REGEX: re.Pattern = re.compile(  # Pattern to match error_msgs
    r"(?P<pkg>.+)\/(?P<mod_stem>\w+)\.(?P<ext>\w{0,5}):(?P<line_no>\d+): (?P<level>\w+):(?P<indent> +)(?P<msg>.+)$",
    re.I,
)
REPORT_REGEX = re.compile(
    r"Found (?P<errors>\d+) errors in (?P<files>\d+) files \(checked (?P<source>\d+) source file\)",
    re.I
)
now = dtnow.fortmat("YYYY-MM-DD HH:nn:ss:SSSS A")

logger.configure(
    handlers=[
        {
            "sink": "logs/debug.log",
            "level": "DEBUG",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            "colorize": True
        },
        {
            "sink": "logs/info.log",
            "level": "INFO",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            "colorize": True,
            "backtrace": True,
            "diagnose": True
        },
        dict(
            sink=lambda msg: console.print(
                f"[i dim]{now}[/][[b #ffff88]{msg}[/]",
                justify='left'
            ),
            level="SUCCESS",
            format="{message}",
            colorize=False,
            backtrace=False,
            diagnose=False
        )
    ]
)


# with open(mypy_output, "r", encoding="utf-8") as infile:
#     mypy_line = infile.readlines()

class MypyMsg(BaseModel):
    """Mypy error message."""
    line: str = Field(..., description="Raw error message.")
    enumerated_line: int= Field(..., description="Line number of error.", ge=1)
    pkg: str = Field(..., description="Package name of the error.")
    mod: str = Field(..., description="Module name of the error.")
    ext: str = Field(..., description="File extension of the error.")
    line_no: int = Field(..., description="Line number of error.", ge=1)
    level: str = Field(..., description="Level of error.")
    level_style: str = Field(..., description="Style of error level.")
    indent: int = Field(..., description="Indentation of error message.", ge=0)
    msg: str = Field(..., description="Error message.")

    def __init__(self, error_line: str, enumerated_line: int, verbose: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(error_line, str), "Error_line input must be a string."
        self.input: str = error_line
        self.enumerated_line: int = enumerated_line
        if verbose:
            log = logger.debug
        else:
            log = logger.success
        log(f"MypyMsg.__init__(error_line={error_line}")

        match: Optional[re.Match] = ERROR_REGEX.search(error_line)
        if match:
            log("Parsed mypy error message:")
            self.pkg: str = match.group("pkg")
            log(f"- pkg: {self.pkg}")

            self.mod: str = match.group("mod")
            log(f"- mod: {self.mod}")

            self.ext: str = match.group("ext")
            log(f"- ext: {self.ext}")

            line_no: str = match.group("line_no")
            self.line_no: int = int(line_no)
            log(f"- lineno: {self.line_no}")

            self.level: str = str(match.group("level"))
            log(f"- level: {self.level}")
            match self.level:
                case "error":
                    self.level_style = "bold #ff0000"
                case "note":
                    self.level_style = "bold #ac64ff"
                case _:
                    self.level_style = "bold #cdcdcd"

            indent: str = match.group("indent")
            self.indent: int = len(indent)
            log(f"- indent: {self.indent}")

            self.msg: str = match.group("msg")
            log(f"- msg: {self.msg}")
        raise ValueError("Invalid mypy error message.")
    
    def append(self, msg: str, enumerated_line: int) -> bool:
        """Append a line to the error message."""

        match: Optional[re.Match] = ERROR_REGEX.search(error_line)
        if match:
            self.pkg: str = match.group("pkg")
            self.mod: str = match.group("mod")
            self.ext: str = match.group("ext")
            line_no: str = match.group("line_no")
            self.line_no: int = int(line_no)
            self.level: str = str(match.group("level"))
            match self.level:
                case "error":
                    self.level_style = "bold #ff0000"
                case "note":
                    self.level_style = "bold #ac64ff"
                case _:
                    self.level_style = "bold #cdcdcd"
            indent: str = match.group("indent")
            self.indent: int = len(indent)
            self.msg: str = match.group("msg")
            return True
        return False

    def __rich__(self) -> Panel:
        log_level: str = ""
        if self.level == "error":
            log_level = " ERROR"
        elif self.level == "note":
            log_level = " NOTE"
        table = Table(
            title=f"Mypy{log_level} {self.enumerated_line}",
            show_header=True,
            title_style=self.level_style,
            header_style="bold #ffffff",
            border_style=self.level_style,
            expand = False,
            width=60
        )
        table.add_column("Package", style="bold #ffffff", justify="center")
        table.add_column("Module", style="bold #ffffff", justify="center")
        table.add_column("Line Number", style="bold #ffffff", justify="center")
        table.add_column("Level", style="bold #ffffff", justify="center")
        module = f"[bolb #ffffff]{self.mod}[/bold]"
        line_number = f"[bold #00ffff]{self.line_no: ^7}[/bold]"
        
        table.add_row(
            module, line_number, str(self.line_no), self.level
        )
        message: Text = Text(
            self.msg,
            style=self.level_style,
            justify="left"
        )
        message_group = Group(
            table, NewLine(), message
        )
        return Panel(message_group, border_style=self.level_style)

class Mypy(BaseModel):
    """Mypy report."""
    lines: list[MypyMsg] = Field(..., description="List of mypy error messages.")
    def __init__(self) -> None:
        mypy_result = run(["mypy", "-m", "maxgradient","--ignore-missing-imports"], capture_output=True)
        line_errors = mypy_result.stderr.decode("utf-8").splitlines()
        for enumerated_line, line in enumerate(line_errors, 1):
            if enumerated_line == 1:
                self.lines.append(MypyMsg(line, enumerated_line))


if __name__ == "__main__":
    mypy_result = run(["mypy", "-m", "maxgradient","--ignore-missing-imports"], capture_output=True)
    line_errors = mypy_result.stderr.decode("utf-8")
    for lineno, line in enumerate(line_errors.splitlines(), 1):
        mypymsg = MypyMsg(line, lineno)
