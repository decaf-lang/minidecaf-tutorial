# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step5 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : function

function
    : type Identifier '(' ')' '{' statement* '}'

type
    : 'int'

statement
    : 'return' expression ';'
    | expression? ';'
    | declaration

declaration
    : type Identifier ('=' expression)? ';'

expression
    : assignment

assignment
    : logical_or
    | Identifier '=' expression

logical_or
    : logical_and
    | logical_or '||' logical_and

logical_and
    : equality
    | logical_and '&&' equality

equality
    : relational
    | equality ('=='|'!=') relational

relational
    : additive
    | relational ('<'|'>'|'<='|'>=') additive

additive
    : multiplicative
    | additive ('+'|'-') multiplicative

multiplicative
    : unary
    | multiplicative ('*'|'/'|'%') unary

unary
    : primary
    | ('-'|'~'|'!') unary

primary
    : Integer
    | '(' expression ')'
    | Identifier
```

## step5 语义规范

**5.1** 每一条变量声明（定义）指定了对标识符的解释和属性。当变量被定义时，应当有一块存储空间为这个变量所保留。当变量声明之后，若与这个变量的名称相同的标识符作为操作数（operand）出现在一个表达式中时，其就应被指派（designate）为这个变量。

**5.2** 变量的初始化表达式指定了变量的初始值。

**5.3** 同一个标识符应只能作为至多一个变量的名字，即是说，不允许声明重名变量。

**5.4** 对未声明的变量的使用是错误。

**5.5** 没有被初始化的（局部）变量的值是不确定的。

> 在初始化表达式中，正在被初始化的变量已被声明，但其值尚未被初始化。 例如，`int a = a + 1;`，这样一条声明在语义上等价于 `int a; a = a + 1;`

**5.6** 局部变量的名字可以为 `main`。

**5.7** 赋值运算 `=` 的左操作数必须是一个**可修改的左值**（modifiable lvalue）。**左值**（lvalue）即一个会被指派为某个变量的表达式，如在 `int a; a = 1;` 中，`a` 即是一个会被指派为变量的表达式。的左值**可修改**是指被指派的变量不能是一个左值数组。

> 就 step5 来说，这一点其实几乎已经被语法保证，因为其 `=` 的左边只能是一个标识符，只需再要求其是一个已经声明过的变量的名字即可。 详见后面 step12 的讨论。

**5.8** 在赋值运算（`=`）中，右操作数的值会被存在左操作数所指派的变量中。

**5.9** 赋值表达式的结果，为赋值运算完成后左操作数所指派的变量的值，但这个结果本身并非左值。

**5.10** 一个函数中可以有任意多条 `return` 语句。

**5.11** 当 `main` 函数执行至 `}` 时，应终止执行并返回 0。

