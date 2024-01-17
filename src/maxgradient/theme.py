"""A container for style information, used by `gradient.Gradient'."""
from typing import Dict, Mapping, Optional, Tuple

from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table
from rich.terminal_theme import TerminalTheme
from rich.theme import Theme

from maxgradient.default_styles import GRADIENT_STYLES, styles_table

_ColorTuple = Tuple[int, int, int]


class GradientTheme(Theme):
    """A container for style information used by 'MaxGradient.gradient.GradientConsole'.
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to \
            styles. Defaults to None for a theme with no styles.
        inherit (bool, optional): Inherit default styles. Defaults to True.
    """

    styles: Dict[str, StyleType]

    def __init__(
        self, styles: Optional[Mapping[str, StyleType]] = None, inherit: bool = True
    ) -> None:
        super().__init__(styles=styles, inherit=True)
        self.styles = GRADIENT_STYLES.copy() if inherit else {}
        if styles is not None:
            self.styles.update(
                {
                    name: style if isinstance(style, Style) else Style.parse(style)
                    for name, style in styles.items()
                }
            )

    def __repr__(self) -> str:
        return f"GradientTheme({self.styles!r})"

    def __rich__(self) -> Table:
        return styles_table()

    def __getitem__(self, name: str) -> Style:
        return Style.parse(str(self.styles[name]))

    @classmethod
    def get_theme_table(cls) -> Table:
        """Get a table of all styles in the theme."""
        return styles_table()


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

if __name__ == "__main__":  # pragma: no cover
    theme = GradientTheme()
    console = Console(theme=theme)

    console.print(theme.get_theme_table(), justify="center")
