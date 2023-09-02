"""Rule class for maxgradient package."""
from typing import Literal, Union

from rich.align import AlignMethod
from rich.cells import cell_len, set_cell_size
from rich.console import Console, ConsoleOptions, RenderResult
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.rule import Rule as RichRule
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
        gradient (bool, optional): Whether to use gradient colors. Defaults to True.
        thickness (Thickness, optional): Thickness of the rule. Defaults to "medium".
        end (str, optional): Character at end of Rule. defaults to "\\\\n"
        align (str, optional): How to align the title, one of "left", "center", or "right". Defaults to "center".
    """

    # @spy
    def __init__(
        self,
        title: Union[str, Text] = "",
        *,
        gradient: bool = True,
        thickness: Thickness = "medium",
        end: str = "\n",
        align: AlignMethod = "center",
    ) -> None:
        self.gradient = gradient
        if thickness not in ["thin", "medium", "thick"]:
            raise ValueError(
                f"thickness must be one of 'thin', 'medium', or 'thick' (not {thickness!r})"
            )
        self.thickness = thickness
        if self.thickness == "thin":
            self.characters = "─"
        elif self.thickness == "medium":
            self.characters = "━"
        elif self.thickness == "thick":
            self.characters = "█"

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
        color_list = ColorList(5)
        self.left_colors = [color_list[0], color_list[1], color_list[2]]
        self.right_colors = [color_list[2], color_list[3], color_list[4]]

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.characters!r})"

    # @spy
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
            color_list = ColorList(5)
            yield Gradient(
                self._rule_line(chars_len, width),
                colors=[
                    color_list[0],
                    color_list[1],
                    color_list[2],
                    color_list[3],
                    color_list[4],
                ],
            )
            return

        if isinstance(self.title, Text):
            self.title_text = self.title
        else:
            self.title_text = console.render_str(self.title, style="rule.text")

        self.title_text.plain = self.title_text.plain.replace("\n", " ")
        self.title_text.expand_tabs()

        required_space = 4 if self.align == "center" else 2
        truncate_width = max(0, width - required_space)

        # / No Title
        if not truncate_width:
            yield self._rule_line(chars_len, width)
            return

        rule_text = Text(end=self.end)
        if self.align == "center":
            rule_text = self.center_rule(rule_text, truncate_width, chars_len, width)
        elif self.align == "left":
            self.title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(self.title_text)
            rule_text.append(" ")
            if self.gradient:
                rule_text.append(
                    Gradient(
                        characters * (width - self.title_text.cell_len - 1),
                        colors=self.right_colors,
                    )
                )
            else:
                rule_text.append(characters * (width - rule_text.cell_len))
        elif self.align == "right":
            self.title_text.truncate(truncate_width, overflow="ellipsis")
            rule_text.append(
                Gradient(
                    characters * (width - self.title_text.cell_len - 1),
                    colors=self.left_colors,
                )
            )
            rule_text.append(" ")
            rule_text.append(self.title_text)

        rule_text.plain = set_cell_size(rule_text.plain, width)
        # console.out(f"Rule3:\n{rule_text}", end="")
        yield rule_text

    # @spy
    def _rule_line(self, chars_len: int, width: int) -> Text:
        rule_text = Gradient(
            self.characters * ((width // chars_len) + 1), colors=self.left_colors
        )
        rule_text.truncate(width)
        rule_text.plain = set_cell_size(rule_text.plain, width)
        return rule_text

    def center_rule(
        self, rule_text: Text, truncate_width: int, chars_len: int, width: int
    ) -> Text:
        """Generate a centered rule.

        Args:
            rule_text (Text): Text of the rule.
            truncate_width (int): Width of the truncated rule.
            chars_len (int): Width of the rule characters.
            width (int): Width of the rule.
        """
        self.title_text.truncate(truncate_width, overflow="ellipsis")
        self.side_width = (width - cell_len(self.title_text.plain)) // 2
        if self.gradient:
            rule_text.append(
                Gradient(
                    self.characters * (self.side_width // chars_len + 1),
                    colors=self.left_colors,
                    end="",
                )
            )
        else:
            rule_text.append(
                Text(self.characters * (self.side_width // chars_len + 1), end="")
            )
        rule_text.append(" ")
        rule_text.append(self.title_text)
        rule_text.append(" ")
        if self.gradient:
            rule_text.append(
                Gradient(
                    text=self.characters * (self.side_width // chars_len + 1),
                    colors=self.right_colors,
                    end=" ",
                )
            )
        else:
            rule_text.append(
                Text(self.characters * (self.side_width // chars_len + 1), end=" ")
            )
        rule_text.truncate(width)
        return rule_text

    # @spy
    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        return Measurement(1, 1)

    @property
    def thickness(self) -> None:
        """Thickness of the rule line."""
        return self._thickness

    # @spy
    @thickness.setter
    def thickness(self, thickness: Thickness) -> None:
        if thickness not in ("thin", "medium", "thick"):
            raise ValueError(
                f'invalid value for thickness, expected "thin", "medium", "thick" (not {thickness!r})'
            )
        self._thickness = thickness

    @property
    def characters(self) -> str:
        """Characters used to draw the rule."""
        return self._characters

    @characters.setter
    def characters(self, characters: str) -> None:
        """Set or generate the characters to draw the rule."""
        # log.debug(msg=f"Called Rule.characters.setter with {characters!r}")
        if characters is not None:
            self._characters = characters
            return
        else:
            if self.thickness == "thin":
                self.characters = "─"
            elif self.thickness == "medium":
                self.characters = "━"
            elif self.thickness == "thick":
                self.characters = "█"
            log.debug(f"Rule.characters: {self.characters!r}")

    @classmethod
    def rule_example(cls) -> None:
        """Create a console with examples of Rule."""
        import sys

        from rich.console import Console

        try:
            text = sys.argv[1]
        except IndexError:
            text = "Gradient Rule"
        console = Console()
        console.print("[u b #ffffff]Rule Examples[/]", justify="center")
        console.line()
        console.print("[#ffffff]Gradient Rule without a title ⬇︎[/]", justify="center")
        console.print(GradientRule(thickness="thin"))
        console.line()
        console.print(
            GradientRule(
                title="Thin Gradient Rule",
                gradient=True,
                thickness="thin",
                align="center",
            )
        )
        console.line()
        console.print(
            GradientRule(title="Medium Gradient Rule", gradient=True, align="center")
        )
        console.line()
        console.print(
            GradientRule(
                title="Medium Left-aligned Non-gradient Rule",
                gradient=False,
                thickness="medium",
                align="left",
            )
        )
        console.line()
        console.print(
            GradientRule(title="Medium Right-aligned Gradient Rule", align="right")
        )
        console.line()
        console.print(GradientRule("Thick Gradient Rule", thickness="thick"))


if __name__ == "__main__":
    GradientRule.rule_example()
