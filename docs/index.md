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

The basic usage is to create a console object and use it to print gradient text. MaxGradient.Console is a drop in replacement for rich.rich.Console and can be used in the same way. It does, however, have some additional methods like <span class="green">gradient</span><span class="white">()</span>.

<div class="code-card">
    <h5 class="white">Quick Start Example</h5>
    <div><!--Code Block Start--><pre><code><span class="comment"># import console from MaxGradient</span>
<span class="import">import </span><span class="white">maxgradient </span><span class="import">as </span>mg

console <span class="eq">= </span>mg<span class="grey">.</span><span class="console">Console</span>()
console<span class="white">.</span><span class="green">gradient</span>(<span class="yellow">"Hello, World!"</span>)
</code></pre>

<!--Code Block End-->
</div>

<!--Code Block Start
<pre><code><span class="code-title">Quick Start Example</span>
<span class="comment"># import console from MaxGradient</span>
<span class="import">import </span>maxgradient <span class="import">as </span>mg

console <span class="eq">= </span>mg<span class="grey">.</span><span class="console">Console</span>()
console<span class="white">.</span><span class="green">gradient</span>(<span class="yellow">"Hello, World!"</span>)
</code></pre>
Code Block End-->

<!--Caption Start-->
<figure>
    <!--<figcaption>Produces the following:</figcaption>-->
    <img src="img/hello_world.svg" alt="Hello, World!">
</figure>
<!--Caption End-->

<h2><span class="cool-wipe">Gradient with Color</span></h2>

<p>MaxGradient easily make random gradients that require no more than the text you wish to color, it can also be used to make gradients with specific colors. The <span class="green">gradient</span><span class="white">()</span> method takes a string of text as well as a list of colors. The number of colors in the list determines the number of colors in the gradient. The gradient will be evenly distributed between the colors in the list. The gradient will be applied to the text in the order it is given in the list.</p>

<p>MaxGradient accepts the following as </p>
<ul>
    <li>color names</li>
    <li>hex color codes</li>
    <li>rgb color codes</li>
    <li>X11 named colors</li>
    <li>as well as any colors from rich's standard library.</li>
</ul>

<p>Let's take a look at some examples:</p>

<!--Code Block Start | 1 -->
<h5 class="white">Example 1</h5>
<pre><code><span class="comment"># While MaxGradient has a multiple modules including a Gradient</span>
<span class="comment"># module, the main modules may all be imported directly from maxgradient.</span>
<span class="import">import </span>maxgradient <span class="import">as </span>mg

console <span class="eq">= </span>mg<span class="grey">.</span><span class="class">Console</span>()<span class="comment"> # Initialize a console</span>

<span class="comment"># Use the Console's gradient function</span>
console<span class="white">.</span><span class="green">gradient</span>(
<span class="yellow">    "This gradient contains the colors: magenta, violet, and purple."</span>,
<span style="color:#FCB56B;">    colors</span> <span><span class="eq">= [</span>
<span class="yellow">        "magenta"</span>,
<span class="yellow">        "violet"</span>,
<span class="yellow">        "purple"</span>
<span class="eq">    ]</span>
)
</code></pre>

<!--Code Block End | 1 -->

<!--Result | 1 -->
<figure>
    <img src="img/gradient_with_color_1.svg" alt="Hello, World!">
</figure>
<!--Result | 1 -->

<br /><hr><br />

<!--Code Block Start | 2 -->
<h5 class="white">Example 2</h5>
<pre><code>
console<span class="white">.</span><span class="green">gradient</span>(
    <span class="yellow">"This gradient contains the colors: magenta, violet, purple,</span><span class="keyword">\</span>
<span class="yellow">blue, lightblue, and cyan."</span>
    <span style="color:#FCB56B;">colors</span> <span><span class="eq">= [</span>
        <span class="yellow">"rgb(255,0,255)",</span>
        <span class="yellow">"violet",</span>
        <span class="yellow">"#5f00ff",</span>
        <span class="yellow">"blue",</span>
        <span class="yellow">"rgb(0, 136, 255)",</span>
        <span class="yellow">"cyan"</span>
    <span class="eq">]</span><span class="white">,</span>
    <span style="color:#FCB56B;">justify </span><span class="eq">= </span><span class="yellow">"center"</span><span class="white">,</span>
    <span style="color:#FCB56B;">style </span><span class="eq">= </span><span class="yellow">"bold"</span>
)
</code></pre>

<!--Code Block End | 2 -->

<!--Result Start | 2 -->
<figure>
    <img src="img/gradient_with_color_2.svg" alt="Hello, World!">
</figure>
<!--Result End | 2 -->

<br /><hr><br />

<div class="row ">
