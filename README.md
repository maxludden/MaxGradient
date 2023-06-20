<html>
<head>
    <link href="gradient.css" rel="stylesheet">
    <style>
        html {
        font-family: "Century Gothic";
        font-size: 25px;
    }
    body {
        color: #fff;
        background: #111;
    }
    table {
        margin-left: 20px
    }
    td {
        font-family: 'Century Gothic';
        padding-left: 5px;
    }
    .pdm {
        font-size: 20px;
        background: linear-gradient(to right, #ff00ff, #5f00ff);
        display: inline-block;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-decoration: none;
    }
        a:hover {
            color: #000;
        }
        a:visited {
            color: #f00;
        }
        a:active {
            color: #ff5900;
        }
        .result {
            width: 50%;
            margin: auto;
            display: block;
        }
    </style>
</head>

![MaxGradient](https://bit.ly/MaxGradient)

<h2 class="cool">MaxGradient</h2>

MaxGradient automating printing gradient colored text to the console. It's built upon the great [rich](http://rich.readthedocs.io/en/latest/) library.

<h2 class="lime-yellow">Installation</h2><br>
 MaxGradient can be installed from PyPi using your favorite package manager:
<h3 class="pdm">PDM<span class="recommended"> (Recommended)</span></h3>
<pre>
<code>
    <span class="rainbow">pdm </span><span class="light">add</span> maxgradient
</code>
</pre>

<h3 class="blue-lightblue">Pip</h3>

<pre>
<code>
pip install maxgradient
</code>
</pre>

<h2 class="warm">Usage</span>

### Basic Usage

The basic usage is to create a console object and use it to print gradient text:

<pre>
    <code>
    import maxgradient as mg

    console = mg.Console()
    console.gradient("Hello, World!")
    </code>
</pre>
<img class="result" src="Images/hello_world.svg">

<br><br><hr><br>

### Gradient

You may also instantiate a Gradient Object. The Gradient class is a subclass of the
rich.text.Text class, and can be used in the same way. The Gradient class has a
few extra arguments available though.

```python
class Gradient(rich.rich.Text):
    """Text with gradient color / style."""
    def __init__ (
        ext: Optional[str | Text] = "",
        colors: Optional[List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = Style.null(),
        *,
        # The arguments below are used directly by Text
        # so I won't cover them here. If you have questions,
        # check out the rich documentation.
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,) -> None:
```
The Gradient class can utilize the above arguments to get a plethora of different gradients. 


![MaxGradient](Images/gradient_examples.svg)

<br><br><hr><br>
## Color

The final main component of <span class="code-3">MaxGradient</span> is expanding the <span class="code-1">rich.color.Color</span> class. The <span class="code-3">MaxGradient </span>.<span class="code-1">Color</span> class can still parse and ustilize the <span class="code-1">rich.color.Color</span>'s <a href="https://rich.readthedocs.io/en/latest/appendix/colors.html" alt="Rich Standard Colors">standard colors</a> but in addition to Hex and RGB colors, it can also parse RGB Tuples as well as X11 color names. I've also included the colors that <span class="code-3">MaxGradient</span> uses to create random gradients from for convienince. The follow are the available named colors as well as there hex and rgb colors:

<img src="Images/available_colors.svg" >

<h3 class="code-2">Example</h3>
<pre>
    <code>
import maxgradient as mg

console = mg.Console()
console.print("[bold lime]This is a a vibrant green color!")
    </code>
</pre>
<img class="result" src="Images/color_example.svg">