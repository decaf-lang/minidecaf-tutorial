# 实验指导 step6：
step6 我们要支持：
1. 条件语句：
  * if 语句
  * 条件表达式（又称三元/三目表达式，ternary expression）
2. 循环语句：
  * while 语句
  * for 语句
  * do-while 语句
3. break/continue 语句。

我们将给出 if 语句的完整实现，同学可以参考进而实现 while 语句，体会程序由线性结构向循环结构的转变。为了减少重复劳动，我们将 for、do-while 语句的实现作为可选，不计入成绩，感兴趣的同学可以自行完成。

为了保证条件语句和循环语句的语义完整性，我们给出了语句块的实现，但是不强调对应的作用域的概念，留待下一阶段实现。

语法上的改动是：

1. 条件语句、循环语句和 break/continue 语句
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'if'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span> <span class="SpecOperator">(</span><span class="SpecToken">'else'</span> <span class="SpecRule">statement</span><span class="SpecOperator">)?</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">compound_statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'while'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">declaration</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'do'</span> <span class="SpecRule">statement</span> <span class="SpecToken">'while'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'break'</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'continue'</span> <span class="SpecToken">';'</span>
</div></pre>

2. 条件表达式
<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span><br>
<span class="SpecRuleStart">conditional</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">logical_or</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">logical_or</span> <span class="SpecToken">'?'</span> <span class="SpecRule">expression</span> <span class="SpecToken">':'</span> <span class="SpecRule">conditional</span>
</div></pre>

3. `block_item`：为了下一阶段做准备
<pre id='vimCodeElement'><code></code><div class="changed">
<div class="changed"><span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>
</div>
<div class="changed"><span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>
</div></pre>

条件语句和循环语句的语义和 C 相同，需要注意条件表达式优先级只比赋值高，同时要检查 break/continue 不能出现在循环外。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。