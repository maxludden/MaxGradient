from maxgradient.console import Console
from maxgradient.gradient import Gradient
from maxgradient.color import Color
from maxgradient._gc import GradientColor as GC

console = Console()
console.line(2)
console.gradient_rule("Sample Text")
for color in GC.NAMES:
    console.print(color)