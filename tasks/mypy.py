# tasks/mypy.py
# Run mypy on maxgradient.
# ruff: noqa: F401
import re
from io import StringIO
from pathlib import Path
from subprocess import PIPE, CompletedProcess, run
from sys import argv
from typing import Optional, Tuple, List

from loguru import logger
from maxgradient import Gradient
from rich import inspect
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install

MYPY_THEME = Theme(
    {
        "mypy.error": "bold #ff0000",
        "mypy.numbers": "bold #8BE9FD",
        "mypy.success": "bold #00ff00",
        "mypy.colon": "bold #ffffff",
    }
)


class MypyHighlighter(RegexHighlighter):
    base_style = "mypy."
    highlights = [
        r"(?P<error_msg>:)",
        r"^(?P<error_path>/.*):(?P<error_line>\d+): error: (?P<error_msg>.*)$",
        r"(?P<numbers>\d+)",
        r"(?P<success>Success)",
    ]


console = Console()
logger.remove()
logger.add(
    lambda msg: console.print(msg),
    level="SUCCESS",
    colorize=False,
    backtrace=True,
    diagnose=True,
)


class MypyError:
    def __init__(self, message: str, index: int):
        self.parts: List[str] = self._split_msg(message)
        self.index: int = index
        
    def _split_msg(self, message: str) -> List[str]:
        """Split the message into a list of strings.
        
        Returns:
            List[str]: A list of strings.
        """
        return [part.strip() for part in message.split(":")]
    
    @property
    def path(self) -> Path:
        """The path to the file in which the error occurred."""
        path = Path(self.parts[0])
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found.")
        return path

    @property
    def line(self) -> int:
        """The line on which the error occurred."""
        return int(self.parts[1])

    @property
    def error_msg(self) -> str:
        """The error message."""
        return self.parts[3]
class MypyRun:
    OUTFILE: Path = Path('/Users/maxludden/dev/py/MaxGradient/logs/mypy-output.txt')

    def __init__(self, console: Optional[Console] = None) -> None:
        logger.debug("Initializing MypyRun()")
        self.console = console or Console()
        if not self.OUTFILE.exists():
            with open(self.OUTFILE, "w") as f:
                f.write("Mypy output file")
        self.result: str = self.init()
        

    def init(self) -> str:
        logger.debug("Entering MypyRun.init()")
        buffer: StringIO = StringIO()
        result = run(
            args=["mypy", "-p", "src.maxgradient", "--ignore-missing-imports"],
            stdout=PIPE,  # Capture the standard output
            stderr=PIPE,  # Capture the standard error
        )
        self.returncode = result.returncode
        # Write the standard output and error to the buffer
        buffer.write(result.stdout.decode().strip())
        self.stdout = buffer.getvalue()
        buffer.flush()
        buffer.write(result.stderr.decode().strip())
        self.stderr = buffer.getvalue()
        if not self.stderr == "":
            return str(self.stderr)
        else:
            return self.stdout

    @property
    def console(self) -> Console:
        """A console instance for mypy."""
        logger.debug("Retrieving self._console")
        if self._console is None:
            self._console = self.get_console()
        install(console=self._console)
        return self._console

    @console.setter
    def console(self, console: Optional[Console]) -> None:
        """A console instance for mypy.

        Args:
            console (Console): A console instance for mypy.
        """
        logger.debug(f"Setting self._console({console})")
        if console is None:
            console = self.get_console()
        self._console = console

    def get_console(self) -> Console:
        """Generate a console instance for mypy if one isn't provided \
            and installs the rich traceback handler."""
        logger.debug("Entering MypyRun.get_console()")
        console = Console(record=True, theme=MYPY_THEME, highlighter=MypyHighlighter())
        install(console=console)
        logger.debug("Installed rich traceback handler.")
        return console

    @property
    def stdout(self) -> str:
        """The standard output from mypy."""
        logger.debug("Retrieving self._stdout")
        return self._stdout

    @stdout.setter
    def stdout(self, stdout: str) -> None:
        """ "Set the standard output from mypy."""
        logger.debug(f"Setting self._stdout({stdout})")
        self._stdout = stdout

    @property
    def stdout_text(self) -> Text:
        """The rendered standard output stream from mypy."""
        logger.debug("Retrieving self._stdout_text")
        return self.console.render_str(
            text=self.stdout, highlight=True, highlighter=MypyHighlighter()
        )

    @property
    def stderr(self) -> Optional[str]:
        """The standard error from mypy."""
        logger.debug("Retrieving self._stderr")
        if self._stderr is None:
            self._stderr = ""
        return self._stderr

    @stderr.setter
    def stderr(self, stderr: str) -> None:
        """Set the standard error from mypy."""
        logger.debug(f"Setting self._stderr({stderr})")
        self._stderr = stderr

    @property
    def stderr_text(self) -> Text:
        """The rendered standard error stream from mypy."""
        logger.debug("Retrieving self._stderr_text")
        return self.console.render_str(
            text=self._stderr, highlight=True, highlighter=MypyHighlighter()
        )

    @property
    def returncode(self) -> int:
        """The return code from mypy."""
        logger.debug("Retrieving self._returncode")
        return self._returncode

    @returncode.setter
    def returncode(self, returncode: int) -> None:
        """Set the return code from mypy."""
        logger.debug(f"Setting self._returncode({returncode})")
        self._returncode = returncode

    def success(self) -> Panel:
        logger.debug("Entering MypyRun.success()")
        return Panel(
            self.stdout_text,
            title="[i #00ff00]MyPy Passed![/]",
            border_style="bold #008800",
            expand=False,
            padding=(1, 2),
        )

    def error(self) -> Panel:
        logger.debug("Entering MypyRun.error()")
        title = Text(f"Error {self.returncode}", style="bold #ff0000")
        return Panel(
            self.stderr_text,
            title=title,
            border_style="bold #ff0000",
            expand=False,
            padding=(1, 2),
        )


if __name__ == "__main__":
    console = Console()
    mypy = MypyRun()
    console.line(2)
    if mypy.returncode == 0:
        console.print(mypy.success(), justify="center")
    else:
        console.print(mypy.error(), justify="center")
