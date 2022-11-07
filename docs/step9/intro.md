# 实验指导 step9：函数
step9 开始，我们要支持多函数了。

1. 我们需要支持函数的声明和定义：
    <pre id='vimCodeElement'><code></code><div class="changed">
    <div class="changed"><span class="SpecRuleStart">program</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span><span class="SpecOperator">*</span>

    <span class="SpecRuleStart">function</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">parameter_list</span> <span class="SpecToken">')'</span> <span class="SpecOperator">(</span><span class="SpecRule">compound_statement</span> <span class="SpecOperator">|</span> <span class="SpecToken">';'</span><span class="SpecOperator">)</span>
    </div>
    <div class="changed"><span class="SpecRuleStart">parameter_list</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span><span class="SpecOperator">)*)?</span>
    </div>
    </pre>

2. 我们还需要支持函数调用：
    <pre id='vimCodeElement'><code></code><div class="changed">
    <div class="changed"><span class="SpecRuleStart">expression_list</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">expression</span><span class="SpecOperator">)*)?</span>
    </div>
    <div class="changed"><span class="SpecRuleStart">unary</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">postfix</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

    <span class="SpecRuleStart">postfix</span>
    <span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
    <span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression_list</span> <span class="SpecToken">')'</span>
    </div>
    </pre>

语义检查部分，我们需要检查函数的重复定义、检查调用函数的实参（argment）和形参（parameter）的个数类型一致。我们不支持 void 返回类型，这可以通过忽略函数的 int 返回值实现。

**注意**：从 step 9 开始，MiniDecaf 会引入 runtime，部分函数在源代码中只有声明，其定义在 runtime 编译得到的链接库中。因此我们并不需要检查函数只声明、未定义的情况。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。
