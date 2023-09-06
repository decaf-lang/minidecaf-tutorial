# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step7 语法规范
灰色部分表示相对上一节的修改。

<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<div class="changed"><span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>
</div>
<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<div class="changed"><span class="SpecRuleStart">compound_statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>
</div>
<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">compound_statement</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'if'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span> <span class="SpecOperator">(</span><span class="SpecToken">'else'</span> <span class="SpecRule">statement</span><span class="SpecOperator">)?</span>
</div>
<span class="SpecRuleStart">declaration</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">assignment</span>

<div class="changed"><span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span>

<span class="SpecRuleStart">conditional</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'?'</span> <span class="SpecRule">expression</span> <span class="SpecToken">':'</span> <span class="SpecRule">conditional</span>
</div>
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
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span>
</pre>

> 注意：`if` 的 `then` 分支和 `else` 分支需要是一个语句（statement）而非声明（declaration）。
> 例如 `if (1) int a;` 不是合法的 MiniDecaf 程序。

# step7 语义规范

**7.1** 条件表达式会先对第一个操作数求值，再根据其值选择计算第二个或第三个操作数。当且仅当第一个操作数的值不等于 0，我们会对第二个操作数求值。当且仅当第一个操作数的值等于 0，我们会对第三个操作数求值。当第一个操作数的值为 0 时，条件表达式的求值结果为第二个操作数所求得的值；当第一个操作数的值非 0 时，条件表达式的求值结果为第三个操作数所求得的值。
> 不论选择第二个操作数或者是第三个操作数去求值，都必须首先计算完第一个操作数，之后才能开始第二个或第三个操作数的求值计算。

**7.2** 对于 if 语句而言，当控制条件不等于 0 时，会执行第一个子句；当控制条件等于 0 时，如果有 else 分支，就会执行第二个语句，否则整个 if 语句的执行便已经完成。

**7.3** 如果出现悬吊 `else`（dangling else），要求 `else` 优先和最接近的没有匹配 `else` 的 `if` 匹配。
> 例如 `if (0) if (0) ; else ;` 等价于 `if (0) { if (0) ; else; }` 而非 `if (0) { if (0) ; } else ;`。
