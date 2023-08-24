<!--<img src="img/maxgradient_banner.png" class="banner" alt="MaxGradient Banner">-->

MaxGradient automates the printing gradient colored text to the console. It's built upon the great rich library. It contains a Console that can serve as a drop in replacement for rich.rich.Console and has an expanded Color class which can parse X11 color names on top of rich's standard colors. MaxGradient is a work in progress and I'm open to any suggestions or contributions.

# <span class="rainbow-wipe">Installation</span>

MaxGradient can be installed from PyPi using your favorite python package manager:

## <span class="pdm-wipe">PDM</span> (Recommended)

<pre><code>pdm<span class="keyword"> add </span>maxgradient</code></pre>

## PIP

```shell
pip install maxgradient
```

# <span class="rainbow-wipe">Usage</span>

## Quick Start

The basic usage is to create a console object and use it to print gradient text. MaxGradient Console is a drop in replacement for rich.rich.Console and can be used in the same way. It does, however, have some additional methods like <span class="green">gradient</span><span class="white">()</span>.

<pre><code><span class="comment"># import console from MaxGradient</span>
<span class="import">import </span>maxgradient <span class="import">as </span>mg

console <span class="eq">= </span>mg<span class="grey">.</span><span class="console">Console</span>()
console<span class="white">.</span><span class="green">gradient</span>(<span class="yellow">"Hello, World!"</span>)
</code></pre>

<figure>
    <figcaption class="twotwelve">Produces the following:</figcaption>
    <img class="result" src="img/hello_world.svg" alt="Hello, World!">
</em>
