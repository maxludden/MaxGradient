"""Generate a gradient panel."""

from os import environ
from sys import stdout
from io import StringIO
from typing import Any, Optional, Iterable

from rich.panel import Panel
from rich.text import Text
from rich.containers import Lines