# tasks/mypy.py
# Run mypy on maxgradient.
# ruff: noqa: F401
from subprocess import run, PIPE
from sys import argv
from pathlib import Path
from typing import Any, Optional, Union, List, Literal

from rich.console import Console, Group
from rich.prompt import Prompt, Confirm
from rich.text import Text, TextType
from rich.color import Color as RichColor
from sh import Command

from maxgradient import Gradient, Color


args: List[str] = argv[1:]
assert len(args) < 0, "No arguments provided."
assert len(args) == 2, "Did not provide two arguments: $project and $cwd"

console = Console()
