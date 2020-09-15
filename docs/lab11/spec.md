# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step11 语法规范
灰色部分表示相对上一节的修改。
<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">function</span> <span class="SpecOperator">|</span> <span class="SpecRule">declaration</span><span class="SpecOperator">)*</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">parameter_list</span> <span class="SpecToken">')'</span> <span class="SpecOperator">(</span><span class="SpecRule">compound_statement</span> <span class="SpecOperator">|</span> <span class="SpecToken">';'</span><span class="SpecOperator">)</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">type</span> <span class="SpecToken">'*'</span>
</div>
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
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecOperator">(</span><span class="SpecToken">'='</span> <span class="SpecRule">expression</span><span class="SpecOperator">)?</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">expression_list</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">expression</span> <span class="SpecOperator">(</span><span class="SpecToken">','</span> <span class="SpecRule">expression</span><span class="SpecOperator">)*)?</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">assignment</span>

<span class="SpecRuleStart">assignment</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">conditional</span>
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecRule">unary</span> <span class="SpecToken">'='</span> <span class="SpecRule">expression</span>
</div>
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
<div class="changed"><span class="SpecRuleIndicator">    |</span> <span class="SpecOperator">(</span><span class="SpecToken">'-'</span><span class="SpecOperator">|</span><span class="SpecToken">'~'</span><span class="SpecOperator">|</span><span class="SpecToken">'!'</span><span class="SpecOperator">|</span><span class="SpecToken">'&amp;'</span><span class="SpecOperator">|</span><span class="SpecToken">'*'</span><span class="SpecOperator">)</span> <span class="SpecRule">unary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">type</span> <span class="SpecToken">')'</span> <span class="SpecRule">unary</span>
</div>
<span class="SpecRuleStart">postfix</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">primary</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression_list</span> <span class="SpecToken">')'</span>

<span class="SpecRuleStart">primary</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">'('</span> <span class="SpecRule">expression</span> <span class="SpecToken">')'</span>
<span class="SpecRuleIndicator">    |</span> <span class="SpecToken">Identifier</span>
</pre>

# step11 语义规范
**11.1.** 构成左值表达式的必要条件除了能通过 5.5 中两条外新增一条：
* 如果 `e` 是类型为 `T*` 的表达式，那么 `*e` 是类型为 `T` 的左值。
> 因此 `int a; *&a=2;` 中 `*&a` 是左值。

**11.2.** step11 中类型只有 int 和指针类型。禁止隐式类型转换，但允许显式类型转换，只要不违反其他几条规范。

**11.3.** `&` 的操作数必须是左值。
> 所以 `&*e` 等价于 `e`，但它不是左值了

**11.4.** `*` 的操作数类型必须是指针类型。

**11.5.** 指针类型的表达式仅能参与如下运算：类型转换、（一元）`&`、`*`、六种二元比较运算（`<`，`<=`，`>=`，`>`，`==`，`!=`）、`=`。
    指针不得参与乘除模和、一元、逻辑运算。但是除了两种相等性比较之外，其他四种比较运算的结果是未定义的。
> 参与赋值和比较运算的指针类型必须相同，例如不能把`int **`赋值给`int *`，也不能比较`int **`和`int *`。
> 
> 四种涉及大小关系的比较运算结果是未定义的，这个规则的意义在于，我们对变量在内存中的排布顺序不做出任何要求。
> 例如程序`int main() { int a; int b; return a < b; }`中，`a`和`b`谁在栈中地址较高都可以，所以`a < b`的结果是0和1都可以。
> 
> step12 会支持指针的算术运算。step12引入数组后，指向同一数组的指针之间的大小关系也有了明确定义。

**11.6.** 所有涉及条件表达式的地方，包括if，?:运算符，循环，条件表达式的类型都必须是整数。

**11.7.** 空指针是值为 0 的指针。
    因为禁止隐式类型转换，所以空指针字面量必须由 0 显示转换而来，例如 `(int*) 0`。
    判断空指针类似：`if (p == (int**)0) ;` 或 `if ((int)p = 0) ;`。

**11.8.** 未对齐的指针是未定义行为。就 MiniDecaf 而言，指针必须对齐到 4 字节边界，即如果把一个指针转化为整数，那么结果必须是4的整数倍，否则是未定义行为。

**11.9.** 如果指针类型和被指向的对象的类型不匹配（例如 step12 的数组/指针越界），对这样的指针解引用就是未定义行为。
    这样的指针也包含空指针，所以空指针解引用是未定义行为。
> 所以 `int a; int *p = (int*)a; int x=&*p;` 没有包含未定义行为，但 `int y=*p;` 包含了未定义行为。
>
> 这里我们其实和 C 不同，C 中只要指针指向的地方的值的类型和指针的不匹配就是未定义行为，但我们只要不解引用都可以。

