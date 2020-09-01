# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step12 语法规范
灰色部分表示相对上一节的修改。
<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">function</span> <span class="SpecOperator">|</span> <span class="SpecRule">declaration</span><span class="SpecOperator">)*</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">parameter_list</span> <span class="SpecToken">')'</span> <span class="SpecOperator">(</span><span class="SpecRule">compound_statement</span> <span class="SpecOperator">|</span> <span class="SpecToken">';'</span><span class="SpecOperator">)</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">type</span> <span class="SpecToken">'*'</span>

<span class="SpecRuleStart">parameter_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span><span class="SpecOperator">)*)?</span>

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
<div class="changed"><span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'['</span> <span class="SpecToken">Integer</span> <span class="SpecToken">']'</span><span class="SpecOperator">)*</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>
</div>
<span class="SpecRuleStart">expression_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">expression</span><span class="SpecOperator">)*)?</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">assignment</span>

<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecRule">unary</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span>

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
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">postfix</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'&amp;'</span><span class="SpecOperator">|</span><span class="SpecToken">'*'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">type</span> <span class="SpecToken">')'</span> <span class="SpecRule">unary</span>

<span class="SpecRuleStart">postfix</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression_list</span> <span class="SpecToken">')'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">postfix</span> <span class="SpecToken">'['</span> <span class="SpecRule">expression</span> <span class="SpecToken">']'</span>
</div>
<span class="SpecRuleStart">primary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
</pre>

# step12 语义规范
**12.1.** 支持多维数组，但每一维长度只能是正整数常数，不能是零或负数。
> 所以也没有变长数组 `int a[n];` 也没有不定长数组 `int a[];`。

**12.2.** 对数组取地址是错误，也不会有指向数组的指针。
> 这是为了简化实验，否则需要引入 C 中一堆繁复的记号，像 `int *a[10]` 和 `int (*a)[10]`，对于实验意义不大。

**12.3.** 数组声明不能有初始值。局部变量数组初始值未定，全局变量初始值为零。
> C 中可以写 `int a[2]={1, 2}` 但 MiniDecaf 不行。

**12.4.** 数组首地址对齐要求同元素的对齐要求（4 字节）。
    数组的各个元素在内存中是连续的，并且多维的情况下排在前面的维度优先。
> 例如 `int a[3][4][5]` 占用了 60 个 int（240 字节）的连续内存，和 `int b[60]` 一样。
> `a[1][2][3]` 的偏移量是 `(1*20+2*5+3) * 4` 字节，和 `b[33]` 一样。

**12.5.** 下标运算优先级高于一元运算符。
> 因此 `-a[0]` 即 `-(a[0])`。

**12.6.** 下标运算 `a[b]` 的操作数类型必须是：`a` 为指针或数组，`b` 为 int。

**12.7.** 下标运算越界是未定义行为。

**12.8.** 可以将数组的前几维单独提出，类型还是数组类型，可转换以后赋给一个指针。
> 例如 `int a[2][2][2]`，那么 `int *p = (int*) a[0]; int *q = (int*) a[1][1];` 是合法的。
> 但 `int x=a[1]` 和 `int *r=a[0][0][0]` 是不合法的。

**12.9.** 左值表达式除了能通过 11.1 中三条规则得到，新增一条规则：
* 通过下标运算，如果结果类型不是数组类型，那么结果表达式是左值。
> 例如 `int a[2][2]`，那么 `a[1]` 不是左值，但 `a[1][1]` 是左值，`a[1][1]=2` 和 `&a[1][1]` 都是合法操作。

**12.10.** 数组类型的表达式仅能参与如下运算：类型转换、下标。

**12.11.** 函数形参不能被声明为数组，传参只能传指针。
> C 允许 `int foo(int a[]);` 和 `int bar(int b[5]);` 但我们不允许。

**12.12.** （更新 11.5）指针可参加加减运算，允许 int 加指针和指针加 int，以及指针减 int（不允许 int 减指针）。
    运算结果的类型和指针操作数的类型相同。
    实际运算时，int 操作数需要乘上指针基类型的大小。
> 例如 `int **p`（考虑到 `sizeof(int*) == 4`），那么 `p-2` 等价于 `p+-2`，其汇编类似 `addi result, p, -8`。

**12.13.（更新** 11.5）允许两个指针相减，但两个指针类型必须相同。
    `a` 和 `b` 是同类型的指针，那么 `a-b` 的结果 `c` 是一个 int，且满足 `a == b+c`。

**12.14.** 空指针参与任何指针算术都是未定义行为。

**12.15.** 指针运算越界，按照 11.8 是未定义行为。但有特例：允许越界一个元素。
> 例如如下代码是合法的
> ```
> int a[10]; int *p=(int*) a;
> for (int *q=p; q != p+10; q=1+q) *q=0;
> ```
> 哪怕其中 `p+10` 已经越界了。
