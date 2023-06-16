""""A python script to clear the logs and the console."""
# pylint: disable=W0611, E0401
from os import environ
from pathlib import Path

from rich.panel import Panel
from rich.console import Console

CWD = Path.cwd()
DEBUG_LOG = CWD / "logs" / "debug.log"
INFO_LOG = CWD / "logs" / "info.log"
COUNT = CWD / "logs" / "count.txt"

console = Console()

def clear(path: Path) -> bool:
    """Clear the file at the given path."""
    if path.exists():
        with open(path, 'w', encoding='utf-8') as outfile:
            outfile.write("")
            console.print(
                Panel(
                    f"[lime]Cleared[/] [i white]{path.name: <10}[/i white]",
                    title='[b u #00aa00]Log[/]',
                    border_style='#008000',
                    expand=False,
                    width=30
                ),
                justify='center',
            )
            return True
    return False

def main() -> None:
    """Get the log files and clear them."""
    with open(COUNT, 'r', encoding='utf-8') as infile:
        count = int(infile.read())
    if not count:
        count = int(environ.get('COUNT', 0))
    count += 1
    environ['COUNT'] = str(count)
    with open(COUNT, 'w', encoding='utf-8') as outfile:
        outfile.write(str(count))

    console.clear()
    for log in (DEBUG_LOG, INFO_LOG):
        clear(log)


if __name__ == "__main__":
    main()
