from typing import List

from rich.console import Console
from rich.terminal_theme import TerminalTheme
from rich.panel import Panel

from maxgradient.gradient import Gradient

GRADIENT_TERMINAL_THEME = TerminalTheme(
    background=(0, 0, 0),
    foreground=(255, 255, 255),
    normal=[
        (33, 34, 44),
        (255, 85, 85),
        (20, 200, 20),
        (241, 250, 140),
        (189, 147, 249),
        (255, 121, 198),
        (139, 233, 253),
        (248, 248, 242),
    ],
    bright=[
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (214, 172, 255),
        (255, 146, 223),
        (164, 255, 255),
        (255, 255, 255),
    ],
)

console = Console(record=True, width=80)

colors: List[str] = ["red", "orange", "yellow", "green", "cyan"]

gradient = Gradient(
    "Gradients are awesome!",
    colors=colors,
    justify="center",
    style="bold",
)
console.print(
    Panel(
        gradient,
        title="Example",
        expand=False,
        border_style="bold #ffffff",
        padding=(1,4),
        width=35
    ),
    justify='center'
)
console.save_svg(
    "docs/img/gradients_are_awesome.svg",
    title="",
    theme=GRADIENT_TERMINAL_THEME,
)
