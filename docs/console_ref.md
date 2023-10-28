# maxgradient.console.Console

A custom-themed high level interface for the Console class that inherits from MMoMrich.console.Console. This class is a singleton which removes the need to pass around a console object or use the `get_console` method.

## Initialize

<div class="class-init">
    <span class="class">class </span><span class="white-mono">Console</span> <span class="pink-brac">(</span><br>
    <span class="self">&nbsp;&nbsp;&nbsp;&nbsp;self</span>
    <span class="punc">,</span><br>
    <span class="pink-brac">&nbsp;&nbsp;&nbsp;&nbsp;*</span>
    <span class="punc">,</span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;color_system</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><br><span class="class">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Literal<span class="purple-brac">[</span><span class="yellow">"auto"</span>,<span class="yellow"> "standard"</span>,<span class="yellow"> "256"</span>, <span class="yellow">"truecolor"</span>,<span class="yellow"> "windows"</span><span class="purple-brac">]</span><br><span class="blue-brac">&nbsp;&nbsp;&nbsp;&nbsp;]</span><span class="pink-brac"> = <span><span class="yellow">"auto"</span></span></span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;force_terminal</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">bool</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;force_jupyter</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">bool</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;force_interactive</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">bool</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;soft_wrap</span><span class="punc">: </span><span class="type">bool</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;theme</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">Theme</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="class">GradientTheme</span><span class="white-mono">()</span></span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;stderr</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">False</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;file</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">IO</span><span class="purple-brac">[</span><span class="class">str</span><span class="purple-brac">]</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="white-mono">stdout</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;quiet</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">False</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;width</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">int</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;height</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">int</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;style</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="white-mono">StyleType</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;no_color</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">bool</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;tab_size</span><span class="punc">: </span><span class="class">int</span><span class="pink-brac"> = <span><span class="purple-brac">4</span></span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;record</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">False</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;markup</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;emoji</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;emoji_variant</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="white-mono">EmojiVariant</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;highlight</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;log_time</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;log_path</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;log_time_format</span><span class="punc">: </span><span class="class">Union</span><span class="blue-brac">[</span><span class="type">str</span>, <span class="white-mono">FormatTimeCallable</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="yellow">"</span><span class="blue-brac">[</span><span class="none">%X</span><span class="blue-brac">]</span><span class="yellow">"</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;highlighter</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="white-mono">HighlighterType</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span><span class="class">ColorReprHightlighter</span><span class="white-mono">()</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;legacy_windows</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="type">bool</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;safe_box</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;get_datetime</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">Callable</span><span class="purple-brac">[</span><span class="pink-brac">[]</span>, <span class="class">datetime</span><span class="purple-brac">]</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;get_time</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">Callable</span><span class="purple-brac">[</span><span class="pink-brac">[]</span>, <span class="type">float</span><span class="purple-brac">]</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span><span class="punc">, </span><br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;traceback</span><span class="punc">: </span><span class="class">bool</span><span class="pink-brac"> = <span><span class="none">True</span><span class="punc">,<br>
    <span class="attr">&nbsp;&nbsp;&nbsp;&nbsp;get_time</span><span class="punc">: </span><span class="class">Optional</span><span class="blue-brac">[</span><span class="class">Mapping</span><span class="purple-brac">[</span><span class="type">str</span>, <span class="type">str</span><span class="purple-brac">]</span><span class="blue-brac">]</span><span class="pink-brac"> = <span><span class="none">None</span>) -> </span><span class="none">None</span><span class="punc">: </span><br>
</div>

## Parameters

| Parameters | Description |
| :--------- | :---------- |
| color_system | The text to be displayed in gradient color. Can be entered as a string or as an instance of `rich.text.Text`. Defaults to an empty string. |
| colors | The colors from which to create the gradient. Can be entered as a list of: <ul><li>`maxgradient.color.Color` objects</li><li>a list of tuples containing rgb values</li><li> a list of strings containing the:<ul><li>the names of colors</li><li>hex color codes</li><li>rgb color codes</li></ul></li></ul>Defaults to None, which will result in a randomlt generated gradient. |
| rainbow | Whether or not to create a rainbow gradient. Defaults to False. |
| invert | Whether or not to invert the gradient colors, making the last entered color first, and the first entered color last. Defaults to False. |
| hues | The number of hues to use when creating a random gradient. Defaults to None, which will result in a gradient of three colors. |
| color_sample | Whether or not to display the text's background the same color as the text. Results in a block of color rather than text. |
| style | The style of the text. Unlike Text object where this could determine color, only styles such as bold, underline, or italic will do anything.|
| justify | The justification of the text. Can be one of: <ul><li>`left`</li><li>`center`</li><li>`right`</li></ul>Defaults to None, which will result in the text being left justified. |
| overflow | The overflow of the text. Can be one of: <ul><li>`crop`</li><li>`fold`</li><li>`ellipsis`</li></ul>Defaults to None, which will result in the text being cropped. |
| no_wrap | Whether or not to wrap the text. Defaults to None, which will result in the text being wrapped. |
| end | The string to be appended to the end of the text. Defaults to `\n`. |
| tab_size | The number of spaces to be used when a tab is encountered. Defaults to 8. |
| spans | A list of `rich.text.Span` objects. Defaults to None. |

## Methods

### <span class="class-type">Gradient</span>.<span class="classmethod">as_text</span>()

as_text() returns the gradient as a `rich.text.Text` object.
