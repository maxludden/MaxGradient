from pathlib import Path
from maxgradient import Gradient, Console
from rich.text import Text

class GayEnough:
    console = Console(record=True)
    gradient = Gradient("Is this gay enough yet?!")
    svg_path = Path("/Users/maxludden/dev/py/maxgradient/docs/img") / "gayenough.svg"

    def __init__(self) -> None:
        from rich.console import Console
        from rich.syntax import Syntax
        from rich.text import Text

        from maxgradient import Gradient
        console = Console()
        console.print(
            Syntax("""from rich.console import Console
from maxgradient import Gradient

console = Console()
console.print(Gradient("Is this gay enough yet?!"))""",
            "python"
        ))
        
        console.print(
            Gradient("Is this gay enough yet?!")
        )


    # def hard(self) -> None:
    #     console.print(
    #         "[b #91B0DF]from[/] [#AEAAEE]rich.console[/] [b #91B0DF]import[/] [i #D6D594] Console]"
    #     )

if __name__ == '__main__':
    GayEnough()