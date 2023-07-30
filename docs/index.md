![MaxGradient](../Images/maxgradient_banner.svg)

MaxGradient automates the printing gradient colored text to the console. It's built upon the great rich library. It contains a Console that can serve as a drop in replacement for rich.rich.Console and has an expanded Color class which can parse X11 color names on top of rich's standard colors. MaxGradient is a work in progress and I'm open to any suggestions or contributions.

# Installation

MaxGradient can be installed from PyPi using your favorite package manager:

## PDM (Recommended)

```shell
pdm add maxgradient
```

## Pip

```shell
pip install maxgradient
```

# Usage

## Quick Start

The basic usage is to create a console object and use it to print gradient text:

```python
import maxgradient as mg

console = mg.Console()
console.gradient("Hello, World!")
```

![Hello, World!](../Images/hello_world.svg)
