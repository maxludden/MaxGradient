# ruff: noqa: F401
from pathlib import Path
from typing import List
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

COLOR: Path = Path("/Users/maxludden/dev/py/maxgradient/src/maxgradient/color.py")

console = Console()
syntax = Syntax.from_path(
    str(COLOR.resolve()),
    line_numbers=True,
    padding=(1,4),
    background_color="#111111"
    )
console.print(syntax)

