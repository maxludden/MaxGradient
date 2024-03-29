# <span class="rainbow-wipe">MaxGradient.Color</span>

Color extends the [Rich.color.Color](https://github.com/Textualize/rich/blob/master/rich/color.py) class to allow colors to be parsed from:

- [X11](https://www.w3schools.com/colors/colors_x11.asp) color names (over 200 colors)
- Rich's [Standard Color Library](https://rich.readthedocs.io/en/latest/appendix/colors.html)
- Hex codes (3-digit and 6-digit)
- RGB values (with or without the 'rgb' prefix)

A color can be represented as a string in numerous ways. The easiest is the name of the color:

- <span class="red">red</span>
- <span class="magenta">magenta</span>
- <span class="blue">blue</span>

You can also use the hex code of the color:

- <span class="red">#ff0000</span> (six digit hex code)
- <span class="magenta">#F0F</span> (three digit hex code)

Or the RGB Color Code/ColorTriplet of the color:

- <span class="light-green">rgb(170,255,170)</span> (with `rgb` prefix)
- <span style="color:#0f0;">(0, 255, 0)</span> (`rgb` tuple without prefix)

In addition to common names, MaxGradient also supports the entire rich color standard color palette. But we didn't stop there, in addition to rich's standard library, MaxGradient also supports the entire X11 color palette. That's over 200 colors!

## Example 1: <span style="color:#ff0000;">Color("red")</span>

```python
from maxgradient import Color, Console

console = Console()
console.print(
    Color("red"),
    justify="center"
)
```

![Color('red')](img/color_red.svg)

## Example 2: <span style="color:#AAFFAA;"> Color("#AAFFAA") </span>

```python
console.print(
    Color("#aaffaa"),
    justify = "center"
)
```

![Color('#AAFFAA')](img/color_aaffaa.svg)

## Example 3: <span style="color:darkOrchid;">Color("DarkOrchid")</span>

```python
console.print(
    Color("DarkOrchid"),
    justify = "center"
)
```

![Color('DarkOrchid')](img/color_darkorchid.svg)

<!-- 
## Possible Colors

To view all of the available colors run the following command in the console:

```shell
python -m maxgradient.color
```

![Gradients are cool!](img/available_colors.svg) -->
