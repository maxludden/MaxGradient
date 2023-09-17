<html>
    <head>
        <link href="styles/gradient.css" rel="stylesheet">
    </head>
    <body>
        <!--MaxGradient Banner-->
        <img src="https://raw.githubusercontent.com/maxludden/maxludden/621fcb611c1e52160d89d33e1441b34948c37752/maxgradient_banner.svg" alt="MaxGradient" width="100%">
        <!--End of Banner-->
​        <div class="badges">
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Python-3.9 | 3.10 | 3.11-blue?logo=python" alt="PyPI - MaxGradient"></a>
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/PyPI-MaxGradient-blue?" alt="PyPI - MaxGradient"></a>
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Version-0.1.7-bbbbbb" alt="Version - 0.1.7"></a>
​            <a href="https://pdm.fming.dev/"><img class="badge" src="https://camo.githubusercontent.com/acf0526fc1f541f9d980d7983ff5ab8e540cf2136206c2b5dc740f658a37fac0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f70646d2d6d616e616765642d626c756576696f6c6574"></a>
​        </div>
        <!--End of badges-->
​        <div class="summary">
            <p><span class="mg">MaxGradient</span> automates the printing gradient colored text to the console. It's built upon the great <a href="https://rich.readthedocs.io/en/latest/introduction.html"> <span class="warm-wipe">rich library</span></a>. It contains a Console that can serve as a drop in replacement for <span class="lightblue-cyan-wipe">rich.rich.Console</span> and has an expanded Color class which can parse X11 color names on top of rich's standard colors. <span class="mg">MaxGradient</span> is a work in progress and I'm open to any suggestions or contributions.</span></p>
        </div>
​        <div class="body">

## Installation

<div class="section">
    <p><span class="mg">MaxGradient</span> can be installed from PyPi using your favorite package manager:</p>

### PDM <span class="recommend">(Recommended)</span></h3>

```shell
pdm add maxgradient
```

### Pip

```shell
pip install maxgradient
```

## Usage

### Basic Usage

<div class="section">
    <p>The basic usage is to create a console object and use it to print gradient text:</p>

```python
import maxgradient as mg

console = mg.Console()
console.gradient("Hello, World!")
```

<img class="result" src="Images/hello_world.svg" alt="Hello, World!"/>

---

## <span class="cool-wipe-header">Gradient</span>

<div class="section">
    <p>You may also instantiate a Gradient Object. The <span class="red-magenta-wipe">Gradient </span>class is a subclass of the<span class="lightblue-cyan-wipe"> rich.text.Text</span> class, and can be used in the same way. The <span class="magenta-violet-wipe">Gradient</span> class has a few extra arguments available though.<p>

```python
class Gradient(rich.rich.Text):
    """Text with gradient color / style."""

    def __init__ (
        ext: Optional[str | Text] = "",
        colors: Optional[str|List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = Style.null(),
        *,
        # The arguments below are used directly by Text
        # so I won't cover them here. If you have
        # questions check out the rich documentation.
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,) -> None:
```

The Gradient class can utilize the above arguments to get a plethora of different gradients.

<a href="Images/gradient_examples.svg" target="_blank">
  <img src="Images/gradient_examples.svg" alt="Gradient Examples" onclick="zoomImage(this)">
</a>

<br><br><hr><br>

## Color

The final main component of <span class="violet-purple-wipe">MaxGradient</span> is expanding the <span class="purple-blue-wipe">rich.color.Color</span> class. The <span class="rainbow-wipe">MaxGradient </span>.<span class="lightblue-cyan-wipe">Color</span> class can still parse and utilize the <span class="cyan-green-wipe">rich.color.Color</span>'s <a class="green-yellow-wipe" href="https://rich.readthedocs.io/en/latest/appendix/colors.html" alt="Rich Standard Colors">standard colors</a> but in addition to Hex and RGB colors, it can also parse RGB Tuples as well as X11 color names. I've also included the colors that <span class="rainbow-wipe">MaxGradient</span> uses to create random gradients from for convenience. The follow are the available named colors as well as there hex and rgb colors:

<img src="Images/available_colors.svg" >

### Color Examples

```python
import maxgradient as mg

console = mg.Console()
console.print("[bold green]This is a a vibrant green color!")
```

<img class="result" src="Images/color_example.svg" alt="Color Example">

### Changelog v1.0.6

- Added docs
- Changed docs to readthedocs theme.
</body>
</html>
