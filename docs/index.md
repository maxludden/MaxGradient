<!--<img src="img/maxgradient_banner.png" class="banner" alt="MaxGradient Banner">-->

MaxGradient automates the printing gradient colored text to the console. It's built upon the great rich library. It contains a Console that can serve as a drop in replacement for rich.rich.Console and has an expanded Color class which can parse X11 color names on top of rich's standard colors. MaxGradient is a work in progress and I'm open to any suggestions or contributions.

# <span class="rainbow-wipe">Installation</span>

MaxGradient can be installed from PyPi using your favorite python package manager:

## <span class="cool-wipe">PDM (Recommended)</span>

<pre><code>pdm<span class="keyword"> add </span>maxgradient</code></pre>

## <span class="cool-wipe">PIP</span>

<pre><code>pip<span class="keyword"> install </span>maxgradient</code></pre>

# <span class="rainbow-wipe">Usage</span>

## <span class="cool-wipe">Quick Start</span>

The basic usage is to create a console object and use it to print gradient text. MaxGradient Console is a drop in replacement for rich.rich.Console and can be used in the same way. It does, however, have some additional methods like <span class="green">gradient</span><span class="white">()</span>.

<pre><code><span class="comment"># import console from MaxGradient</span>
<span class="import">import </span>maxgradient <span class="import">as </span>mg

console <span class="eq">= </span>mg<span class="grey">.</span><span class="console">Console</span>()
console<span class="white">.</span><span class="green">gradient</span>(<span class="yellow">"Hello, World!"</span>)
</code></pre>

<figure>
    <figcaption class="twotwelve">Produces the following:</figcaption>
    <img class="result" src="img/hello_world.svg" alt="Hello, World!">
</figure>

## <span class="cool-wipe">Gradient with Color</span>

<p>MaxGradient easily make random gradients that require no more than the text you wish to color, it can also be used to make gradients with specific colors. The <span class="green">gradient</span><span class="white">()</span> method takes a string of text as well as a list of colors. The number of colors in the list determines the number of colors in the gradient. The gradient will be evenly distributed between the colors in the list. The gradient will be applied to the text in the order it is given in the list.</p>

<p>We'll talk a low level look at <span class="warm-wipe">MaxGradient</span><span class="white">.color.</span><span class="class">Color</span> but you can use:</p>
<ul>
    <li>color names</li>
    <li>hex color codes</li>
    <li>rgb color codes</li>
    <li>X11 named colors</li>
    <li>as well as any colors from rich's standard library.</li>
</ul>