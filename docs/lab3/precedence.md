# 优先级和结合性

操作符有优先级和结合性的概念，在之前的编程经历中大家应该已经对这两个概念已经有了直观的理解，这里用例子进一步解释一下：

1. 优先级是两个操作符之间的关系，例如`*`的优先级比`+`高，所以表达式`1 + 2 * 3`应该解析成语法树`add (1  mul (2 3))`（前序表示），不能解析成`mul (add (1 2) 3)`
2. 结合性是一个操作符的性质，例如`-`是左结合的`1 - 2 - 3`应该解析成`sub (1  sub (2 3))`，不能解析成`sub (sub (1 2) 3)`

我们给出的语法规范已经表示了这样的性质，因此理论上我们不需要再额外定义操作符的优先级和结合性了。你可以自己试试，按照本步给出的语法规则，上面的两个表达式确实只能解析成我们期望的结果。

但是有一个问题：这样的语法规范虽然是正确的，也确实可以直接用来实现语法分析器了，但并不符合直观：我们一开始学习C或者别的编程语言的时候，讲的就是一个二元表达式由两个子表达式和中间的操作符组成，并且操作符有优先级和结合性。也就是这样的：

<pre id='vimCodeElement'><code></code><div class="changed">
<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">'+'</span><span class="SpecOperator">|</span><span class="SpecToken">'-'</span><span class="SpecOperator">)</span> <span class="SpecRule">expression</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">'*'</span><span class="SpecOperator">|</span><span class="SpecToken">'/'</span><span class="SpecOperator">|</span><span class="SpecToken">'%'</span><span class="SpecOperator">)</span> <span class="SpecRule">expression</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">)</span> <span class="SpecRule">expression</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
</div></pre>

当然，它是有歧义的，你也可以自己试试，如果只有这些产生式的话，上面的两个表达式都可以解析成正确或者错误的结果。所以如果想基于这个规范来实现语法分析器，就必须告诉语法分析工具这些操作符的优先级和结合性是什么。

之后每一步给出的语法都是没有歧义，本身就能体现优先级和结合性的。如果你确实想借助优先级和结合性来实现，需要两个步骤：

1. 把我们给出的语法规范转化成类似上面这样“更模糊”，有歧义的语法规范。我们相信这个方向的转化应该是容易的。
2. 指定每个操作符的优先级和结合性。可以参考[https://en.cppreference.com/w/c/language/operator_precedence](https://en.cppreference.com/w/c/language/operator_precedence)，它给出了C语言操作符的优先级和结合性，因为我们的MiniDecaf语言是C语言的一个子集，所以这张表格也足够我们的语言使用了。
