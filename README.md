<html>
    <head>
        <link href="styles/style.css" rel="stylesheet">
    </head>
    <body>
        <!--MaxGradient Banner-->
        <img src="docs/img/MaxGradient.svg" alt="MaxGradient" width="100%">
        <!--End of Banner-->
​        <div class="badges">
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Python-3.9 | 3.10 | 3.11 | 3.12 -blue?logo=python" alt="PyPI - MaxGradient"></a>
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/PyPI-MaxGradient-blue?" alt="PyPI - MaxGradient"></a>
​            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Version-0.2.9-bbbbbb" alt="Version 0.2.9"></a>
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

![PDM](docs/img/pdm-maxgradient.svg)

### Pip

![Pip](docs/img/pip.svg)

## Usage

### Basic Usage

<div class="section">
    <p>The basic usage is to create a console object and use it to print gradient text:</p>

![Console Gradient](docs/img/console_gradient.svg)
<img class="result" src="docs/img/hello_world.svg" alt="Hello, World!"/>

---

## <span class="cool-wipe-header">Gradient</span>

<div class="section">
    <p>You may also instantiate a Gradient Object. The <span class="red-magenta-wipe">Gradient </span>class is a subclass of the<span class="lightblue-cyan-wipe"> rich.text.Text</span> class, and can be used in the same way. The <span class="magenta-violet-wipe">Gradient</span> class has a few extra arguments available though.<p>

![Gradient Class](docs/img/gradient_class.svg)

The Gradient class can utilize the above arguments to get a plethora of different gradients.

<img src="docs/img/gradient_examples.svg" alt="Gradient Examples">

## Color

The final main component of <span class="violet-purple-wipe">MaxGradient</span> is expanding the <span class="purple-blue-wipe">rich.color.Color</span> class. The <span class="rainbow-wipe">MaxGradient </span>.<span class="lightblue-cyan-wipe">Color</span> class can still parse and utilize the <span class="cyan-green-wipe">rich.color.Color</span>'s <a class="green-yellow-wipe" href="https://rich.readthedocs.io/en/latest/appendix/colors.html" alt="Rich Standard Colors">standard colors</a> but in addition to Hex and RGB colors, it can also parse RGB Tuples as well as X11 color names. I've also included the colors that <span class="rainbow-wipe">MaxGradient</span> uses to create random gradients from for convenience. The follow are the available named colors as well as there hex and rgb colors:

<img src="docs/img/available_colors.svg" >

### Color Examples

![Color](docs/img/color_code.svg)

<img class="result" src="docs/img/color_example.svg" alt="Color Example">
<br /><br /></br />
<figure style="display:flex;align-content:center;">
    <p style="text-align:center;">Created by</p>
    <img style="margin:auto;" width="25%" src="docs/img/MaxLogo.svg" alt="Max Ludden's Logo" />
</figure>

## Changelog

### v0.2.9 | Updated Banner

- Updated MaxGradient Logo and Favicon
- Updated banner to include new logo as http rather than refernceing the svg file locally.

### v0.2.8 | Fixed `cli.py`

- Fixed `cli.py` so that it works with the new `gradient` method
- Removed logging

### v0.2.7 | Bug Fixes

- Combined multiple CSS stylesheets into one:
    - `next-btn.css` -> `style.css`
    - `gradient.css` -> `style.css`
- General corrections to every file after correcting for Mypy

### v0.2.6 | Type Stubs

- Added type stubs - Mypy should work now
- Simplified `maxgradient.log.py` and fixed line lengths

### v0.2.5 | Renamed Files

- Removed erroneous `maxgradient._console.py` file
- Renamed several files:
    - `maxgradient._gc.py` -> `maxgradient._gradient_color.py`
    - `maxgradient._hex.py` -> `maxgradient._hex_color.py`
    - `maxgradient._rgb.py` -> `maxgradient._rgb_color.py`
    - `maxgradient._x11.py` -> `maxgradient._x11_color`
    - `maxgradient._rich.py` -> `maxgradient._rich_color.py`

### v0.2.4 | Converted to linting with [`ruff`](https://docs.astral.sh/ruff/)

- Rewrote `MaxGradient.console.Console` to replicate `rich.console.Console`
    - added `gradient` method
    - added `gradient_rule` method
- Switched to [`ruff`](https://docs.astral.sh/ruff/) for linting
- Pruned dependencies
- Updated default_styles.GRADIENT_STYLES

### v0.2.3

- Updated docs and added more examples and reference
- Fixed bugs
    - Fixed bug where gradient would not print if gradient was the only thing in the console
    - Fixed bug where gradient wouldn't print if the style wasn't a `rich.style.Style` object

### v0.2.2

- Added examples to docs and fixed some typos and bugs
- Disabled logging
- Fixed gradient class
- Added gradient rules

### v0.1.6

- Added docs
- Changed docs to readthedocs theme.

</body>
</html>
