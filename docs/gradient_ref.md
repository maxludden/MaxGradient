---
Author: Max Ludden
Date: 2023-07-26
CSS: styles/gradient.css
---

# <span class="cool-wipe-header">Gradient Reference</span>

<span class="rainbow-wipe">maxgradient.gradient.Gradient</span> is at the core of MaxGradient. Gradient is a subclass of <span class="green-wipe">rich.text.Text</span>, and can be used in the same way. The Gradient class however also incorporates <span class="rainbow-wipe">maxgradient.color.Color</span> which is an expanded version of <span class="green-wipe">rich.color.Color</span>. Gradient can be used to create a gradient of colors or styles. Gradient can also be used to create a rainbow effect, or to invert the colors of the gradient.

```python
class Gradient(rich.text.Text):
    """Text with gradient color / style."""

    def __init__ (
        text: Optional[str | Text] = "",
        colors: Optional[str|List[Color | Tuple | str]] = None,
        rainbow: bool = False,
        invert: bool = False,
        hues: Optional[int] = None,
        color_sample: bool = False,
        style: StyleType = Style.null(),
        *,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: Optional[List[Span]] = None,) -> None:
```
