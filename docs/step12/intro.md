# 实验指导 step12：为数组添加更多支持
step12 的目标是支持数组的初始化和传参：

语法上没有太大改动，

数组的初始化：

<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">declaration</span>
<div class="changed"><span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'['</span> <span class="SpecToken">Integer</span> <span class="SpecToken">']'</span><span class="SpecOperator">) +</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">'{' (Integer (',' Integer)*)? '}'</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>
</div></pre>



数组的传参：

<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">parameter_list</span> <span class="SpecToken">')'</span> <span class="SpecOperator">(</span><span class="SpecRule">compound_statement</span> <span class="SpecOperator">|</span> <span class="SpecToken">';'</span><span class="SpecOperator">)</span>
<span class="SpecRuleStart">parameter_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">type</span> <span class="SpecToken">Identifier ('[' ']')?(('['Integer']')*)?</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier ('[' ']')?(('['Integer']')*)?</span><span class="SpecOperator">)*)?</span>
</div></pre>


你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。