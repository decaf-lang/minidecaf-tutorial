# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step9 语法规范
灰色部分表示相对上一节的修改。
<pre id='vimCodeElement'>
<code></code>
<div class="changed"><span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span><span class="SpecOperator">*</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">parameter_list</span> <span class="SpecToken">')'</span> <span class="SpecOperator">(</span><span class="SpecRule">compound_statement</span> <span class="SpecOperator">|</span> <span class="SpecToken">';'</span><span class="SpecOperator">)</span>
</div>
<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<div class="changed"><span class="SpecRuleStart">parameter_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span><span class="SpecOperator">)*)?</span>
</div>
<span class="SpecRuleStart">compound_statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'{'</span> <span class="SpecRule">block_item</span><span class="SpecOperator">*</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">block_item</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">declaration</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'if'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span> <span class="SpecOperator">(</span><span class="SpecToken">'else'</span> <span class="SpecRule">statement</span><span class="SpecOperator">)?</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">compound_statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'for'</span> <span class="SpecToken">'('</span> <span class="SpecRule">declaration</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">';'</span> <span class="SpecRule">expression</span><span class="SpecOperator">?</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'while'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecRule">statement</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'do'</span> <span class="SpecRule">statement</span> <span class="SpecToken">'while'</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'break'</span> <span class="SpecToken">';'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'continue'</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">declaration</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>

<div class="changed"><span class="SpecRuleStart">expression_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">expression</span><span class="SpecOperator">)*)?</span>
</div>
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

<div class="changed"><span class="SpecRuleStart">unary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">postfix</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">postfix</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression_list</span> <span class="SpecToken">')'</span>
</div>
<span class="SpecRuleStart">primary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span>
</pre>

# step9 语义规范

> **函数声明**指对函数名、参数类型及返回值类型的声明，包含了函数体的函数声明被称作**函数定义**。
>
> 例如，`int fun(int x)` 是一个函数声明，`int fun() { return 1; }` 是一个函数定义。

**9.1** 在函数调用中，实参和形参的参数个数必须相同，同一位置的参数类型也必须相同。
> 现在只有 int 类型，不过以后会有更多类型。

**9.2** 在准备函数的调用时，所有的实参会被求值，然后赋给相应位置上的形参。
> 在函数体中，形参的值可能会被改变，但即便实参是一个可修改的左值，被调用函数中形参的改变也不会影响实参的值。

**9.4** 函数是可以递归调用的，包括直接调用自身、或者通过其他的函数间接地递归。

**9.5** （更新 5.10）执行一条 `return` 语句，意味着终止当前函数的执行，并将控制权交还给调用当前函数的 caller，语句中的表达式的值会返还给 caller 作为函数调用的表达式的值。一个函数可以有任意多条 `return` 语句。

**9.6** 如果一个函数在一个表达式中被调用了，那么它应有且仅有一个定义；否则，它应有不多于一个定义。
> 所以，如果一个函数被声明了却没有被调用，那么它也无需被定义。

**9.7** 函数的形参可以被视为在函数体的开头被定义（被以实参的值初始化）的局部变量。所有形参均为左值，且不能被在函数体中直接重定义（除非是在一个更小的嵌套的块中）。
> 例如，`int f(int x) { int x; }` 不合法，但 `int f(int x) {{ int x; }}` 合法。

**9.8** 如果一个不是 `main` 的函数执行到了它的 `}`，且其返回值被 caller 所使用，则这是一个未定义行为。
> 对于感兴趣的同学：C 语言中规定只有使用了返回值才是未定义行为，而 C++ 中规定不管返回值有没有被使用，都是未定义行为。
>
> 我们没有支持 void 类型，但可以忽略返回值达到类似的效果。
>
> “执行到了 `}`” 意味着执行时没有通过 `return` 返回，例如 `int f(){if(0) return 0;}`。
>
> 实现的时候，你可以直接让所有函数都默认返回 0，语义规范说 main 之外的函数没有 return 是未定义行为，未定义行为的意思就是你想怎么处理都可以，所以全部默认返回 0 当然也是可以的，而且更清晰简单。

**9.9** 所有同名函数声明的形参个数必须相同。

**9.10** 在函数定义之前，可以有一个前置的函数声明。
> 事实上，在 C/C++ 标准中，函数声明可以出现在任意位置任意多次。因为多个头文件中可能出现同一个函数的声明，在预处理过 `#include` 之后，便可能会面对多个函数声明的情况。
> 
> 简单起见，这里我们只要求支持一个前置的函数声明，在函数定义之后出现的以及更多次数的函数声明我们不做规定。

**9.11** 函数名属于文件级作用域。对于函数定义，形参声明所在作用域就是函数体的块语句对应作用域；对于不在函数定义中的函数声明，形参声明所在的作用域是一个单独的仅包含该函数形参声明列表的作用域，其被称为**函数原型**作用域。
> 所以，函数体中的局部变量可以与该函数同名，例如 `int f() {int f=0; return f;}` 是合法的；函数声明中不能有同名参数，例如 `int f(int x, int x)` 是不合法的。
