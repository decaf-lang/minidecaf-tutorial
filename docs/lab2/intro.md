# 实验指导 step2：一元运算符
step2 中，我们要给整数常量增加一元运算：取负 `-`、按位取反 `~` 以及逻辑非 `!`。

语法上，我们需要修改 `expression` 的定义，从 `expression : Integer` 变成：

<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
</div></pre>

三个操作的语义和 C 以及常识相同，例如 `~0 == -1`，`!!2 == 1`。
稍微一提，关于按位取反，我们使用补码存储 int；关于逻辑非，只有 0 表示逻辑假，其他的 int 都是逻辑真。
