# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step10 语法规范

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
    : type Identifier ('=' expression)? ';'

expression_list
    : (expression (',' expression)*)?

expression
    : assignment

assignment
    : conditional
    | Identifier '=' expression

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

primary
    : Integer
    | '(' expression ')'
    | Identifier
```

## step10 语义规范

**10.1** 对于全局变量的初始化，我们仅对初始化表达式是整数字面量的情况做要求（例如 `2123`），对初始化表达式是非字面量的情况不做任何要求（例如 `a` 或 `f()` 或 `2+3`）。

> C 其实也支持非字面量的编译期常量，例如 `int a=1+3;`。编译器可以计算出 `1+3==4` 然后让它等价于 `int a=4;`。 但为了实现简便，我们就不要求支持这点。
>
> C 不允许 `int a=f();` 因为 `f()` 不是编译器常量； 而 C++ 甚至可以支持 `int a=f();`，其大致实现为 `int a=0;` 然后在 `main` 之前执行的初始化函数中 `a=f();`。

**10.2** 我们对全局变量的重复声明不做任何要求或限定；但全局变量不能被重复定义，即不能有同名的被初始化的全局变量。

> `int a; int a=2; int a; int main(){ return a;}` 是合法的 C 代码，不过不是合法的 C++ 代码，也许 C++ 的处理方式更符合你的直觉。
>
> 为了简单，我们不要求这点。比如对于形如 `int a; int a=2;` 或 `int a; int a;` 的代码片段，你可以以任意方式处理。

**10.3** 如果一个全局变量没有被初始化，我们认为其拥有一个默认初始值 0。

