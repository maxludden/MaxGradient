# Console

<dl class="py class">
    <dt class="sig sig-object py" id="maxgradient.console.Console">
        <em class="property">
            <span class="pre">class</span>
            <span class="w"> </span>
        </em>
        <span class="sig-prename descclassname"><span class="pre">maxgradient.console.</span></span><span class="sig-name descname"><span class="pre">Console</span></span>
        <span class="sig-paren">(</span>
        <em class="sig-param">
            <span class="n">
                <span class="pre">*</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">color_system='auto'</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">force_terminal=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">force_jupyter=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">force_interactive=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">soft_wrap=False</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">theme=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">stderr=False</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">file=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">quiet=False</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">width=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">height=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">style=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">no_color=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">tab_size=4</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">record=False</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">markup=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">emoji=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">emoji_variant=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">highlight=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">log_time=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">log_path=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">log_time_format='[%X]'</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">highlighter=None()</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">legacy_windows=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">safe_box=True</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">get_datetime=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">get_time=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">traceback=None</span>
            </span>
        </em>, <em class="sig-param">
            <span class="n">
                <span class="pre">_environ=None</span>
            </span>
        </em>
        <span class="sig-paren">)</span>
            <a class="reference internal" href="../_modules/rich/console.html#Console">
                <span class="viewcode-link">
                    <span class="pre">[source]</span>
                </span>
            </a><a class="headerlink" href="#rich.console.Console" title="Permalink to this definition">¶</a></dt>
