# 实验指导 step11：数组
step11 的目标是支持数组：

语法上没有太大改动，
1. 数组的初始化：
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

我们只接受 pdf 格式的实验报告，你需要将报告放在仓库的 `./reports/<branch-name>.pdf`，比如 stage 6 的实验报告需要放在 `stage-6` 这个 branch 下的 `./reports/stage-6.pdf`。整个 stage 6 只需要提交一份报告，你不需要单独为 step 11 准备报告。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。