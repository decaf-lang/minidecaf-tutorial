### 词法语法分析

本步骤引入了全局变量的概念。这意味着你可以将变量声明和初始化放在函数外进行，在本步骤中你将修改之前的文法规定，支持全局变量的声明和初始化。

> 注：因词法分析部分需要解释的东西较少，我们将词法和语法分析合为一个文件，但需要注意的是，它们是相互独立的操作流程。

#### 词法分析

本步骤无新增 Token 定义，目前的 Token 列表为：

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
, 
```

#### 语法分析

本步骤新增了对于全局变量的支持，因此现在位于最顶层的声明有**函数声明和变量声明**两种，之前的顶层声明需要加入对变量声明的支持，我们修改文法如下：

```
<program> ::= { <function> } // <= 原有文法
<program> ::= { <function> | <declaration> } // <= 修改后文法，增加支持变量声明
```

在修改了文法定义之后，我们的顶层 AST 会发生一些变化：

```
// 修改前 AST
program = Program(function_declaration list)

// 修改后 AST
toplevel_item = Function(function_declaration)
              | Variable(declaration)
toplevel = Program(toplevel_item list)
program = Program(function_declaration list)
```