<dd><p>A custom-themed high level interface for the Console class that inherits from rich.console.Console. This class is a singleton which removes the need to pass around a console object or use the `get_console` method.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd">
    <ul class="simple">
        <li><p><strong>color_system</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – 
        The color system supported by your terminal. Valid values are:
            <ul>
                <li><code class="docutils literal notranslate"><span class="pre">"auto",</span></code></li>
                <li><code class="docutils literal notranslate"><span class="pre">"standard",</span></code></li>
                <li><code class="docutils literal notranslate"><span class="pre">"256",</span></code></li>
                <li><code class="docutils literal notranslate"><span class="pre">"truecolor",</span></code></li>
            </ul>
        <div>Leave as <pre style="display:inline;">"auto"</pre> to autodetect.</em></p>
        </li><li>
            <p>
                <strong>force_terminal</strong>
                    (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em>
                    <em>, </em>
                    <em>optional</em>) – Enable/disable terminal control codes, or None to auto-detect terminal. Defaults to None.
            </p>
        </li><li>
            <p>
                <strong>force_jupyter</strong>
                    (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable/disable Jupyter rendering, or None to auto-detect Jupyter. Defaults to None.
            </p>
        </li><li>
            <p>
                <strong>force_interactive</strong>
                    (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable/disable interactive mode, or None to auto detect. Defaults to None.
            </p>
        </li><li>
            <p>
                <strong>soft_wrap</strong>
                    (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Set soft wrap default on print method. Defaults to False.
            </p>
        </li><li>
            <p>
                <strong>theme</strong>
                    (<a class="reference internal" href="theme.html#maxgradient.theme.Theme" title="rich.theme.Theme"><em>Theme</em></a><em>, </em><em>optional</em>) – An optional style theme object, or <code class="docutils literal notranslate"><span class="pre">None</span></code> for default theme, GradientTheme()
            </p>
        <li><li>
            <p>
                <strong>stderr</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Use stderr rather than stdout if `file`</span></code> is not specified. Defaults to False.
            </p>
        </li><li>
            <p>
                <strong>file</strong>
                    (<em>IO</em><em>, </em><em>optional</em>) – A file object where the console should write to. Defaults to stdout.
            </p>
        </li><li>
            <p>
                <strong>quiet</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>Optional</em>) – Boolean to suppress all output. Defaults to False.
            </p>
        </li><li>
            <p>
                <strong>width</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – The width of the terminal. Leave as default to auto-detect width.
            </p>
        </li><li>
            <p>
                <strong>height</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – The height of the terminal. Leave as default to auto-detect height.
            </p>
        </li><li>
            <p>
                <strong>style</strong>
                    (<em>StyleType</em><em>, </em><em>optional</em>) – Style to apply to all output, or None for no style. Defaults to None.
            </p>
        </li><li>
            <p>
                <strong>no_color</strong>
                    (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enabled no color mode, or None to auto detect. Defaults to None.
                    </p>
        </li><li>
            <p>
                <strong>tab_size</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – Number of spaces used to replace a tab character. Defaults to 4.</p>
        </li><li>
            <p>
                <strong>record</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Boolean to enable recording of terminal output, required to call <a class="reference internal" href="#maxgradient.console.Console.export_html" title="maxgradient.console.Console.export_html">export_html()</a>, <a class="reference internal" href="#rich.console.Console.export_svg" title="rich.console.Console.export_svg">export_svg()</a>, and <a class="reference internal" href="#rich.console.Console.export_text" title="rich.console.Console.export_text">export_text()</a>. Defaults to False.</p>
        </li><li>
            <p>
                <strong>markup</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Boolean to enable <a class="reference internal" href="../markup.html#console-markup"><span class="std std-ref">Console Markup</span></a>. Defaults to True.</p>
        </li><li>
            <p>
                <strong>emoji</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable emoji code. Defaults to True.</p>
        </li><li>
            <p>
                <strong>emoji_variant</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Optional emoji variant, either “text” or “emoji”. Defaults to None.</p>
        </li><li>
            <p>
                <strong>highlight</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable automatic highlighting. Defaults to True.</p>
        </li><li>
            <p>
                <strong>log_time</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Boolean to enable logging of time by <a class="reference internal" href="#rich.console.Console.log" title="rich.console.Console.log">log()</a> methods. Defaults to True.</p>
        </li><li>
            <p>
                <strong>log_path</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Boolean to enable the logging of the caller by <a class="reference internal" href="#rich.console.Console.log" title="rich.console.Console.log">log()</a>. Defaults to True.</p>
        </li><li>
            <p>
                <strong>log_time_format</strong>
                    (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>TimeFormatterCallable</em><em>]</em><em>, </em><em>optional</em>) – If <span class="pre">`log_time`</span> is enabled, either string for strftime or callable that formats the time. Defaults to “[%X] “.</p>
        </li><li>
            <p>
                <strong>highlighter</strong>
                    (<em>HighlighterType</em><em>, </em><em>optional</em>) – Default highlighter.</p>
        </li><li>
            <p>
                <strong>legacy_windows</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable legacy Windows mode, or `None` to auto detect. Defaults to `None`.</p>
        </li><li>
            <p>
                <strong>safe_box</strong>
                    (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Restrict box options that don’t render on legacy Windows.</p>
        </li><li>
            <p>
                <strong>get_datetime</strong> (<em>Callable</em><em>[</em><em>[</em><em>]</em><em>, </em><em>datetime</em><em>]</em><em>, </em><em>optional</em>) – Callable that gets the current time as a datetime.datetime object (used by Console.log), or None for datetime.now.</p>
        </li><li>
            <p>
                <strong>get_time</strong> (<em>Callable</em><em>[</em><em>[</em><em>]</em><em>, </em><em>time</em><em>]</em><em>, </em><em>optional</em>) – Callable that gets the current time in seconds, default uses time.monotonic.</p>
        </li><li>
            <p>
                <strong>_environ</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Mapping" title="(in Python v3.11)"><em>Mapping</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p>
        </li>
    </ul>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.begin_capture">
<span class="sig-name descname"><span class="pre">begin_capture</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.begin_capture"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.begin_capture" title="Permalink to this definition">¶</a></dt>
<dd><p>Begin capturing console output. Call <a class="reference internal" href="#rich.console.Console.end_capture" title="rich.console.Console.end_capture"><code class="xref py py-meth docutils literal notranslate"><span class="pre">end_capture()</span></code></a> to exit capture mode and return output.</p>
<dl class="field-list simple">
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.bell">
<span class="sig-name descname"><span class="pre">bell</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.bell"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.bell" title="Permalink to this definition">¶</a></dt>
<dd><p>Play a ‘bell’ sound (if supported by the terminal).</p>
<dl class="field-list simple">
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.capture">
<span class="sig-name descname"><span class="pre">capture</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.capture"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.capture" title="Permalink to this definition">¶</a></dt>
<dd><p>A context manager to <em>capture</em> the result of print() or log() in a string,
rather than writing it to the console.</p>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre id="codecell0"><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">rich.console</span> <span class="kn">import</span> <span class="n">Console</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">console</span> <span class="o">=</span> <span class="n">Console</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="n">console</span><span class="o">.</span><span class="n">capture</span><span class="p">()</span> <span class="k">as</span> <span class="n">capture</span><span class="p">:</span>
<span class="gp">... </span>    <span class="n">console</span><span class="o">.</span><span class="n">print</span><span class="p">(</span><span class="s2">"[bold magenta]Hello World[/]"</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="nb">print</span><span class="p">(</span><span class="n">capture</span><span class="o">.</span><span class="n">get</span><span class="p">())</span>
</pre><button class="copybtn o-tooltip--left" data-tooltip="Copy" data-clipboard-target="#codecell0">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-copy" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <title>Copy to clipboard</title>
  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
  <rect x="8" y="8" width="12" height="12" rx="2"></rect>
  <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2"></path>
</svg>
    </button></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>Context manager with disables writing to the terminal.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#rich.console.Capture" title="rich.console.Capture">Capture</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.clear">
<span class="sig-name descname"><span class="pre">clear</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">home</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.clear"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.clear" title="Permalink to this definition">¶</a></dt>
<dd><p>Clear the screen.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>home</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Also move the cursor to ‘home’ position. Defaults to True.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.clear_live">
<span class="sig-name descname"><span class="pre">clear_live</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.clear_live"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.clear_live" title="Permalink to this definition">¶</a></dt>
<dd><p>Clear the Live instance.</p>
<dl class="field-list simple">
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.color_system">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">color_system</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><span class="pre">Optional</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></em><a class="headerlink" href="#rich.console.Console.color_system" title="Permalink to this definition">¶</a></dt>
<dd><p>Get color system string.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>“standard”, “256” or “truecolor”.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>Optional[<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a>]</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.control">
<span class="sig-name descname"><span class="pre">control</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">control</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.control"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.control" title="Permalink to this definition">¶</a></dt>
<dd><p>Insert non-printing control codes.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>control_codes</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – Control codes, such as those that may move the cursor.</p></li>
<li><p><strong>control</strong> (<em>Control</em>) – </p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.encoding">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">encoding</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><span class="pre">str</span></a></em><a class="headerlink" href="#rich.console.Console.encoding" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the encoding of the console file, e.g. <code class="docutils literal notranslate"><span class="pre">"utf-8"</span></code>.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>A standard encoding string.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.end_capture">
<span class="sig-name descname"><span class="pre">end_capture</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.end_capture"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.end_capture" title="Permalink to this definition">¶</a></dt>
<dd><p>End capture mode and return captured string.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>Console output.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.export_html">
<span class="sig-name descname"><span class="pre">export_html</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">theme</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">code_format</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">inline_styles</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.export_html"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.export_html" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate HTML from console contents (requires record=True argument in constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>theme</strong> (<em>TerminalTheme</em><em>, </em><em>optional</em>) – TerminalTheme object containing console colors.</p></li>
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>code_format</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Format string to render HTML. In addition to ‘{foreground}’,
‘{background}’, and ‘{code}’, should contain ‘{stylesheet}’ if inline_styles is <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p></li>
<li><p><strong>inline_styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – If <code class="docutils literal notranslate"><span class="pre">True</span></code> styles will be inlined in to spans, which makes files
larger but easier to cut and paste markup. If <code class="docutils literal notranslate"><span class="pre">False</span></code>, styles will be embedded in a style tag.
Defaults to False.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>String containing console contents as HTML.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.export_svg">
<span class="sig-name descname"><span class="pre">export_svg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'Rich'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">theme</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">code_format</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'&lt;svg</span> <span class="pre">class="rich-terminal"</span> <span class="pre">viewBox="0</span> <span class="pre">0</span> <span class="pre">{width}</span> <span class="pre">{height}"</span> <span class="pre">xmlns="http://www.w3.org/2000/svg"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;!--</span> <span class="pre">Generated</span> <span class="pre">with</span> <span class="pre">Rich</span> <span class="pre">https://www.textualize.io</span> <span class="pre">--&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;style&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">@font-face</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">"Fira</span> <span class="pre">Code";\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">src:</span> <span class="pre">local("FiraCode-Regular"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2")</span> <span class="pre">format("woff2"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff")</span> <span class="pre">format("woff");\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-style:</span> <span class="pre">normal;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">400;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">@font-face</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">"Fira</span> <span class="pre">Code";\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">src:</span> <span class="pre">local("FiraCode-Bold"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2")</span> <span class="pre">format("woff2"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff")</span> <span class="pre">format("woff");\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-style:</span> <span class="pre">bold;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">700;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">.{unique_id}-matrix</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">Fira</span> <span class="pre">Code,</span> <span class="pre">monospace;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-size:</span> <span class="pre">{char_height}px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">line-height:</span> <span class="pre">{line_height}px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-variant-east-asian:</span> <span class="pre">full-width;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">.{unique_id}-title</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-size:</span> <span class="pre">18px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">bold;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">arial;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{styles}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/style&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;defs&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;clipPath</span> <span class="pre">id="{unique_id}-clip-terminal"&gt;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">&lt;rect</span> <span class="pre">x="0"</span> <span class="pre">y="0"</span> <span class="pre">width="{terminal_width}"</span> <span class="pre">height="{terminal_height}"</span> <span class="pre">/&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/clipPath&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{lines}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/defs&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{chrome}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;g</span> <span class="pre">transform="translate({terminal_x},</span> <span class="pre">{terminal_y})"</span> <span class="pre">clip-path="url(#{unique_id}-clip-terminal)"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{backgrounds}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;g</span> <span class="pre">class="{unique_id}-matrix"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{matrix}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/g&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/g&gt;\n&lt;/svg&gt;\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">font_aspect_ratio</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0.61</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique_id</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.export_svg"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.export_svg" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate an SVG from the console contents (requires record=True in Console constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>title</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – The title of the tab in the output image</p></li>
<li><p><strong>theme</strong> (<em>TerminalTheme</em><em>, </em><em>optional</em>) – The <code class="docutils literal notranslate"><span class="pre">TerminalTheme</span></code> object to use to style the terminal</p></li>
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code></p></li>
<li><p><strong>code_format</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Format string used to generate the SVG. Rich will inject a number of variables
into the string in order to form the final SVG output. The default template used and the variables
injected by Rich can be found by inspecting the <code class="docutils literal notranslate"><span class="pre">console.CONSOLE_SVG_FORMAT</span></code> variable.</p></li>
<li><p><strong>font_aspect_ratio</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.11)"><em>float</em></a><em>, </em><em>optional</em>) – The width to height ratio of the font used in the <code class="docutils literal notranslate"><span class="pre">code_format</span></code>
string. Defaults to 0.61, which is the width to height ratio of Fira Code (the default font).
If you aren’t specifying a different font inside <code class="docutils literal notranslate"><span class="pre">code_format</span></code>, you probably don’t need this.</p></li>
<li><p><strong>unique_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – unique id that is used as the prefix for various elements (CSS styles, node
ids). If not set, this defaults to a computed value based on the recorded content.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.export_text">
<span class="sig-name descname"><span class="pre">export_text</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">styles</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.export_text"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.export_text" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate text from console contents (requires record=True argument in constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – If <code class="docutils literal notranslate"><span class="pre">True</span></code>, ansi escape codes will be included. <code class="docutils literal notranslate"><span class="pre">False</span></code> for plain text.
Defaults to <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>String containing console contents.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.file">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">file</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.IO" title="(in Python v3.11)"><span class="pre">IO</span></a><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></em><a class="headerlink" href="#rich.console.Console.file" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the file object to write to.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.get_style">
<span class="sig-name descname"><span class="pre">get_style</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.get_style"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.get_style" title="Permalink to this definition">¶</a></dt>
<dd><p>Get a Style instance by its theme name or parse a definition.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – The name of a style or a style definition.</p></li>
<li><p><strong>default</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.11)"><em>Union</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em><em>]</em>) – </p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>A Style object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style">Style</a></p>
</dd>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><strong>MissingStyle</strong> – If no style could be parsed from name.</p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.height">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">height</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><span class="pre">int</span></a></em><a class="headerlink" href="#rich.console.Console.height" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the height of the console.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The height (in lines) of the console.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)">int</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.input">
<span class="sig-name descname"><span class="pre">input</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">prompt</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">markup</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">emoji</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">password</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">stream</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.input"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.input" title="Permalink to this definition">¶</a></dt>
<dd><p>Displays a prompt and waits for input from the user. The prompt may contain color / style.</p>
<p>It works in the same way as Python’s builtin <a class="reference internal" href="#rich.console.Console.input" title="rich.console.Console.input"><code class="xref py py-func docutils literal notranslate"><span class="pre">input()</span></code></a> function and provides elaborate line editing and history features if Python’s builtin <a class="reference external" href="https://docs.python.org/3/library/readline.html#module-readline" title="(in Python v3.11)"><code class="xref py py-mod docutils literal notranslate"><span class="pre">readline</span></code></a> module is previously loaded.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>prompt</strong> (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="text.html#rich.text.Text" title="rich.text.Text"><em>Text</em></a><em>]</em>) – Text to render in the prompt.</p></li>
<li><p><strong>markup</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable console markup (requires a str prompt). Defaults to True.</p></li>
<li><p><strong>emoji</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable emoji (requires a str prompt). Defaults to True.</p></li>
<li><p><strong>password</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a>) – (bool, optional): Hide typed text. Defaults to False.</p></li>
<li><p><strong>stream</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.TextIO" title="(in Python v3.11)"><em>TextIO</em></a><em>]</em>) – (TextIO, optional): Optional file to read input from (rather than stdin). Defaults to None.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>Text read from stdin.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)">str</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.is_alt_screen">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">is_alt_screen</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><span class="pre">bool</span></a></em><a class="headerlink" href="#rich.console.Console.is_alt_screen" title="Permalink to this definition">¶</a></dt>
<dd><p>Check if the alt screen was enabled.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>True if the alt screen was enabled, otherwise False.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.is_dumb_terminal">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">is_dumb_terminal</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><span class="pre">bool</span></a></em><a class="headerlink" href="#rich.console.Console.is_dumb_terminal" title="Permalink to this definition">¶</a></dt>
<dd><p>Detect dumb terminal.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>True if writing to a dumb terminal, otherwise False.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.is_terminal">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">is_terminal</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><span class="pre">bool</span></a></em><a class="headerlink" href="#rich.console.Console.is_terminal" title="Permalink to this definition">¶</a></dt>
<dd><p>Check if the console is writing to a terminal.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>True if the console writing to a device capable of
understanding terminal codes, otherwise False.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.line">
<span class="sig-name descname"><span class="pre">line</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">count</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.line"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.line" title="Permalink to this definition">¶</a></dt>
<dd><p>Write new line(s).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>count</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – Number of new lines. Defaults to 1.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.log">
<span class="sig-name descname"><span class="pre">log</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">objects</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'</span> <span class="pre">'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">end</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">justify</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">emoji</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">markup</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlight</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">log_locals</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_stack_offset</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.log"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.log" title="Permalink to this definition">¶</a></dt>
<dd><p>Log rich content to the terminal.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>objects</strong> (<em>positional args</em>) – Objects to log to the terminal.</p></li>
<li><p><strong>sep</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write between print data. Defaults to ” “.</p></li>
<li><p><strong>end</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write at end of print data. Defaults to “\n”.</p></li>
<li><p><strong>style</strong> (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em><em>, </em><em>optional</em>) – A style to apply to output. Defaults to None.</p></li>
<li><p><strong>justify</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – One of “left”, “right”, “center”, or “full”. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>emoji</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable emoji code, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to None.</p></li>
<li><p><strong>markup</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable markup, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to None.</p></li>
<li><p><strong>highlight</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable automatic highlighting, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to None.</p></li>
<li><p><strong>log_locals</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Boolean to enable logging of locals where <code class="docutils literal notranslate"><span class="pre">log()</span></code>
was called. Defaults to False.</p></li>
<li><p><strong>_stack_offset</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – Offset of caller from end of call stack. Defaults to 1.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.measure">
<span class="sig-name descname"><span class="pre">measure</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">renderable</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">options</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.measure"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.measure" title="Permalink to this definition">¶</a></dt>
<dd><p>Measure a renderable. Returns a <a class="reference internal" href="measure.html#rich.measure.Measurement" title="rich.measure.Measurement"><code class="xref py py-class docutils literal notranslate"><span class="pre">Measurement</span></code></a> object which contains
information regarding the number of characters required to print the renderable.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>renderable</strong> (<em>RenderableType</em>) – Any renderable or string.</p></li>
<li><p><strong>options</strong> (<em>Optional</em><em>[</em><a class="reference internal" href="#rich.console.ConsoleOptions" title="rich.console.ConsoleOptions"><em>ConsoleOptions</em></a><em>]</em><em>, </em><em>optional</em>) – Options to use when measuring, or None
to use default options. Defaults to None.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>A measurement of the renderable.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference internal" href="measure.html#rich.measure.Measurement" title="rich.measure.Measurement">Measurement</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.options">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">options</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference internal" href="#rich.console.ConsoleOptions" title="rich.console.ConsoleOptions"><span class="pre">ConsoleOptions</span></a></em><a class="headerlink" href="#rich.console.Console.options" title="Permalink to this definition">¶</a></dt>
<dd><p>Get default console options.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.out">
<span class="sig-name descname"><span class="pre">out</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">objects</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'</span> <span class="pre">'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">end</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlight</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.out"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.out" title="Permalink to this definition">¶</a></dt>
<dd><p>Output to the terminal. This is a low-level way of writing to the terminal which unlike
<a class="reference internal" href="#rich.console.Console.print" title="rich.console.Console.print"><code class="xref py py-meth docutils literal notranslate"><span class="pre">print()</span></code></a> won’t pretty print, wrap text, or apply markup, but will
optionally apply highlighting and a basic style.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>sep</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write between print data. Defaults to ” “.</p></li>
<li><p><strong>end</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write at end of print data. Defaults to “\n”.</p></li>
<li><p><strong>style</strong> (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em><em>, </em><em>optional</em>) – A style to apply to output. Defaults to None.</p></li>
<li><p><strong>highlight</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable automatic highlighting, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use
console default. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>objects</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Any" title="(in Python v3.11)"><em>Any</em></a>) – </p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.pager">
<span class="sig-name descname"><span class="pre">pager</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pager</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">styles</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">links</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.pager"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.pager" title="Permalink to this definition">¶</a></dt>
<dd><p>A context manager to display anything printed within a “pager”. The pager application
is defined by the system and will typically support at least pressing a key to scroll.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>pager</strong> (<em>Pager</em><em>, </em><em>optional</em>) – A pager object, or None to use <code class="xref py py-class docutils literal notranslate"><span class="pre">SystemPager</span></code>. Defaults to None.</p></li>
<li><p><strong>styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Show styles in pager. Defaults to False.</p></li>
<li><p><strong>links</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Show links in pager. Defaults to False.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#rich.console.PagerContext" title="rich.console.PagerContext"><em>PagerContext</em></a></p>
</dd>
</dl>
<p class="rubric">Example</p>
<div class="doctest highlight-default notranslate"><div class="highlight"><pre id="codecell1"><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">rich.console</span> <span class="kn">import</span> <span class="n">Console</span>
<span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">rich.__main__</span> <span class="kn">import</span> <span class="n">make_test_card</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">console</span> <span class="o">=</span> <span class="n">Console</span><span class="p">()</span>
<span class="gp">&gt;&gt;&gt; </span><span class="k">with</span> <span class="n">console</span><span class="o">.</span><span class="n">pager</span><span class="p">():</span>
<span class="go">        console.print(make_test_card())</span>
</pre><button class="copybtn o-tooltip--left" data-tooltip="Copy" data-clipboard-target="#codecell1">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-copy" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="#000000" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <title>Copy to clipboard</title>
  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
  <rect x="8" y="8" width="12" height="12" rx="2"></rect>
  <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2"></path>
