---
Author: Max Ludden
Date: 2023-07-26
CSS: styles/gradient.css
---

# Gradient Reference {.gradient-header1}

<span class="rainbow-wipe">maxgradient.gradient.Gradient</span> is at the core of MaxGradient. Gradient is a subclass of <span class="green-wipe">rich.text.Text</span>, and can be used in the same way. The Gradient class however also incorporates <span class="rainbow-wipe">maxgradient.color.Color</span> which is an expanded version of <span class="green-wipe">rich.color.Color</span>. Gradient can be used to create a gradient of colors or styles. Gradient can also be used to create a rainbow effect, or to invert the colors of the gradient.

## Initialize {.gradient-header2}

<div class="class-init">
    <span class="class">class </span><span class="white-mono">Gradient</span> <span class="pink-brac">(</span><br>
    <span class="self">&nbsp;&nbsp;&nbsp;&nbsp;self</span>
    <span class="punc">,</span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;text</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">str</span><span class="pink-brac">|</span></span></span><span class="class">rich</span><span class="punc">.</span><span class="white-mono">text</span><span class="punc">.</span><span class="type">Text</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="yellow">""</span></span></span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;colors</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="white-mono">List</span><span class="purple-brac">[</span><span class="type">Color</span><span class="pink-brac">|</span><span class="type">Tuple</span><span class="pink-brac">|</span><span class="class">str</span><span class="purple-brac">]</span><span
    class="pink-brac">|</span><span class="class">str</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;rainbow</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">False</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;hues</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">int</span><span class="blue-brac">] </span><span class="pink-brac">= <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;color_sample</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">False</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;style</span><span class="punc">: </span><span class="white-mono">StyleType</span><span class="pink-brac"> = <span><span class="class">rich</span><span class="punc">.</span><span class="white-mono">text</span><span class="punc">.</span><span class="type">Style</span><span class="punc">.</span><span class="lime-text">null</span><span class="white-mono">()</span><span class="punc">, </span><br>
    <span class="pink-brac">&nbsp;&nbsp;&nbsp;&nbsp;*</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;justify</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">str</span><span class="blue-brac">] </span><span class="pink-brac">= <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;overflow</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">str</span><span class="blue-brac">] </span><span class="pink-brac">= <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;no_wrap</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">bool</span><span class="blue-brac">] </span><span class="pink-brac">= <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;end</span><span class="punc">: </span><span class="class">str</span> <span class="pink-brac">= <span><span class="yellow">"</span><span class="pink-brac">\n</span><span class="yellow">"</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;tab_size</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">int</span><span class="blue-brac">] </span><span class="pink-brac">= <span><span class="class">8</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;spans</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="white-mono">List</span><span class="purple-brac">[</span><span class="type">Span</span><span class="purple-brac">]</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span>
    <span class="pink-brac">) -> </span><span class="none">None</span><span class="punc">: </span><br>
</div>

## Parameters {.gradient-header3}

| Parameters | Description |
| :--------- | :---------- |
| text | The text to be displayed in gradient color. Can be entered as a string or as an instance of `rich.text.Text`. Defaults to an empty string. |
| colors | The colors from which to create the gradient. Can be entered as a list of: <ul><li>`maxgradient.color.Color` objects</li><li>a list of tuples containing rgb values</li><li> a list of strings containing the:<ul><li>the names of colors</li><li>hex color codes</li><li>rgb color codes</li></ul></li></ul>Defaults to None, which will result in a randomlt generated gradient. |
| rainbow | Whether or not to create a rainbow gradient. Defaults to False. |
| hues | The number of hues to use when creating a random gradient. Defaults to None, which will result in a gradient of three colors. |
| style | The style of the text. Unlike Text object where this could determine color, only styles such as bold, underline, or italic will do anything.|
| justify | The justification of the text. Can be one of: <ul><li>`left`</li><li>`center`</li><li>`right`</li></ul>Defaults to None, which will result in the text being left justified. |
| overflow | The overflow of the text. Can be one of: <ul><li>`crop`</li><li>`fold`</li><li>`ellipsis`</li></ul>Defaults to None, which will result in the text being cropped. |
| no_wrap | Whether or not to wrap the text. Defaults to None, which will result in the text being wrapped. |
| end | The string to be appended to the end of the text. Defaults to `\n`. |
| tab_size | The number of spaces to be used when a tab is encountered. Defaults to 8. |
| spans | A list of `rich.text.Span` objects. Defaults to None. |

## Methods {.gradient-header1}

### <span class="class-type">Gradient</span>.<span class="classmethod">as_text</span>()

as_text() returns the gradient as a `rich.text.Text` object.
