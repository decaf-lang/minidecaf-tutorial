# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step2 语法规范
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
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
</div></pre>

# step2 语义规范
**2.1** 运算符 `-` 的结果是其操作数的相反数。

**2.2** 运算符 `~` 的结果是其操作数的二进制反码（也就是说，结果中的每一个二进制位是 1 当且仅当其对应的二进制位是 0）。

**2.3** 当操作数不等于 0 时，逻辑非运算符 `!` 的结果为 0；当操作数等于 0 时，其结果为 1。

**2.4** MiniDecaf 中，负数字面量不被整体作为一个 token。它被看成是一个取负符号、后面是它的绝对值。
     所以我们无法用字面量表示 `-2147483648`，但可以写成 `-2147483647-1`（待我们加上四则运算后）。

**2.5** 整数运算越界是**未定义行为**（undefined behavior），即对程序的行为无任何限制。
> 例如 `-(-2147483647-1)` 是未定义行为。这一条规则对于后续 step 引入的运算符也都适用。
> 对于含有未定义行为的 C/C++ 程序，在启用优化选项编译时，编译器可能产生意料之外的结果。
