# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step6 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : function

function
    : type Identifier '(' ')' '{' block_item* '}'

type
    : 'int'

block_item
    : statement
    | declaration

statement
    : 'return' expression ';'
    | expression? ';'
    | 'if' '(' expression ')' statement ('else' statement)?

declaration
    : type Identifier ('=' expression)? ';'

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
    : primary
    | ('-'|'~'|'!') unary

primary
    : Integer
    | '(' expression ')'
    | Identifier
```

> 注意：`if` 的 `then` 分支和 `else` 分支需要是一个语句（statement）而非声明（declaration）。 例如 `if (1) int a;` 不是合法的 MiniDecaf 程序。

## step6 语义规范

**6.1** 条件表达式会先对第一个操作数求值，再根据其值选择计算第二个或第三个操作数。当且仅当第一个操作数的值不等于 0，我们会对第二个操作数求值。当且仅当第一个操作数的值等于 0，我们会对第三个操作数求值。当第一个操作数的值为 0 时，条件表达式的求值结果为第二个操作数所求得的值；当第一个操作数的值非 0 时，条件表达式的求值结果为第三个操作数所求得的值。

> 不论选择第二个操作数或者是第三个操作数去求值，都必须首先计算完第一个操作数，之后才能开始第二个或第三个操作数的求值计算。

**6.2** 对于 if 语句而言，当控制条件不等于 0 时，会执行第一个子句；当控制条件等于 0 时，如果有 else 分支，就会执行第二个语句，否则整个 if 语句的执行便已经完成。

**6.3** 如果出现悬吊 `else`（dangling else），要求 `else` 优先和最接近的没有匹配 `else` 的 `if` 匹配。

> 例如 `if (0) if (0) ; else ;` 等价于 `if (0) { if (0) ; else; }` 而非 `if (0) { if (0) ; } else ;`。

