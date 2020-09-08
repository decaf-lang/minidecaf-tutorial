# 实验指导 step4：比较和逻辑表达式
step4 我们要增加的是：

1. 比较大小和相等的二元操作：`<`、`<=`、`>=`, `>`, `==`, `!=`
    <pre id='vimCodeElement'><code></code><div class="changed">
    <span class="SpecRuleStart">equality</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">relational</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecRule">equality</span> <span class="SpecOperator">(</span><span class="SpecToken">'=='</span><span class="SpecOperator">|</span><span class="SpecToken">'!='</span><span class="SpecOperator">)</span> <span class="SpecRule">relational</span>

    <span class="SpecRuleStart">relational</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">additive</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecRule">relational</span> <span class="SpecOperator">(</span><span class="SpecToken">'&lt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&lt;='</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;='</span><span class="SpecOperator">)</span> <span class="SpecRule">additive</span></div></pre>

2. 逻辑与 `&&`、逻辑或 `||`
    <pre id='vimCodeElement'><code></code><div class="changed">
    <span class="SpecRuleStart">expression</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>

    <span class="SpecRuleStart">logical_or</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_and</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'||'</span> <span class="SpecRule">logical_and</span>

    <span class="SpecRuleStart">logical_and</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">equality</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_and</span> <span class="SpecToken">'&amp;&amp;'</span> <span class="SpecRule">equality</span></div></pre>

新特性的语义、优先级、结合性和 C 以及常识相同，例如 `1<3 == 2<3 && 5>=2` 是逻辑真（int 为 `1`）。
但特别注意，C 中逻辑运算符 `||` 和 `&&` 有短路现象，我们不要求。
