# 实验指导 step11：指针
step11 支持的是指针：

1. 增加类型：指针类型
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">type</span> <span class="SpecToken">'*'</span></div></pre>

2. 引入左值的概念，修改赋值
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">unary</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span></div></pre>

3. 支持取地址操作符 `&` 和解引用操作符 `*`
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">postfix</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'&amp;'</span><span class="SpecOperator">|</span><span class="SpecToken">'*'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span></div></pre>

4. 支持类型转换
<pre id='vimCodeElement'><code></code>
<span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> ...
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">type</span> <span class="SpecToken">')'</span> <span class="SpecRule">unary</span></div></pre>

step11 相当复杂，代码量不小。
需要我们引入类型系统、左值的概念，并且加入类型检查以及一大堆语义检查。
