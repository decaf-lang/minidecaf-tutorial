# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step11 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : (function | declaration)*

function
    : type Identifier '(' parameter_list ')' (compound_statement | ';')

type
    : 'int'

parameter_list
    : (type Identifier (',' type Identifier)*)?

compound_statement
    : '{' block_item* '}'

block_item
    : statement
    | declaration

statement
    : 'return' expression ';'
    | expression? ';'
    | 'if' '(' expression ')' statement ('else' statement)?
    | compound_statement
    | 'for' '(' expression? ';' expression? ';' expression? ')' statement
    | 'for' '(' declaration expression? ';' expression? ')' statement
    | 'while' '(' expression ')' statement
    | 'do' statement 'while' '(' expression ')' ';'
    | 'break' ';'
    | 'continue' ';'

declaration
    : type Identifier ('[' Integer ']')* ('=' expression)? ';'


expression_list
    : (expression (',' expression)*)?

expression
    : assignment

assignment
    : conditional
    | unary '=' expression


conditional
    : logical_or
    | logical_or '?' expression ':' conditional

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
    : postfix
    | ('-'|'~'|'!') unary

postfix
    : primary
    | Identifier '(' expression_list ')'
    | postfix '[' expression ']'

primary
    : Integer
    | '(' expression ')'
    | Identifier
```

## step11 语义规范

**11.1** 一个数组类型描述了一组被连续分配在一段内存空间中的对象，所有对象都具有相同的类型（我们称之为**元素类型**）。数组类型包含两部分：元素类型，和数组的长度（即元素数量）。数组类型的表达式仅能参与下标运算。

**11.2** 我们仅要求支持固定长度的数组，即在数组的声明中，其长度是一个正整数字面量。

> 所以，我们不要求支持变长数组 `int a[n];` 或不定长数组 `int a[];`。

**11.3** 我们不要求支持数组的初始化。

> C 中可以写 `int a[2]={1, 2}`，但简单起见，我们不做要求。
>
> 由于我们不要求数组的初始化，根据 5.5，作为局部变量的数组中的元素初始值未定；根据 10.3，作为全局变量的数组中的元素初始值为 0。

**11.4** 对于下标运算 `a[b]`，要求 `a` 是一个数组类型，`b` 是一个整数类型，`a[b]` 是 `a` 中的第 `b` 个元素（从 0 开始计数）。

**11.5** 下标运算越界是未定义行为。

> 即便是类似 `int a[4][5]; a[1][7]` 这种，同样也是未定义行为。

