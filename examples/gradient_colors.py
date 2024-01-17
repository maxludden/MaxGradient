"""This example displays all of the colors used to generate random gradients."""
from enum import Enum
from pathlib import Path

from rich.columns import Columns
from rich.console import Console

from maxgradient._gradient_color import GradientColor
from maxgradient.rule import GradientRule
from maxgradient.theme import GRADIENT_TERMINAL_THEME


class GradientColorFormat(Enum):
    """Gradient color formats."""

    COLUMN = "column"
    COLUMNS = "columns"
    TABLE = "table"


def gradient_color_example(
    format: GradientColorFormat = GradientColorFormat.COLUMNS,
) -> None:
    """Display all of the colors used to generate random gradients."""

    console = Console(record=True)
    match format:
        case GradientColorFormat.COLUMN:
            console.print(GradientRule("Gradient Color Column"))
            [console.print(color, justify="center") for color in GradientColor.NAMES]
        case GradientColorFormat.COLUMNS:
            console.print(GradientRule("New Gradient Colors"))
            columns = Columns(
                [GradientColor(color) for color in GradientColor.NAMES],
                equal=True,
                expand=True,
            )
            console.print(columns)
        case GradientColorFormat.TABLE, _:
            console.print(GradientColor.color_table())

    filepath: Path = Path.cwd() / "docs" / "img" / "new_gradient_colors.svg"
    console.save_svg(
        str(filepath), title="New Gradient Colors", theme=GRADIENT_TERMINAL_THEME()
    )


if __name__ == "__main__":
    gradient_color_example()
