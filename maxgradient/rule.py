from enum import Enum
from typing import Literal, Optional, Union

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.console import Console, ConsoleOptions, RenderResult
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.style import Style
from rich.text import Text

from maxgradient.color_list import ColorList
from maxgradient.gradient import Gradient
from maxgradient.log import Log

Thickness = Literal["thin", "medium", "thick"]
console = Console()
log = Log


class GradientRule(JupyterMixin):
    """A console renderable to draw a horizontal rule (line).

    Args:
        title (Union[str, Text], optional): Text to render in the rule. Defaults to "".
        characters (str, optional): Character(s) used to draw the line. Defaults to "─".
        style (StyleType, optional): Style of Rule. Defaults to "rule.line".
        end (str, optional): Character at end of Rule. defaults to "\\\\n"
        align (str, optional): How to align the title, one of "left", "center", or "right". Defaults to "center".
    """

    def __init__(
        self,
        title: Union[str, Text] = "",
        *,
        thickness: Thickness = "thin",
        characters: Optional[str] = None,
        end: str = "\n",
        align: AlignMethod = "center",
    ) -> None:
        if thickness not in ["thin", "medium", "thick"]:
            raise ValueError(
                f"thickness must be one of 'thin', 'medium', or 'thick' (not {thickness!r})"
            )
        self.set_thickness = thickness

        if cell_len(self.characters) < 1:
            raise ValueError(
                "'characters' argument must have a cell width of at least 1"
            )
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.title = title
        self.thickness = thickness
        self.end = end
        self.align = align

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.characters!r})"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width

        characters = (
            "-"
            if (options.ascii_only and not self.characters.isascii())
            else self.characters
        )

        chars_len = cell_len(characters)
        if not self.title:
            yield self._rule_line(chars_len, width)
            return

        if isinstance(self.title, Text):
            title_text = self.title
        else:
            title_text = console.render_str(self.title, style="rule.text")

        title_text.plain = title_text.plain.replace("\n", " ")
        title_text.expand_tabs()

        required_space = 4 if self.align == "center" else 2
        truncate_width = max(0, width - required_space)
        if not truncate_width:
            yield self._rule_line(chars_len, width)
            return

        rule_text = Text(end=self.end)
        if self.align == "center":
            title_text.truncate(truncate_width, overflow="ellipsis")
            side_width = (width - cell_len(title_text.plain)) // 2
            left = Gradient(characters * (side_width // chars_len + 1))
            left.truncate(side_width - 2)
            right_length = width - cell_len(left.plain) - cell_len(title_text.plain)
            right = Gradient(characters * (side_width // chars_len + 1))
            right.truncate(right_length - 1)
            rule_text.append(left.plain + " ")
            rule_text.append(title_text)
            rule_text.append(" " + right.plain)
        elif self.align == "left":
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(title_text)
            rule_text.append(" ")
            rule_text.append(characters * (width - rule_text.cell_len))
        elif self.align == "right":
            title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(characters * (width - title_text.cell_len - 1))
            rule_text.append(" ")
            rule_text.append(title_text)

        rule_text.plain = set_cell_size(rule_text.plain, width)
        yield rule_text

    def _rule_line(self, chars_len: int, width: int) -> Text:
        rule_text = Text(self.characters * ((width // chars_len) + 1))
        rule_text.truncate(width)
        rule_text.plain = set_cell_size(rule_text.plain, width)
        return rule_text

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(1, 1)

    @property
    def thickness(self) -> None:
        """Thickness of the rule line."""
        return self._thickness

    @thickness.setter
    def thickness(self, thickness: Thickness) -> None:
        if thickness not in ("thin", "medium", "thick"):
            raise ValueError(
                f'invalid value for thickness, expected "thin", "medium", "thick" (not {thickness!r})'
            )
        self._thickness = thickness

    @property
    def characters(self) -> str:
        """Retrieves the character(s) used to draw the rule line."""
        return self.characters

    @characters.setter
    def characters(self) -> None:
        """Character(s) used to draw the line.

        Notes: Characters.setter() must be called after thickness.setter() to ensure that the correct characters are used.
        """
        log.debug(f"Called rule.characters()")
        if self.thickness == "thin":
            self.characters = "─"
        elif self.thickness == "medium":
            self.characters = "━"
        else:  # if thickness == "thick"
            self.characters = "█"


if __name__ == "__main__":  # pragma: no cover
    import sys

    from rich.console import Console

    try:
        text = sys.argv[1]
    except IndexError:
        text = "Hello, World"
    console = Console()
    console.print(GradientRule(title=text))

    console = Console()
    console.print(GradientRule("foo"), width=4)
