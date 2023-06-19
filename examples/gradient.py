# pylint: disable=E0402, E0401
import maxgradient as mg
from rich.syntax import Syntax

console = mg.Console(width=40, record=True)
console.print(
    Syntax(
        code="import maxgradient as mg\n\nconsole = mg.Console()\nconsole.\
gradient(\n\t\"Hello, World!\"\n)",
        lexer="python",
        padding=(1,4)
    )
)
console.gradient("    Hello, World!")
console.save_svg(
    "gradient_basic.svg",
    title="Gradient Basic"
)
