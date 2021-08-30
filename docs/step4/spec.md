# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step4 语法规范
灰色部分表示相对上一节的修改。

<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">statement</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>

<div class="changed"><span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>

<span class="SpecRuleStart">logical_or</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_and</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'||'</span> <span class="SpecRule">logical_and</span>

<span class="SpecRuleStart">logical_and</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">equality</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_and</span> <span class="SpecToken">'&amp;&amp;'</span> <span class="SpecRule">equality</span>

<span class="SpecRuleStart">equality</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">relational</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">equality</span> <span class="SpecOperator">(</span><span class="SpecToken">'=='</span><span class="SpecOperator">|</span><span class="SpecToken">'!='</span><span class="SpecOperator">)</span> <span class="SpecRule">relational</span>

<span class="SpecRuleStart">relational</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">additive</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">relational</span> <span class="SpecOperator">(</span><span class="SpecToken">'&lt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;'</span><span class="SpecOperator">|</span><span class="SpecToken">'&lt;='</span><span class="SpecOperator">|</span><span class="SpecToken">'&gt;='</span><span class="SpecOperator">)</span> <span class="SpecRule">additive</span>
</div>
<span class="SpecRuleStart">additive</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">multiplicative</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">additive</span> <span class="SpecOperator">(</span><span class="SpecToken">'+'</span><span class="SpecOperator">|</span><span class="SpecToken">'-'</span><span class="SpecOperator">)</span> <span class="SpecRule">multiplicative</span>

<span class="SpecRuleStart">multiplicative</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">multiplicative</span> <span class="SpecOperator">(</span><span class="SpecToken">'*'</span><span class="SpecOperator">|</span><span class="SpecToken">'/'</span><span class="SpecOperator">|</span><span class="SpecToken">'%'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">primary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
</pre>


# step4 语义规范

**4.1** 关系操作符 `<`（小于）、`>`（大于）、`<=`（小于等于）和`>=`（大于等于）的结果取决于两个操作数是否满足它们所指定的关系，当满足时结果为 1，当不满足时结果为 0。
> 关系操作符可能导致表达式的含义与数学文献中常见的含义不同，例如 `0<1<2` 的含义与 `(0<1)<2` 相同，即“如果 0 小于 1，那么判断是否有 1 小于 2，否则判断是否有 0 小于 2”。

**4.2** 判等操作符 `==`（等于）和 `!=`（不等于）类似于关系操作符，结果取决于两个操作数是否满足它们所指定的关系，当满足时结果为 1，当不满足时结果为 0。但判等操作符的优先级比关系操作符更低。对于任意一对操作数，这两个操作符中有且仅有一个结果为 1。
> 其优先级的设定会导致其含义在某些时候可能会反直观，例如，`0 < 1 == 2 < 3` 的运算结果为 1。

**4.3** 当操作数都非 0 时，逻辑与操作符 `&&` 的结果为 1；否则其结果为 0。

**4.4** 当操作数有一个非 0 时，逻辑或操作符 `||` 的结果为 1；否则其结果为 0。

**4.5** 逻辑操作符 `||` 和 `&&` 依然遵循语义规范 3.5，即其操作数的求值顺序是未指定行为。
     换言之，我们不对逻辑表达式的短路求值做要求，可以将操作数两个以任意顺序计算出，再计算逻辑操作的结果。
                                                                 
