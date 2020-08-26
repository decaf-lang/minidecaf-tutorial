### 词法语法分析

本步骤引入了函数调用的概念。和之前只允许主函数定义不同，在本步骤中你将修改之前的文法规定，允许在一个源程序中声明和定义多个函数，并支持对它们的调用。

> 注：因词法分析部分需要解释的东西较少，我们将词法和语法分析合为一个文件，但需要注意的是，它们是相互独立的操作流程。

#### 词法分析

你需要添加逗号`,`来支持函数参数的分隔，目前的 Token 列表为：

```
{
}
(
)
;
int
return
Identifier [a-zA-Z_][a-zA-Z0-9_]*
Integer literal [0-9]+
-
~
!
+
*
/
&&
||
==
!=
<
<=
>
>=
=
if
else
:
?
for
while
do
break
continue
, // <= 此处为新增Token
```

#### 语法分析

和之前的步骤不同，本步骤添加了对函数调用的支持，因此我们需要处理函数定义以及函数调用。

1. 函数定义

   在此前的步骤中，我们将一个源文件限制为**只可定义一个函数并且函数的声明和定义不可分离**，文法如下：

   ```
   <program> ::= <function>
   <function> ::= "int" Identifier "(" ")" "{" { <block-item> } "}"
   ```

   为了实现正常的函数定义，你**首先**需要添加函数参数列表，支持带参数的函数：

   ```
   <function> ::= "int" Identifier "(" [ "int" Identifier { "," "int" Identifier } ] ")" 
   ```

   **其次**，你需要支持函数的声明和定义分离这一特性。函数声明指在使用该函数前说明其函数名、参数列表以及返回类型，而函数定义指包含函数体的一个完整函数单元，如下例所示，我们首先声明了`foo`函数，并在之后给出了`foo`函数的定义。

   ```C
   int three();
   int three() {
       return 3;
   }
   ```

   **综上**，为了支持函数参数、函数的声明与定义，可以将文法修改为如下所示：

   ```
   <function> ::= "int" Identifier "(" [ "int" Identifier { "," "int" Identifier } ] ")" ( "{" { <block-item> } "}" | ";" )
   ```

   > 注：原则上同一个函数可以声明无数次，但只能定义一次。本实验中对于同名函数的重复声明不做要求，即属于未定义行为，测例中不会出现同名函数重复声明的情况。

2. 函数调用

   函数调用是一个类似这样的表达式：

   ```
   foo(arg1, arg2, ...)
   ```

   它包含了函数名和一个参数列表，和函数声明不同，参数可以为任意形式的表达式，因此我们在处理时将函数名作为`Identifier`元素，参数作为`exp`元素进行处理，语法解析器生成相应的AST节点：

   ```
   exp = ...
       | FunCall(string, exp list) // string is the function name
       ...
   ```

   和前面的步骤一样，作为表达式，函数调用也应该有其优先级，一般函数调用具有尽可能高的优先级，因此在文法中，我们将其添加到`<factor>`规则中：

   ```
   <exp> ::= Identifier "=" <exp> | <conditional-exp>
   <conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]
   <logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
   <logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
   <equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
   <relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
   <additive-exp> ::= <term> { ("+" | "-") <term> }
   <term> ::= <factor> { ("*" | "/") <factor> }
   <factor> ::= <function-call> | "(" <exp> ")" | <unary_op> <factor> | Integer | Identifier
   <function-call> ::= id "(" [ <exp> { "," <exp> } ] ")" // <= 此处为新增文法
   <unary_op> ::= "!" | "~" | "-"
   ```
