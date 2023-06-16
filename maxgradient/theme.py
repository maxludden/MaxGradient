"""A container for style information, used by `gradient.Gradient'."""
from typing import Dict, Mapping, Optional

from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table
from rich.theme import Theme
from rich.highlighter import RegexHighlighter

from maxgradient.default_styles import GRADIENT_STYLES, styles_table

class LogHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "log."
    highlights = [
        r"(?P<keyword>.+(?=\d+)) ?(?P<index>\d+)?(?P<separator>:) ",
        r"(?P<keyword>[A-Za-z_]+)(?P<separator>:) "
    ]

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


if __name__ == "__main__":  # pragma: no cover
    theme = GradientTheme()
    console = Console(theme=theme)

    console.print(theme.get_theme_table(), justify="center")
