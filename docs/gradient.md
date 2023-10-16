# <span class="rainbow-wipe">MaxGradient.Gradient</span>

Maxgradient.gradient.Gradient is a subclass of [rich.text.Text](https://github.com/Textualize/rich/blob/master/rich/text.py), and can be used in the same way. If a gradient is made with just a string, the gradient will automatically generate colors for you. If that's not colorful enough for you, you can pass the rainbow argument to the gradient to generate a rainbow gradient.

If you need more control over the gradient, you can pass a list of colors to the gradient. The gradient will be evenly distributed between the colors in the list. The gradient will be applied to the text in the order it is given in the list.

## Example 1: Random Gradient

![Random Gradient Example](img/random_gradient.svg)

## Example 2: Rainbow Gradient

![Rainbow Gradient Example](img/rainbow_gradient.svg)

## Example 3: Gradient with Specified Colors

![Gradient with Specified Colors Example](img/red_orange_yellow_gradient.svg)
