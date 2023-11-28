<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <picture>
            <source srcset="img/maxgradient_banner.svg" media="(min-width: 800px)">
            <source srcset="img/maxgradient_banner_sq.svg" media="(min-width: 600px)">
            <img src="img/maxGradient.svg" alt="MaxGradient" style="width:auto;">
        </picture>
        <div id="spacer"></div>
        <div class="badges">
            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Python-3.9 | 3.10 | 3.11 | 3.12 -blue?logo=python" alt="PyPI - MaxGradient"></a>
            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/PyPI-MaxGradient-blue?" alt="PyPI - MaxGradient"></a>
            <a href="https://GitHub.com/maxludden/maxgradient"><img  class="badge" src="https://img.shields.io/badge/Version-0.2.11-bbbbbb" alt="Version 0.2.11"></a>
            <a href="https://pdm.fming.dev/"><img class="badge" src="https://camo.githubusercontent.com/acf0526fc1f541f9d980d7983ff5ab8e540cf2136206c2b5dc740f658a37fac0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f70646d2d6d616e616765642d626c756576696f6c6574"></a>
        </div>
        <div id="spacer"></div>
        <div class="gradient-border" id="box">
            <div id="title">MaxGradient</div>
            <p>MaxGradient automates printing gradient colored text to the console. It's built upon the great <a href="https://github.com/Textualize/rich" title="GitHub.com/textualize/rich">rich library</a>. It contains a Console that can serve as a drop in replacement for <a href="https://github.com/Textualize/rich/blob/master/rich/console.py">rich.console.Console</a> and has an expanded Color class which can parse X11 color names on top of rich's standard colors. MaxGradient is a work in progress and I'm open to any suggestions or contributions.</p>
        </div>
        <div id="spacer"></div>

<h1 class="rainbow-wipe">Installation</h1>

MaxGradient can be installed from PyPi using your favorite python package manager:

<h2><span class="pdm-recommended">PDM (Recommended)</span></h2>

```shell
pdm add maxgradient
```

<h2><span class="pdm-wipe">PIP</span></h2>

```shell
pip install maxgradient
```

<hr>

<h1 class=rainbow-wipe>Usage</h1>

<h2><span class="pdm-wipe">Quick Start</span></h2>

The basic usage is to create a console object and use it to print gradient text. MaxGradient.Console is a drop in replacement for rich.rich.Console and can be used in the same way. It does, however, have some additional methods like <span class="animatedtitle"> gradient</span><span class="white">()</span>.

<h2 class="pdm-wipe">Example</h2>

```python
#import console from MaxGradient
import maxgradient as mg

console = mg.Console() # Initialize a console
console.gradient(
    "Hello, World!",
    justify = "center"
)
```

<img src="img/hello_world.svg" alt="Hello, World!" style="width:100%;">

<h2><span class="cool-wipe">Gradient with Color</span></h2>

<p>MaxGradient easily make random gradients that require no more than the text you wish to color, it can also be used to make gradients with specific colors. The <span class="green">gradient</span><span class="white">()</span> method takes a string of text as well as a list of colors. The number of colors in the list determines the number of colors in the gradient. The gradient will be evenly distributed between the colors in the list. The gradient will be applied to the text in the order it is given in the list.</p>