</svg>
    </button></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>A context manager.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#rich.console.PagerContext" title="rich.console.PagerContext">PagerContext</a></p>
</dd>
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>pager</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><em>Pager</em><em>]</em>) – </p></li>
<li><p><strong>styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a>) – </p></li>
<li><p><strong>links</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a>) – </p></li>
</ul>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.pop_render_hook">
<span class="sig-name descname"><span class="pre">pop_render_hook</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.pop_render_hook"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.pop_render_hook" title="Permalink to this definition">¶</a></dt>
<dd><p>Pop the last renderhook from the stack.</p>
<dl class="field-list simple">
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.pop_theme">
<span class="sig-name descname"><span class="pre">pop_theme</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.pop_theme"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.pop_theme" title="Permalink to this definition">¶</a></dt>
<dd><p>Remove theme from top of stack, restoring previous theme.</p>
<dl class="field-list simple">
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.print">
<span class="sig-name descname"><span class="pre">print</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">objects</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'</span> <span class="pre">'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">end</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">justify</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overflow</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">no_wrap</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">emoji</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">markup</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlight</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">height</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">crop</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">soft_wrap</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">new_line_start</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.print"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.print" title="Permalink to this definition">¶</a></dt>
<dd><p>Print to the console.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>objects</strong> (<em>positional args</em>) – Objects to log to the terminal.</p></li>
<li><p><strong>sep</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write between print data. Defaults to ” “.</p></li>
<li><p><strong>end</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – String to write at end of print data. Defaults to “\n”.</p></li>
<li><p><strong>style</strong> (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em><em>, </em><em>optional</em>) – A style to apply to output. Defaults to None.</p></li>
<li><p><strong>justify</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Justify method: “default”, “left”, “right”, “center”, or “full”. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>overflow</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Overflow method: “ignore”, “crop”, “fold”, or “ellipsis”. Defaults to None.</p></li>
<li><p><strong>no_wrap</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Disable word wrapping. Defaults to None.</p></li>
<li><p><strong>emoji</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable emoji code, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>markup</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable markup, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>highlight</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable automatic highlighting, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use console default. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>width</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>]</em><em>, </em><em>optional</em>) – Width of output, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to auto-detect. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>crop</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Crop output to width of terminal. Defaults to True.</p></li>
<li><p><strong>soft_wrap</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable soft wrap mode which disables word wrapping and cropping of text or <code class="docutils literal notranslate"><span class="pre">None</span></code> for
Console default. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>new_line_start</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>False</em>) – Insert a new line at the start if the output contains more than one line. Defaults to <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p></li>
<li><p><strong>height</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>]</em>) – </p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.print_exception">
<span class="sig-name descname"><span class="pre">print_exception</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">100</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">extra_lines</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">3</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">theme</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">word_wrap</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">show_locals</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">suppress</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_frames</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">100</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.print_exception"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.print_exception" title="Permalink to this definition">¶</a></dt>
<dd><p>Prints a rich render of the last exception and traceback.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>width</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>]</em><em>, </em><em>optional</em>) – Number of characters used to render code. Defaults to 100.</p></li>
<li><p><strong>extra_lines</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – Additional lines of code to render. Defaults to 3.</p></li>
<li><p><strong>theme</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Override pygments theme used in traceback</p></li>
<li><p><strong>word_wrap</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable word wrapping of long lines. Defaults to False.</p></li>
<li><p><strong>show_locals</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable display of local variables. Defaults to False.</p></li>
<li><p><strong>suppress</strong> (<em>Iterable</em><em>[</em><em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>ModuleType</em><em>]</em><em>]</em>) – Optional sequence of modules or paths to exclude from traceback.</p></li>
<li><p><strong>max_frames</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a>) – Maximum number of frames to show in a traceback, 0 for no maximum. Defaults to 100.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.print_json">
<span class="sig-name descname"><span class="pre">print_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">json</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">data</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">indent</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">2</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlight</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">skip_keys</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ensure_ascii</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">check_circular</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">allow_nan</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sort_keys</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.print_json"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.print_json" title="Permalink to this definition">¶</a></dt>
<dd><p>Pretty prints JSON. Output will be valid JSON.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>json</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – A string containing JSON.</p></li>
<li><p><strong>data</strong> (<em>Any</em>) – If json is not supplied, then encode this data.</p></li>
<li><p><strong>indent</strong> (<em>Union</em><em>[</em><em>None</em><em>, </em><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em><em>, </em><em>optional</em>) – Number of spaces to indent. Defaults to 2.</p></li>
<li><p><strong>highlight</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable highlighting of output: Defaults to True.</p></li>
<li><p><strong>skip_keys</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Skip keys not of a basic type. Defaults to False.</p></li>
<li><p><strong>ensure_ascii</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Escape all non-ascii characters. Defaults to False.</p></li>
<li><p><strong>check_circular</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Check for circular references. Defaults to True.</p></li>
<li><p><strong>allow_nan</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Allow NaN and Infinity values. Defaults to True.</p></li>
<li><p><strong>default</strong> (<em>Callable</em><em>, </em><em>optional</em>) – A callable that converts values that can not be encoded
in to something that can be JSON encoded. Defaults to None.</p></li>
<li><p><strong>sort_keys</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Sort dictionary keys. Defaults to False.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.push_render_hook">
<span class="sig-name descname"><span class="pre">push_render_hook</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">hook</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.push_render_hook"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.push_render_hook" title="Permalink to this definition">¶</a></dt>
<dd><p>Add a new render hook to the stack.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>hook</strong> (<a class="reference internal" href="#rich.console.RenderHook" title="rich.console.RenderHook"><em>RenderHook</em></a>) – Render hook instance.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.push_theme">
<span class="sig-name descname"><span class="pre">push_theme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">theme</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">inherit</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.push_theme"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.push_theme" title="Permalink to this definition">¶</a></dt>
<dd><p>Push a new theme on to the top of the stack, replacing the styles from the previous theme.
Generally speaking, you should call <a class="reference internal" href="#rich.console.Console.use_theme" title="rich.console.Console.use_theme"><code class="xref py py-meth docutils literal notranslate"><span class="pre">use_theme()</span></code></a> to get a context manager, rather
than calling this method directly.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>theme</strong> (<a class="reference internal" href="theme.html#rich.theme.Theme" title="rich.theme.Theme"><em>Theme</em></a>) – A theme instance.</p></li>
<li><p><strong>inherit</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Inherit existing styles. Defaults to True.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.render">
<span class="sig-name descname"><span class="pre">render</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">renderable</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">options</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.render"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.render" title="Permalink to this definition">¶</a></dt>
<dd><p>Render an object in to an iterable of <cite>Segment</cite> instances.</p>
<p>This method contains the logic for rendering objects with the console protocol.
You are unlikely to need to use it directly, unless you are extending the library.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>renderable</strong> (<em>RenderableType</em>) – An object supporting the console protocol, or
an object that may be converted to a string.</p></li>
<li><p><strong>options</strong> (<a class="reference internal" href="#rich.console.ConsoleOptions" title="rich.console.ConsoleOptions"><em>ConsoleOptions</em></a><em>, </em><em>optional</em>) – An options object, or None to use self.options. Defaults to None.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>An iterable of segments that may be rendered.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>Iterable[<a class="reference internal" href="segment.html#rich.segment.Segment" title="rich.segment.Segment">Segment</a>]</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.render_lines">
<span class="sig-name descname"><span class="pre">render_lines</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">renderable</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">options</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">pad</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">new_lines</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.render_lines"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.render_lines" title="Permalink to this definition">¶</a></dt>
<dd><p>Render objects in to a list of lines.</p>
<blockquote>
<div><p>The output of render_lines is useful when further formatting of rendered console text
is required, such as the Panel class which draws a border around any renderable object.</p>
<dl class="simple">
<dt>Args:</dt><dd><p>renderable (RenderableType): Any object renderable in the console.
options (Optional[ConsoleOptions], optional): Console options, or None to use self.options. Default to <code class="docutils literal notranslate"><span class="pre">None</span></code>.
style (Style, optional): Optional style to apply to renderables. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.
pad (bool, optional): Pad lines shorter than render width. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code>.
new_lines (bool, optional): Include “</p>
</dd>
</dl>
</div></blockquote>
<p>” characters at end of lines.</p>
<blockquote>
<div><dl class="simple">
<dt>Returns:</dt><dd><p>List[List[Segment]]: A list of lines, where a line is a list of Segment objects.</p>
</dd>
</dl>
</div></blockquote>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>renderable</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Union" title="(in Python v3.11)"><em>Union</em></a><em>[</em><a class="reference internal" href="#rich.console.ConsoleRenderable" title="rich.console.ConsoleRenderable"><em>ConsoleRenderable</em></a><em>, </em><a class="reference internal" href="#rich.console.RichCast" title="rich.console.RichCast"><em>RichCast</em></a><em>, </em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>]</em>) – </p></li>
<li><p><strong>options</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference internal" href="#rich.console.ConsoleOptions" title="rich.console.ConsoleOptions"><em>ConsoleOptions</em></a><em>]</em>) – </p></li>
<li><p><strong>style</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em>) – </p></li>
<li><p><strong>pad</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a>) – </p></li>
<li><p><strong>new_lines</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a>) – </p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.11)"><em>List</em></a>[<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.List" title="(in Python v3.11)"><em>List</em></a>[<a class="reference internal" href="segment.html#rich.segment.Segment" title="rich.segment.Segment"><em>Segment</em></a>]]</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.render_str">
<span class="sig-name descname"><span class="pre">render_str</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">text</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">justify</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overflow</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">emoji</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">markup</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlight</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">highlighter</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.render_str"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.render_str" title="Permalink to this definition">¶</a></dt>
<dd><p>Convert a string to a Text instance. This is called automatically if
you print or log a string.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>text</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – Text to render.</p></li>
<li><p><strong>style</strong> (<em>Union</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>]</em><em>, </em><em>optional</em>) – Style to apply to rendered text.</p></li>
<li><p><strong>justify</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Justify method: “default”, “left”, “center”, “full”, or “right”. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>overflow</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Overflow method: “crop”, “fold”, or “ellipsis”. Defaults to <code class="docutils literal notranslate"><span class="pre">None</span></code>.</p></li>
<li><p><strong>emoji</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable emoji, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use Console default.</p></li>
<li><p><strong>markup</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable markup, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use Console default.</p></li>
<li><p><strong>highlight</strong> (<em>Optional</em><em>[</em><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>]</em><em>, </em><em>optional</em>) – Enable highlighting, or <code class="docutils literal notranslate"><span class="pre">None</span></code> to use Console default.</p></li>
<li><p><strong>highlighter</strong> (<em>HighlighterType</em><em>, </em><em>optional</em>) – Optional highlighter to apply.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>Renderable object.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference internal" href="#rich.console.ConsoleRenderable" title="rich.console.ConsoleRenderable">ConsoleRenderable</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.rule">
<span class="sig-name descname"><span class="pre">rule</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">characters</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'─'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'rule.line'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">align</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'center'</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.rule"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.rule" title="Permalink to this definition">¶</a></dt>
<dd><p>Draw a line with optional centered title.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>title</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Text to render over the rule. Defaults to “”.</p></li>
<li><p><strong>characters</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Character(s) to form the line. Defaults to “─”.</p></li>
<li><p><strong>style</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Style of line. Defaults to “rule.line”.</p></li>
<li><p><strong>align</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – How to align the title, one of “left”, “center”, or “right”. Defaults to “center”.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.save_html">
<span class="sig-name descname"><span class="pre">save_html</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">theme</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">code_format</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'&lt;!DOCTYPE</span> <span class="pre">html&gt;\n&lt;html&gt;\n&lt;head&gt;\n&lt;meta</span> <span class="pre">charset="UTF-8"&gt;\n&lt;style&gt;\n{stylesheet}\nbody</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">color:</span> <span class="pre">{foreground};\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">background-color:</span> <span class="pre">{background};\n}}\n&lt;/style&gt;\n&lt;/head&gt;\n&lt;body&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;pre</span> <span class="pre">style="font-family:Menlo,\'DejaVu</span> <span class="pre">Sans</span> <span class="pre">Mono\',consolas,\'Courier</span> <span class="pre">New\',monospace"&gt;&lt;code&gt;{code}&lt;/code&gt;&lt;/pre&gt;\n&lt;/body&gt;\n&lt;/html&gt;\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">inline_styles</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.save_html"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.save_html" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate HTML from console contents and write to a file (requires record=True argument in constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – Path to write html file.</p></li>
<li><p><strong>theme</strong> (<em>TerminalTheme</em><em>, </em><em>optional</em>) – TerminalTheme object containing console colors.</p></li>
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>code_format</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Format string to render HTML. In addition to ‘{foreground}’,
‘{background}’, and ‘{code}’, should contain ‘{stylesheet}’ if inline_styles is <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p></li>
<li><p><strong>inline_styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – If <code class="docutils literal notranslate"><span class="pre">True</span></code> styles will be inlined in to spans, which makes files
larger but easier to cut and paste markup. If <code class="docutils literal notranslate"><span class="pre">False</span></code>, styles will be embedded in a style tag.
Defaults to False.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.save_svg">
<span class="sig-name descname"><span class="pre">save_svg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'Rich'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">theme</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">code_format</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'&lt;svg</span> <span class="pre">class="rich-terminal"</span> <span class="pre">viewBox="0</span> <span class="pre">0</span> <span class="pre">{width}</span> <span class="pre">{height}"</span> <span class="pre">xmlns="http://www.w3.org/2000/svg"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;!--</span> <span class="pre">Generated</span> <span class="pre">with</span> <span class="pre">Rich</span> <span class="pre">https://www.textualize.io</span> <span class="pre">--&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;style&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">@font-face</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">"Fira</span> <span class="pre">Code";\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">src:</span> <span class="pre">local("FiraCode-Regular"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2")</span> <span class="pre">format("woff2"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff")</span> <span class="pre">format("woff");\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-style:</span> <span class="pre">normal;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">400;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">@font-face</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">"Fira</span> <span class="pre">Code";\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">src:</span> <span class="pre">local("FiraCode-Bold"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2")</span> <span class="pre">format("woff2"),\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff")</span> <span class="pre">format("woff");\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-style:</span> <span class="pre">bold;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">700;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">.{unique_id}-matrix</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">Fira</span> <span class="pre">Code,</span> <span class="pre">monospace;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-size:</span> <span class="pre">{char_height}px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">line-height:</span> <span class="pre">{line_height}px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-variant-east-asian:</span> <span class="pre">full-width;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">.{unique_id}-title</span> <span class="pre">{{\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-size:</span> <span class="pre">18px;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-weight:</span> <span class="pre">bold;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">font-family:</span> <span class="pre">arial;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">}}\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{styles}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/style&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;defs&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;clipPath</span> <span class="pre">id="{unique_id}-clip-terminal"&gt;\n</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="pre">&lt;rect</span> <span class="pre">x="0"</span> <span class="pre">y="0"</span> <span class="pre">width="{terminal_width}"</span> <span class="pre">height="{terminal_height}"</span> <span class="pre">/&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/clipPath&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{lines}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/defs&gt;\n\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{chrome}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;g</span> <span class="pre">transform="translate({terminal_x},</span> <span class="pre">{terminal_y})"</span> <span class="pre">clip-path="url(#{unique_id}-clip-terminal)"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{backgrounds}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;g</span> <span class="pre">class="{unique_id}-matrix"&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">{matrix}\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/g&gt;\n</span>&nbsp;&nbsp;&nbsp; <span class="pre">&lt;/g&gt;\n&lt;/svg&gt;\n'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">font_aspect_ratio</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0.61</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique_id</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.save_svg"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.save_svg" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate an SVG file from the console contents (requires record=True in Console constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – The path to write the SVG to.</p></li>
<li><p><strong>title</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – The title of the tab in the output image</p></li>
<li><p><strong>theme</strong> (<em>TerminalTheme</em><em>, </em><em>optional</em>) – The <code class="docutils literal notranslate"><span class="pre">TerminalTheme</span></code> object to use to style the terminal</p></li>
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code></p></li>
<li><p><strong>code_format</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Format string used to generate the SVG. Rich will inject a number of variables
into the string in order to form the final SVG output. The default template used and the variables
injected by Rich can be found by inspecting the <code class="docutils literal notranslate"><span class="pre">console.CONSOLE_SVG_FORMAT</span></code> variable.</p></li>
<li><p><strong>font_aspect_ratio</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.11)"><em>float</em></a><em>, </em><em>optional</em>) – The width to height ratio of the font used in the <code class="docutils literal notranslate"><span class="pre">code_format</span></code>
string. Defaults to 0.61, which is the width to height ratio of Fira Code (the default font).
If you aren’t specifying a different font inside <code class="docutils literal notranslate"><span class="pre">code_format</span></code>, you probably don’t need this.</p></li>
<li><p><strong>unique_id</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – unique id that is used as the prefix for various elements (CSS styles, node
ids). If not set, this defaults to a computed value based on the recorded content.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.save_text">
<span class="sig-name descname"><span class="pre">save_text</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">clear</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">styles</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.save_text"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.save_text" title="Permalink to this definition">¶</a></dt>
<dd><p>Generate text from console and save to a given location (requires record=True argument in constructor).</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>path</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – Path to write text files.</p></li>
<li><p><strong>clear</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Clear record buffer after exporting. Defaults to <code class="docutils literal notranslate"><span class="pre">True</span></code>.</p></li>
<li><p><strong>styles</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – If <code class="docutils literal notranslate"><span class="pre">True</span></code>, ansi style codes will be included. <code class="docutils literal notranslate"><span class="pre">False</span></code> for plain text.
Defaults to <code class="docutils literal notranslate"><span class="pre">False</span></code>.</p></li>
</ul>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.screen">
<span class="sig-name descname"><span class="pre">screen</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">hide_cursor</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.screen"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.screen" title="Permalink to this definition">¶</a></dt>
<dd><p>Context manager to enable and disable ‘alternative screen’ mode.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>hide_cursor</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Also hide the cursor. Defaults to False.</p></li>
<li><p><strong>style</strong> (<a class="reference internal" href="style.html#rich.style.Style" title="rich.style.Style"><em>Style</em></a><em>, </em><em>optional</em>) – Optional style for screen. Defaults to None.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>Context which enables alternate screen on enter, and disables it on exit.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>~ScreenContext</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.set_alt_screen">
<span class="sig-name descname"><span class="pre">set_alt_screen</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">enable</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.set_alt_screen"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.set_alt_screen" title="Permalink to this definition">¶</a></dt>
<dd><p>Enables alternative screen mode.</p>
<p>Note, if you enable this mode, you should ensure that is disabled before
the application exits. See <code class="xref py py-meth docutils literal notranslate"><span class="pre">screen()</span></code> for a context manager
that handles this for you.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>enable</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Enable (True) or disable (False) alternate screen. Defaults to True.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>True if the control codes were written.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.set_live">
<span class="sig-name descname"><span class="pre">set_live</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">live</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.set_live"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.set_live" title="Permalink to this definition">¶</a></dt>
<dd><p>Set Live instance. Used by Live context manager.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>live</strong> (<a class="reference internal" href="live.html#rich.live.Live" title="rich.live.Live"><em>Live</em></a>) – Live instance using this Console.</p>
</dd>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><strong>errors.LiveError</strong> – If this Console has a Live context currently active.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.set_window_title">
<span class="sig-name descname"><span class="pre">set_window_title</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.set_window_title"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.set_window_title" title="Permalink to this definition">¶</a></dt>
<dd><p>Set the title of the console terminal window.</p>
<p>Warning: There is no means within Rich of “resetting” the window title to its
previous value, meaning the title you set will persist even after your application
exits.</p>
<p><code class="docutils literal notranslate"><span class="pre">fish</span></code> shell resets the window title before and after each command by default,
negating this issue. Windows Terminal and command prompt will also reset the title for you.
Most other shells and terminals, however, do not do this.</p>
<p>Some terminals may require configuration changes before you can set the title.
Some terminals may not support setting the title at all.</p>
<p>Other software (including the terminal itself, the shell, custom prompts, plugins, etc.)
may also set the terminal window title. This could result in whatever value you write
using this method being overwritten.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>title</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a>) – The new title of the terminal window.</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p></p><dl class="simple">
<dt>True if the control code to change the terminal title was</dt><dd><p>written, otherwise False. Note that a return value of True
does not guarantee that the window title has actually changed,
since the feature may be unsupported/disabled in some terminals.</p>
</dd>
</dl>
<p></p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.show_cursor">
<span class="sig-name descname"><span class="pre">show_cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">show</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.show_cursor"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.show_cursor" title="Permalink to this definition">¶</a></dt>
<dd><p>Show or hide the cursor.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>show</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Set visibility of the cursor.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)">bool</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.size">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">size</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference internal" href="#rich.console.ConsoleDimensions" title="rich.console.ConsoleDimensions"><span class="pre">ConsoleDimensions</span></a></em><a class="headerlink" href="#rich.console.Console.size" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the size of the console.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>A named tuple containing the dimensions.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference internal" href="#rich.console.ConsoleDimensions" title="rich.console.ConsoleDimensions">ConsoleDimensions</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.status">
<span class="sig-name descname"><span class="pre">status</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">status</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">spinner</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'dots'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">spinner_style</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'status.spinner'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">speed</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">1.0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">refresh_per_second</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">12.5</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.status"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.status" title="Permalink to this definition">¶</a></dt>
<dd><p>Display a status and spinner.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>status</strong> (<em>RenderableType</em>) – A status renderable (str or Text typically).</p></li>
<li><p><strong>spinner</strong> (<a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.11)"><em>str</em></a><em>, </em><em>optional</em>) – Name of spinner animation (see python -m rich.spinner). Defaults to “dots”.</p></li>
<li><p><strong>spinner_style</strong> (<em>StyleType</em><em>, </em><em>optional</em>) – Style of spinner. Defaults to “status.spinner”.</p></li>
<li><p><strong>speed</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.11)"><em>float</em></a><em>, </em><em>optional</em>) – Speed factor for spinner animation. Defaults to 1.0.</p></li>
<li><p><strong>refresh_per_second</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.11)"><em>float</em></a><em>, </em><em>optional</em>) – Number of refreshes per second. Defaults to 12.5.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>A Status object that may be used as a context manager.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference internal" href="status.html#rich.status.Status" title="rich.status.Status">Status</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.update_screen">
<span class="sig-name descname"><span class="pre">update_screen</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">renderable</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">region</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">options</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.update_screen"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.update_screen" title="Permalink to this definition">¶</a></dt>
<dd><p>Update the screen at a given offset.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>renderable</strong> (<em>RenderableType</em>) – A Rich renderable.</p></li>
<li><p><strong>region</strong> (<em>Region</em><em>, </em><em>optional</em>) – Region of screen to update, or None for entire screen. Defaults to None.</p></li>
<li><p><strong>x</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – x offset. Defaults to 0.</p></li>
<li><p><strong>y</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – y offset. Defaults to 0.</p></li>
<li><p><strong>options</strong> (<a class="reference external" href="https://docs.python.org/3/library/typing.html#typing.Optional" title="(in Python v3.11)"><em>Optional</em></a><em>[</em><a class="reference internal" href="#rich.console.ConsoleOptions" title="rich.console.ConsoleOptions"><em>ConsoleOptions</em></a><em>]</em>) – </p></li>
</ul>
</dd>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><strong>errors.NoAltScreen</strong> – If the Console isn’t in alt screen mode.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.update_screen_lines">
<span class="sig-name descname"><span class="pre">update_screen_lines</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">lines</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">x</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">y</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.update_screen_lines"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.update_screen_lines" title="Permalink to this definition">¶</a></dt>
<dd><p>Update lines of the screen at a given offset.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>lines</strong> (<em>List</em><em>[</em><em>List</em><em>[</em><a class="reference internal" href="segment.html#rich.segment.Segment" title="rich.segment.Segment"><em>Segment</em></a><em>]</em><em>]</em>) – Rendered lines (as produced by <code class="xref py py-meth docutils literal notranslate"><span class="pre">render_lines()</span></code>).</p></li>
<li><p><strong>x</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – x offset (column no). Defaults to 0.</p></li>
<li><p><strong>y</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><em>int</em></a><em>, </em><em>optional</em>) – y offset (column no). Defaults to 0.</p></li>
</ul>
</dd>
<dt class="field-even">Raises</dt>
<dd class="field-even"><p><strong>errors.NoAltScreen</strong> – If the Console isn’t in alt screen mode.</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="rich.console.Console.use_theme">
<span class="sig-name descname"><span class="pre">use_theme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">theme</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">inherit</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span><a class="reference internal" href="../_modules/rich/console.html#Console.use_theme"><span class="viewcode-link"><span class="pre">[source]</span></span></a><a class="headerlink" href="#rich.console.Console.use_theme" title="Permalink to this definition">¶</a></dt>
<dd><p>Use a different theme for the duration of the context manager.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>theme</strong> (<a class="reference internal" href="theme.html#rich.theme.Theme" title="rich.theme.Theme"><em>Theme</em></a>) – Theme instance to user.</p></li>
<li><p><strong>inherit</strong> (<a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.11)"><em>bool</em></a><em>, </em><em>optional</em>) – Inherit existing console styles. Defaults to True.</p></li>
</ul>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>[description]</p>
</dd>
<dt class="field-odd">Return type</dt>
<dd class="field-odd"><p><a class="reference internal" href="#rich.console.ThemeContext" title="rich.console.ThemeContext">ThemeContext</a></p>
</dd>
</dl>
</dd></dl>

<dl class="py property">
<dt class="sig sig-object py" id="rich.console.Console.width">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">width</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)"><span class="pre">int</span></a></em><a class="headerlink" href="#rich.console.Console.width" title="Permalink to this definition">¶</a></dt>
<dd><p>Get the width of the console.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>The width (in characters) of the console.</p>
</dd>
<dt class="field-even">Return type</dt>
<dd class="field-even"><p><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.11)">int</a></p>
</dd>
</dl>
</dd></dl>

</dd></dl>
```