# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step8 语法规范
灰色部分表示相对上一节的修改。
<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecRule">compound_statement</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<span class="SpecRuleStart">compound_statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'if'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span> <span class="SpecOperator">(</span><span class="SpecToken">'else'</span> <span class="SpecRule">statement</span><span class="SpecOperator">)?</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">compound_statement</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">declaration</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'while'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'break'</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'continue'</span> <span class="SpecToken">';'</span>
</div>
<span class="SpecRuleStart">declaration</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">assignment</span>

<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span>

<span class="SpecRuleStart">conditional</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'?'</span> <span class="SpecRule">expression</span> <span class="SpecToken">':'</span> <span class="SpecRule">conditional</span>

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

# step8 语义规范

> 方便起见，我们称 for 循环括号中的三个表达式/声明自左向右依次为 init、ctrl 和 post。
> 例如 `for (i=0; i<100; i=i+1);` 中，`i=0` 是 init，`i<100` 是 ctrl，`i=i+1` 是 post。

**8.1** 有两种循环语句：for 循环、while 循环。执行一条循环语句，意味着反复执行一条语句（即循环体），直到其控制表达式等于 0。

**8.2** while 循环的控制表达式的求值在循环体的每次执行之前。

**8.3** 对于 for 循环而言：如果 init 是一个声明，其声明发生在控制表达式的第一次求值之前；如果 init 是一个表达式，其求值会在控制表达式的第一次求值之前。ctrl 即是控制表达式，其求值在循环体的每次执行之前。post 的求值在循环体的每次执行之后。

**8.4** for 循环的 init、ctrl 和 post 都可以被省略。省略 ctrl 等价于将其替换为一个非零常数，比如 1。

**8.5** 循环语句有其自己的作用域，且是它所在的作用域的子集。循环体也有其作用域，且是循环语句的作用域的子集。如果 for 循环的 init 是一条声明，则其所声明的变量所属的作用域是整个 for 循环语句的作用域（包含 init、ctrl、post 和循环体）。
> 例如，`for (int i=0;;i=i+1) { int i=1; return i; }` 是不合法的代码片段。

**8.7** continue 语句和 break 语句要么出现在循环体里，要么其就是循环体。

**8.8** 执行一条 continue 语句，意味着将程序的执行跳转至该条 continue 语句所在的最小的循环语句的循环体的末尾。
> 例如，`for (int i=0;i<100;i++) { s+=i; continue; }` 等价于 `for (int i=0;i<100;i++) { s+=i; }`。

**8.9** 执行一条 break 语句，意味着终止该条 break 语句所在的最小的循环语句的执行。