<p>MaxGradient accepts the following as </p>
<ul>
    <li>color names (<span style="color:#ff0000">red</span>, <span style="color:#ff8800;">orange</span>, <span style="color:#ffff00;">yellow</span>, <span style="color:#0f0;">green</span>, <span style="color:#0ff;">cyan</span>, <span style="color: #08f;">lightblue</span>, <span style="color:#00f;">blue</span>, <span style="color:#5f00ff;">purple</span>, <span style="color:#af00ff;">violet</span>, <span style="color:#f0f;">magenta</span>)</li>
    <li>hex color codes (3-digit -> <span style="color:#f0f;">#f0f</span>, 6-digit -> <span style="color:#f0f;">#ff00ff</span>)</li>
    <li>rgb color codes</li>
    <li>X11 named colors</li>
    <li>as well as any colors from rich's standard library.</li>
</ul>
<p>Let's take a look at some examples:</p>
<h3><span class="pdm">Example 1</span>

```python
import maxgradient as mg

console = mg.Console() # Initialize a console
console.gradient(
    "This gradient contains the colors: magenta, violet, and purple.",
    colors = [
        "magenta",
        "violet",
        "purple"
    ])
```

<img src="img/gradient_with_color_1.svg" alt="Gradient with Color 1" style="width:100%;">
<br /><hr><br />
<h3><span class="pdm">Example 2</span></h3>

You are not just stuck with ROY G BIV colors, you can use any colors you want. Let's make a gradient with the colors: magenta, violet, purple, blue, lightblue, and cyan.

```python
console.gradient(
    "This gradient contains the colors: magenta, violet, purple, blue, lightblue, and cyan.",
    colors = [
        "rgb(255,0,255)", # rgb | magenta
        "violet", # named
        "#5f00ff", # hex | purple
        "blue", # another named
        "rgb(0, 136, 255)", # rgb | lightblue
        "cyan" # and another
    ]
)
```

<hr>
<div class="verticle_spacer"></div>
<img src="img/gradient_with_color_2.svg" alt="Gradient with Color 2" style="width:100%;">
<hr>
<div style="margin:auto; text-align:center;">
    <span style="font-size:1.5em; vertical-align:middle;">Created by<br />
    <img src="https://user-images.githubusercontent.com/51646468/284406500-dff29293-4afb-40a5-8e1a-275108898845.svg" alt="Max Ludden's Logo" style="width:25%; margin:auto; padding:20px;"><br /> Max Ludden</span>
</div>
<hr>
<h2>Changelog</h2>
<h3><span class="version">v</span>0.2.11 | <span style="color:#aaff00;">November 28, 2023</span> | Added Tests</h3>
    <ul>
        <li>Removed color_sample and invert from gradient attributes</li>
        <li>Added tests for console, color, and gradient</li>
    </ul>
<h3><span class="version">v</span>3.2.10 | <span style="color:#aaff00;">November 25, 2023</span> | Added Dates</h3>
    <ul>
        <li>Updated changlog to have dates</li>
    </ul>

<h3><span class="version">v</span>0.2.9 | <span style="color:#aaff00;">November 25, 2023</span> | Updated Banner</h3>
    <ul>
        <li>Updated MaxGradient Logo and Favicon</li>
        <li>Updated banner to include new logo as http rather than refernceing the svg file locally.</li>
    </ul>
<h3><span class="version">v</span>0.2.8 | <span style="color:#aaff00;">November 25, 2023</span> | Fixed `cli.py`</h3>
    <ul>
        <li>Fixed `cli.py` so that it works with the new `gradient` method</li>
        <li>Removed logging</li>
    </ul>
<h3><span class="version">v</span>0.2.7 | <span style="color:#aaff00;">November 25, 2023</span> | Bug Fixes</h3>
    <ul>
        <li>Combined multiple CSS stylesheets into one:
            <ul>
                <li>`next-btn.css` -> `style.css`</li>
                <li>`gradient.css` -> `style.css`</li>
            </ul>
        </li>
        <li>General corrections to every file after correcting for Mypy</li>
    </ul>
<h3><span class="version">v</span>0.2.6 | <span style="color:#aaff00;">November 18, 2023</span> | Type Stubs</h3>
    <ul>
        <li>Added type stubs - Mypy should work now</li>
        <li>Simplified `maxgradient.log.py` and fixed line lengths</li>
    </ul>
<h3><span class="version">v</span>0.2.4</h3>
    <ul>
        <li>Rewrote `MaxGradient.console.Console` to replicate `rich.console.Console`
            <ul>
                <li>added `gradient` method</li>
                <li>added `gradient_rule` method</li>
            </ul>
        </li>
        <li>Switched to <a href="https://docs.astral.sh/ruff/" title="rich">rich</a> for linting</li>
        <li>Pruned dependencies</li>
        <li>Updated default_styles.GRADIENT_STYLES</li>
<h3><span class="version">v</span>0.2.3</h3>
    <ul>
        <li>Updated docs and added more examples and reference</li>
        <li>Fixed bugs:
            <ul>
                <li>Fixed bug where gradient would not print if gradient was the only thing in the console</li>
                <li>Fixed bug where gradient wouldn't print if the style wasn't a `rich.style.Style` object</li>
            </ul>
        </li>
    </ul>
<h3><span class="version">v</span>0.2.2</h3>
<ul>
    <li>Added examples to docs and fixed some typos and bugs</li>
    <li>Disabled logging</li>
    <li>Fixed gradient class</li>
    <li>Added gradient rules</li>
