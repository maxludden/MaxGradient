<h1 class=rainbow-wipe>Console</h1>

<span class="white">MaxGradient</span>.console.<span class="class">Console</span> is a drop in replacement for <span class="white">rich</span>.console.<span class="class">Console</span> and can be used in the same way. It does, however, have some additional methods like <span class="green">gradient</span>(). You can initialize a console object with the following code:

<!--Code Block Start-->
<pre><code><span class="comment"># import console from MaxGradient</span>
<span class="import">from </span><span class="white">maxgradient.console </span><span class="import">import </span><span class="class">Console</span>

<span class="comment"># initialize console</span>
<span class="white">console </span><span class="eq">= </span><span class="class">Console</span>()

<span class="comment"># print any rich renderable</span>
<span class="white">console</span><span class="eq">.</span><span class="green">print</span>(<span class="yellow">"[bold lime]Hello, World![/]"</span>)</code></pre>
<figure>
    <img src="img/console_print.svg" alt="console.print([bold #00ff00]Hello, World![/]">