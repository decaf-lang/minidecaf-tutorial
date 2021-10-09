# 实验指导 step11：数组
step11 的目标是支持数组：

语法上没有太大改动，
1. 数组的声明：
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">declaration</span>
<div class="changed"><span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'['</span> <span class="SpecToken">Integer</span> <span class="SpecToken">']'</span><span class="SpecOperator">)*</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>
</div></pre>

2. 数组的下标操作
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">postfix</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression_list</span> <span class="SpecToken">')'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">postfix</span> <span class="SpecToken">'['</span> <span class="SpecRule">expression</span> <span class="SpecToken">']'</span>
</div></pre>

step11 难度不大，但有了数组让我们能够写很多有意思的程序了，step11 之前甚至 MiniDecaf 连快速排序都写不了。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。