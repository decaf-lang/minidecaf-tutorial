# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step6 语法规范
灰色部分表示相对上一节的修改。

<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<div class="changed"><span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecRule">compound_statement</span>
</div>
<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<div class="changed"><span class="SpecRuleStart">compound_statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>
</div>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">compound_statement</span>
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


# step6 语义规范

**6.1** 根据其声明的位置，每一个标识符都属于一个作用域。目前我们有两种作用域：文件级和块级。如果是在块中声明，则标识符其声明所属的块的作用域中，例如局部变量；否则标识符在文件级（全局）作用域中，例如全局变量。

**6.2** （更新 5.6）如果一个标识符在两个作用域里面，这两个作用域必然是嵌套的，即一个内层作用域完全被另一个外层作用域所覆盖。且在内层作用域中，外层作用域里该标识符所指派（designate）的变量或函数是不可见的。
> 在初始化表达式中，其正在初始化的变量已被声明，会隐藏（shadow）外层作用域的同名变量，但其值不确定。例如在下面的代码片段中，`a + 1` 的值是不确定的。
> ```
> int a = 1;
> {
>   int a = a + 1;
> }
> ```

**6.3** （更新 5.3）对于同一个标识符，在同一个作用域中至多有一个声明。

**6.4** （更新 5.4）使用不在当前开作用域中的变量名是不合法的。

