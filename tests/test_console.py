from maxgradient._console import Console
from maxgradient._gradient_color import GradientColor as GC

console = Console()
console.line(2)
console.gradient_rule("Sample Text")
for color in GC.NAMES:
    console.print(color)
