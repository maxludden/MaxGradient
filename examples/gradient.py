# pylint: disable=E0402, E0401
import maxgradient as mg
from maxgradient.theme import GradientTerminalTheme


console = mg.Console(width=40, record=True)

console.gradient("    Hello, World!")
console.save_svg(
    "Images/hello_world.svg",
    title="Hello, World! Result",
    theme=GradientTerminalTheme()
)
