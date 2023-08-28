"""Test the CLI module."""
from io import StringIO

import typer
from rich.text import Text
from typer.testing import CliRunner

from maxgradient import Console, Gradient
from maxgradient.cli import app

console = Console(file=StringIO())


def test_app():
    """Test the CLI app."""
    result = CliRunner().invoke(app, ["Hello world!"])
    assert (
        result.exit_code == 0
    ), f"Exit Code: {result.exit_code}. CLI app should exit with code 0."
    console.print(result)


if __name__ == "__main__":
    test_app()
