"""A container for style information, used by `gradient.Gradient'."""
from typing import Dict, Mapping, Optional, Tuple

from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table
from rich.terminal_theme import TerminalTheme
from rich.theme import Theme

from maxgradient.default_styles import GRADIENT_STYLES, styles_table
from maxgradient.highlighter import RegexHighlighter

_ColorTuple = Tuple[int, int, int]


class GradientTheme(Theme):
    """A container for style information used by 'MaxGradient.gradient.GradientConsole'.
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to \
            styles. Defaults to None for a theme with no styles.
        inherit (bool, optional): Inherit default styles. Defaults to True.
    """

    styles: Dict[str, Style]

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

    def __rich__(self) -> str:
        return styles_table()

    def __getitem__(self, name: str) -> Style:
        return self.styles[name]

    @classmethod
    def get_theme_table(cls) -> Table:
        """Get a table of all styles in the theme."""
        return styles_table()


class GradientTerminalTheme(TerminalTheme):
    """A custom terminal theme for MaxGradient."""

    def __init__(self) -> None:
        super().__init__(
            background=(35, 35, 35),
            foreground=(250, 250, 250),
            normal=[
                (35, 35, 35),
                (192, 0, 0),
                (0, 192, 0),
                (192, 192, 0),
                (0, 55, 255),
                (240, 0, 240),
                (0, 240, 240),
                (240, 240, 240),
            ],
            bright=[
                (0, 0, 0),
                (255, 0, 0),
                (0, 255, 0),
                (255, 255, 0),
                (0, 0, 255),
                (255, 0, 255),
                (0, 255, 255),
                (255, 255, 255),
            ],
        )


if __name__ == "__main__":  # pragma: no cover
    theme = GradientTheme()
    console = Console(theme=theme)

    console.print(theme.get_theme_table(), justify="center")
