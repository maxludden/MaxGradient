
# <span class=rainbow-wipe>Console</span>

<span class="white">MaxGradient</span>.console.<span class="class">Console</span> is a drop in replacement for <a href="https://github.com/Textualize/rich/blob/master/rich/console.py" alt="Rich"><span class="white">rich</span>.console.<span class="class">Console</span></a> and can be used in the same way. It does, however, have some additional methods like <span class="green">gradient</span>(). You can initialize a console object with the following code:


```python
from maxgradient import Console

console = Console()
console.print("[bold lime]Hello, World![/]")
```

<figure>
    <img src="/img/console_print.svg" alt="console.print()">
</figure>

<br /><hr><br />

## New Methods

### Console.gradient()</span>

We will take an in depth look at the <span class="class">Gradient</span> class in the next section. For now, just know that any of the parameters that can be used by `MaxGradient.gradient.Gradient()` can also be used by `console.gradient()`.

Example:

```python
console.gradient(
    "This is by far the simplest way to print gradient colored text to the console.",
    colors = [
        "red",
        "orange",
        "yellow",
        "green"
    ],
    justify = "center",
    style = "bold"
)
```
<figure>
    <img src="/img/console_gradient_example.svg" alt="console.print()">
</figure>

<br ><hr><br >

### Console.gradient_rule()

<span class="class">Console</span>.<span class="green">gradient_rule</span>() expands on <span class="class">rich</span>.rule.<span class="white">Rule()</span> by allowing you to specify both the colors of the rule's gradient, as well as the rule's thickness.

#### Thin Gradient Rule

```python
from maxgradient.console import Console

console = Console()
console.gradient_rule(
    title = "Thin Gradient Rule",
    thickness = "thin"
)
```

<figure>
    <img src="/img/console_gradient_rule_thin.svg" alt="console.print()">
</figure>

<br /><hr><br />

#### Medium Gradient Rule</span>

```python
from maxgradient.console import Console

console = Console()
console.gradient_rule(
    title = "Medium Gradient Rule",
    thickness = "medium"
)
```

<figure>
    <img src="/img/console_gradient_rule_medium.svg" alt="console.print()">
</figure>

<br /><hr><br />

#### Thick Gradient Rule

```python
from maxgradient.console import Console

console = Console()
console.gradient_rule(
    title = "Thick Gradient Rule",
    thickness = "thick"
)
```

<figure>
    <img src="/img/console_gradient_rule_thick.svg" alt="console.print()">
</figure>
