# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step2 语法规范
灰色部分表示相对上一节的修改。

<pre id='vimCodeElement'>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">statement</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>

<div class="changed"><span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
</div></pre>

# step2 语义规范
**2.1.** MiniDecaf 中，负数字面量不被整体作为一个 token。它被看成是一个取负符号、后面是它的绝对值。
     这意味着我们无法用字面量表示 `2147483648`，但可以写成 `-2147483647-1`（待我们加上四则运算后）。

**2.2.** 运算越界是未定义行为。例如 `-(-2147483647-1)` 是未定义行为。

**2.3.** 除非特别声明，子表达式求值顺序是不确定的。
     例如：执行 `int a=0; (a=1)+(a=a+1);` 之后 a 的值是不确定的。

