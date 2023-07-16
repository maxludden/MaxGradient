import os

from rich.console import Console
from rich.panel import Panel

from maxgradient.gradient import Gradient

console = Console()

log_file = "/Users/maxludden/dev/py/maxgradient/logs/debug.log"

if os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("")

console.print(Panel(Gradient("Cleared Logs. Starting new run.\n\n")))
