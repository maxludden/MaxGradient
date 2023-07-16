from typing import Union, Literal

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.console import Console, ConsoleOptions, RenderResult
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.style import Style
from rich.text import Text

from maxgradient.color_list import ColorList
from maxgradient.gradient import Gradient

Thickness = Literal["thin", "medium", "thick"]


class Rule(JupyterMixin):
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
        thickness: Thickness = "medium",
        gradient: bool = True,
        end: str = "\n",
        align: AlignMethod = "center",
    ) -> None:
        self.thickness = thickness

        if cell_len(self.characters) < 1:
            raise ValueError(
                "'characters' argument must have a cell width of at least 1"
            )
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.title = title
        self.gradient = gradient
        self.end = end
        self.align = align

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.characters!r})"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width
        color_list = ColorList(5)

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
            left = Text(characters * (side_width // chars_len + 1), end="")
            left = Gradient(left,[color_list[0], color_list[1], color_list[2]], end="")
            left.truncate(side_width - 1)
            right_length = width - cell_len(left.plain) - cell_len(title_text.plain)
            right = Text(characters * (side_width // chars_len + 1),end="")
            right = Gradient(right,[color_list[2], color_list[3], color_list[4]], end="")
            right.truncate(right_length)
            for i in [left, " ", title_text, " ", right]:
                rule_text.append(i)
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
        rule_text.plain.replace("\n", " ")
        yield rule_text

    def _rule_line(self, chars_len: int, width: int) -> Text:
        color_list = ColorList(5)
        rule_text = Text(self.characters * ((width // chars_len) + 1), end="")
        rule_text = Gradient(rule_text,colors=ColorList(5), end="")
        rule_text.truncate(width)
        rule_text.plain = set_cell_size(rule_text.plain, width)
        return rule_text

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(1, 1)

    @property
    def thickness(self) -> Thickness:
        return self._thickness

    @thickness.setter
    def thickness(self, value: Thickness) -> None:
        if value not in ["thin", "medium", "thick"]:
            raise ValueError(
                f"thickness must be one of 'thin', 'medium', or 'thick' (not {value!r})"
            )
        self._thickness = value
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
        text = "Gradient Rule"
    console = Console()
    console.rule()
    console.print(
        Rule(
            title=f"Rule (with gradient)",
        )
    )
    console.print(
        Rule(
            title="Thin Rule",
            thickness="thin",
            align="center",
        )
    )
    console.print(
        Rule(
            title = "Medium Left-aligned Non-gradient Rule",
            align = "left",
            gradient=False
        )
    )
    console.print(
        Rule("Thick Gradient Rule",
        )
    )
    console.print(
        Rule(
            title = "Medium Right-aligned Gradient Rule",
            align = "right"
        )
    )
