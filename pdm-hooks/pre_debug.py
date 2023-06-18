#!/Users/maxludden/dev/venvs/maxgradient/bin/python
""""A python script to clear the logs and the console."""
# pylint: disable=W0611, E0401
from os import environ
from pathlib import Path
from typing import List

# from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from maxgradient.log import Log, LogConsole

HOME = Path.home()
MAX = HOME / "maxludden" / "dev" / "py" / "maxgradient"
DEBUG_LOG = MAX / "logs" / "debug.log"
INFO_LOG = MAX / "logs" / "info.log"
COUNT = MAX / "logs" / "count.txt"

console = LogConsole()
log = Log(console)


def clear(path: Path | LogConsole) -> Panel:
    """Clear the file at the given path."""
    if isinstance(path, LogConsole):
        msg1 = "[bold #aaffaa]Cleared[/] "
        msg2 = ("[i #7FD6E8]Console[/]",)
        msg = f"{msg1}{msg2}"
        log.log("DEBUG", msg=msg)
        path.clear()
        return Panel(
            msg,
            title="[b u #00aa00]Log[/]",
            border_style="#008000",
            expand=False,
            width=30,
        )
    elif isinstance(path, Path):
        msg1 = "[bold #aaffaa]Cleared[/] "
        msg2 = (f"[i #7FD6E8]{path.name}[/]",)
        msg = f"{msg1}{msg2}"
        log.log(level="DEBUG", msg=msg)
        if path.exists():
            with open(path, "w", encoding="utf-8") as outfile:
                outfile.write("")
            return Panel(
                msg,
                title="[b u #00aa00]Log[/]",
                border_style="#008000",
                expand=False,
                width=30,
            )
        log.error(f"File {path} does not exist. Unable to clear.")


def main() -> None:
    """Get the log files and clear them."""
    with open(COUNT, "r", encoding="utf-8") as infile:
        count = int(infile.read())
    if not count:
        count = int(environ.get("COUNT", 0))
    count += 1
    environ["COUNT"] = str(count)
    with open(COUNT, "w", encoding="utf-8") as outfile:
        outfile.write(str(count))
    panels: List[Panel] = []
    for logfile in (DEBUG_LOG, INFO_LOG, console):
        panels.append(clear(logfile))
    console.print(
        Panel(
            Columns(panels, expand=False, equal=True, align="center"),
            title="[dim]Clear Logs[/]",
            border_style="b #aaaaaa",
            expand=False,
            width=96,
        ),
        justify="center",
    )


if __name__ == "__main__":
    main()
