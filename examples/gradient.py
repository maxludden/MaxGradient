# pylint: disable=E0402, E0401
from lorem_text import lorem
from maxgradient.console import Console
from maxgradient.gradient import Gradient
from rich.panel import Panel
from maxgradient.theme import GradientTerminalTheme

TEXT = lorem.paragraphs(2)

console = Console(width=40,record=True)
console.line(2)
console.gradient("    Hello, World!")
console.line(2)

console.save_svg(
    "Images/hello_world.svg",
    title="Hello, World! Result",
    theme=GradientTerminalTheme()
)
