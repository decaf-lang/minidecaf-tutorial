# 实验指导 step2：一元运算符
step2 中，我们要给整数常量增加一元运算：取负 `-`、按位取反 `~` 以及逻辑非 `!`。

语法上，我们需要修改 `expression` 的定义，从 `expression : Integer` 变成：

<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
</div></pre>

三个操作的语义和 C 以及常识相同，例如 `~0 == -1`，`!!2 == 1`。
稍微一提，关于按位取反，我们使用补码存储 int；关于逻辑非，只有 0 表示逻辑假，其他的 int 都是逻辑真。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。