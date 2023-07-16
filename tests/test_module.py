from pathlib import Path

from sh import Command, RunningCommand

from maxgradient import Console, Gradient, Log

console = Console()
CWD = Path.cwd()
MG = CWD / "maxgradient"

python = Command("python")
python_version = python.bake("--version")
module = python.bake("-m")

def get_files() -> List[H]
with open(CWD /"tests"/"walk.txt", 'r') as infile:
    return infile.read().splitlines()

def run_modules(files: List[str]) -> None:
    """Run the modules."""
    for index, file in enumerate(files, start=1):
        console.line()
        out = module(file)