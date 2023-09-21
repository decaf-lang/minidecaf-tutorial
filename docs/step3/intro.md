# 实验指导 step3：加减乘除模
step3 我们要增加的是：加 `+`、减 `-`、乘 `*`、整除 `/`、模 `%` 以及括号 `(` `)`。

语法上我们继续修改 `expression`，变成

<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">additive</span>

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
</div></pre>

新特性的语义、优先级、结合性和 C 以及常识相同，例如 `1+2*(4/2+1) == 7`。

我们这种表达式语法写法可能比较繁琐，但它有几个好处：
1. 和 [C17 标准草案](../../REFERENCE.md)保持一致
2. 把优先级和结合性信息直接编码入语法里，见[优先级和结合性](./precedence.md)一节。

我们只接受 pdf 格式的实验报告，你需要将报告放在仓库的 `./reports/<branch-name>.pdf`，比如 stage 1 的实验报告需要放在 `stage-1` 这个 branch 下的 `./reports/stage-1.pdf`。整个 stage 1 只需要提交一份报告，你不需要单独为 step 3 准备报告。

你需要：
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 完成实验报告（具体要求请看实验指导书的首页）。实验报告中需要包括：
  * 你的学号姓名
  * 简要叙述，为了完成这个 stage 你做了哪些工作（即你的实验内容）
  * 指导书上的思考题
  * 如果你复用借鉴了参考代码或其他资源，请明确写出你借鉴了哪些内容。*并且，即使你声明了代码借鉴，你也需要自己独立认真完成实验。*
  * 如有代码交给其他同学参考，也必须在报告中声明，告知给哪些同学拷贝过代码（包括可能通过间接渠道传播给其他同学）。

## 如何检查我是否通过自动测试(CI)

在 `git.tsinghua` 上打开你的项目，在界面的右侧，Clone 按钮的下方，`commit id` 的左侧，可以看到一个画圈的 `×` 或者 `√` 的图标，代表当前 commit 是否通过 CI 测试。

如果你希望获取详细测试输出，可以点击这个画圈的 `×` 或者 `√` 的图标，或者在网页左侧选择 `CI/CD` 一栏的 `Jobs`，然后选择希望查看的评测结果即可。如果测试输出无法显示，可以点击输出框右上角四个按钮中最左边的一个，或者在当前地址(如`.../jobs/123456`)的后面加上`/raw`(如`.../jobs/123456/raw`)，即可获取测试输出。