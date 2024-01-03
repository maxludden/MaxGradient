from sh import Command, ErrorReturnCode
from pathlib import Path
from rich.console import Console
from rich.traceback import install as tr_install
from rich.text import Text
from typing import List
# from rich.table import Column
from rich.progress import Progress, TextColumn, SpinnerColumn, BarColumn, MofNCompleteColumn, TaskID
from maxgradient.gradient import Gradient
from rich.panel import Panel

python = Command("/Users/maxludden/dev/venvs/MaxGradient/bin/python").bake("-m",)

def get_modules() -> List[Path]:
    """Get all modules in current directory."""
    CWD = Path.cwd()
    SRC = CWD / "src"
    MODULES: List[Path] = list(SRC.glob("*.py"))
    return MODULES

def get_console() -> Console:
    
    """Create console with traceback handler."""
    console = Console()
    tr_install(console=console, show_locals=True)
    return console

def get_progress(console: Console = get_console()) -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn("point"),
        BarColumn(
            bar_width=None
        ),
        MofNCompleteColumn(),
        console=console,
        refresh_per_second=20
    )
def add_task(progress: Progress = get_progress()) -> TaskID:
    task = progress.add_task(
        "[b #d8d855]Running Modules...[/]",
        total=(len(get_modules())*2))
    return task

console = get_console()
progress = get_progress(console)
task = add_task(progress)



def run(
    run_progress: Progress = progress,
    task: TaskID = task,
    )

if __name__ == "__main__":
    console = get_console()
    with get_progress(console) as progress:
        task = add_task(progress)
        for file in get_modules():
            progress.update(
                task,
                advance=0.4,
                description=f"[b #d8d855]Attempting to run {file.name}...[/]"
            )
            if file.suffix == ".py":
                progress.update(
                task,
                advance=0.1,
                description=f"[b #ff00ff]{file.name}: Running[/]"
            )
                