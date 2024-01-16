# MaxGradient.color.Color Reference

A class to represent a color that inherits and expands `rich.rich.Color`
to include X11 named colors as well as multiple formats of hex and rgb colors.

## Initialize

<div class="class-init">
    <span class="class">class </span><span class="white-mono">Color</span> <span class="pink-brac">(</span><span class="self">self</span><span class="punc">, </span><span class="attr">color</span><span class="punc">: </span><span class="class">Any</span><span class="pink-brac">) -> </span><span class="none">None</span><span class="punc">: </span><br>
</div>

## Parameters

| Name  | Type | Description                  |
| :---- | :--- | :--------------------------- |
| color | Union[[str](https://docs.python.org/3/library/stdtypes.html#str), [tuple](https://docs.python.org/3/library/stdtypes.html#tuple), Color]  | The color to be represented.<br>The color may be:<ul><li>the color name<ul><li>color names (<span style="color:#ff0000">red</span>, <span style="color:#ff8800;">orange</span>, <span style="color:#ffff00;">yellow</span>, <span style="color:#0f0;">green</span>, <span style="color:#0ff;">cyan</span>, <span style="color: #08f;">lightblue</span>, <span style="color:#00f;">blue</span>, <span style="color:#5f00ff;">purple</span>, <span style="color:#af00ff;">violet</span>, <span style="color:#f0f;">magenta</span>)</li><li>hex color codes (3-digit -> <span style="color:#f0f;">#f0f</span>, 6-digit -> <span style="color:#f0f;">#ff00ff</span>)</li><li>rgb color codes</li><li>X11 named colors</li><li>as well as any colors from rich's standard library.</li></ul></li><li>the hex color code</li><li>the rgb color code</li><li>the rgb color tuple</li><li>a `maxgradient.color.Color` object</li>|

## Attributes

| Name | Type | Description |
| :--- | :--- | :---------- |
| original | [str](https://docs.python.org/3/library/stdtypes.html#str) | The original color passed to the constructor. |
| red | [int](https://docs.python.org/3/library/functions.html#int) | The red value of the color. |
| green | [int](https://docs.python.org/3/library/functions.html#int) | The green value of the color. |
| blue | [int](https://docs.python.org/3/library/functions.html#int) | The blue value of the color. |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) | The name of the color. If the color is not a named color, this will default to the hex color code. |
| hex | [str](https://docs.python.org/3/library/stdtypes.html#str) | The hex color code of the color. |
| rgb |  [str](https://docs.python.org/3/library/stdtypes.html#str) | The rgb color code of the color. |
| triplet | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple) | The rgb color tuple of the color. |
| style | [rich.style.Style](https://rich.readthedocs.io/en/latest/style.html#style-class) | A style object with the color as the foreground color. |
| bg_style | [rich.style.Style](https://rich.readthedocs.io/en/latest/style.html#style-class) | A style object with the color as the background color. |

## Methods

- <span class="classmethod">get_contrast</span><span class="white-mono">(</span><span class="self">self</span><span class="white-mono">) -> <span class="attr">str</span><span class="punc">:</span>

&nbsp;&nbsp;&nbsp;&nbsp;<em>Generate the color of the foreground if the color is the background. Ie. lighter colors with return black, and darker colors will return white.</em>

- <span class="classmethod">lighten</span><span class="white-mono">(</span><span class="self">self</span><span class="punc">, </span><span class="attr">percent</span><span class="white-mono">: </span><span class="class">float</span><span class="white-mono"> = </span><span class="basic-type">0.5</span><span class="white-mono">) -> </span><span class="attr">str</span><span class="punc">:</span>

&nbsp;&nbsp;&nbsp;&nbsp;<em>Generate a tint of the color.</em>
   <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - percent (<a href="https://docs.python.org/3/library/functions.html#float" alt="float">float</a>): The amount of white to add to the color.</li>
</ul>

- <span class="classmethod">darken</span><span class="white-mono">(</span><span class="self">self</span><span class="punc">, </span><span class="attr">percent</span><span class="white-mono">: </span><span class="class">float</span><span class="white-mono"> = </span><span class="basic-type">0.5</span><span class="white-mono">) -> </span><span class="attr">str</span><span class="punc">:</span>

&nbsp;&nbsp;&nbsp;&nbsp;<em>Generate a tint of the color.</em><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- percent (<a href="https://docs.python.org/3/library/functions.html#float" alt="float">float</a>): The amount of black to add to the color.</li>
</ul>
