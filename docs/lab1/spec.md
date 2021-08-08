# 规范
每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

# step1 语法规范

我们采用 **EBNF (extended Barkus-Naur form)** 记号书写语法规范，采用类似 [ANTLR](./antlr.md#语法规范) 的记号：
* 小写字母打头的是非终结符（如 `program`），大写字母打头的是终结符（如 `Identifier`），可以用字符串字面量表示终结符（如 `'int'`）
* 后面会用到：`(` 和 `)` 表示分组，`|` 表示选择，`*` 零或多次，`+` 一或多次，`?` 零或一次。
  - 很容易通过增加新的非终结符，去掉这些符号。例如 `x+` 就可以被替换成新的非终结符 `y`，并且 `y : x | x y`。

> EBNF 也有很多写法，另一种是用尖括号表示非终结符 `<program> ::= <function>` 等。

<pre id='vimCodeElement'>
<code></code>
<span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">function</span>

<span class="SpecRuleStart">function</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecRule">type</span> <span class="SpecToken">Identifier</span> <span class="SpecToken">'('</span> <span class="SpecToken">')'</span> <span class="SpecToken">'{'</span> <span class="SpecRule">statement</span> <span class="SpecToken">'}'</span>

<span class="SpecRuleStart">type</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'int'</span>

<span class="SpecRuleStart">statement</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">'return'</span> <span class="SpecRule">expression</span> <span class="SpecToken">';'</span>

<span class="SpecRuleStart">expression</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecToken">Integer</span>
</pre>

# step1 语义规范
**1.1** MiniDecaf 的 int 类型具体指 32 位有符号整数类型，范围 [-2^31, 2^31-1]，补码表示。

**1.2** 编译器应当只接受 [0, 2^31-1] 范围内的整数常量, 不支持负整数常量，如果整数不在此范围内，编译器应当报错。引入负号`-`后，可以用负号配合正整数常量来间接表示负整数常量。

**1.3** 如果输入程序没有 `main` 函数，编译器应当报错。
