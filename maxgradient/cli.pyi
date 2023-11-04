from _typeshed import Incomplete
from maxgradient import Console as Console
from maxgradient.color import Color as Color, ColorParseError as ColorParseError
from maxgradient.gradient import Gradient as Gradient
from typer import Argument as Argument, Option as Option
from typing import List
from typing_extensions import Annotated

app: Incomplete
valid_colors: Incomplete
valid_justify: Incomplete

def complete_color(incomplete: str): ...
def justify_callback(value: str): ...
def parse_console(value: str): ...
def main(text: Annotated[str, None] = ..., style: Annotated[List[str], None] = ..., rainbow: Annotated[bool, None] = ..., justify: Annotated[str, None] = ..., colors: Annotated[List[str], None] = ..., panel: Annotated[bool, None] = ..., verbose: Annotated[bool, None] = ...) -> None: ...
