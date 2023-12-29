# ruff: noqa: F401
"""MaxGradient is a Python library for generating gradients in the terminal.

MaxGradient is a python library built on top of the great \
    [rich](https://github.com/Textualize/rich) library to \
    enable the generation of gradients in the terminal. It \
    is inspired by the [lolcat](https://github.com/tehmaze/lolcat) \
    project. MaxGradient is designed to be easy to use and \
    extendable. It is also designed to be used as a library \
    or as a command line tool.
"""
# ruff: noqa: F401

import maxgradient
from maxgradient import (
    Color,
    ColorList,
    Gradient,
    GradientConsole,
    GradientRule,
    GradientTerminalTheme,
    GradientTheme,
)

__version__ = "0.2.15"

__all__ = [
    "Color",
    "ColorList",
    "Gradient",
    "GradientRule",
    "GradientTheme",
    "GradientTerminalTheme",
    "maxgradient",
    "GradientConsole",
]

if __name__ == "__main__":
    console = GradientConsole()
    console.line(2)
    console.gradient(
        "MaxGradient is a Python library for generating gradients in the terminal.",
        justify="center",
        style="bold",
    )
    console.line(2)
