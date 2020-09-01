# 实验指导 step2：一元运算符
第二步中，我们要给整数常量增加一元运算：取负 `-`、按位取反 `~` 以及逻辑非 `!`。

语法上，我们需要修改 `expression` 的定义，从 `expression : Integer` 变成：

<pre id='vimCodeElement'>
<div class="changed"><span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
</div></pre>

