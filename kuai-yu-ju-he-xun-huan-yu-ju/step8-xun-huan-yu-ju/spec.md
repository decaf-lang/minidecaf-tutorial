# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step8 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : function

function
    : type Identifier '(' ')' compound_statement

type
    : 'int'

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

## step8 语义规范

> 方便起见，我们称 for 循环括号中的三个表达式/声明自左向右依次为 init、ctrl 和 post。 例如 `for (i=0; i<100; i=i+1);` 中，`i=0` 是 init，`i<100` 是 ctrl，`i=i+1` 是 post。

**8.1** 有三种循环语句：for 循环、while 循环和 do 循环。执行一条循环语句，意味着反复执行一条语句（即循环体），直到其控制表达式等于 0。

**8.2** while 循环的控制表达式的求值在循环体的每次执行之前。

**8.3** do 循环的控制表达式的求值在循环体的每次执行之后。

**8.4** 对于 for 循环而言：如果 init 是一个声明，其声明发生在控制表达式的第一次求值之前；如果 init 是一个表达式，其求值会在控制表达式的第一次求值之前。ctrl 即是控制表达式，其求值在循环体的每次执行之前。post 的求值在循环体的每次执行之后。

**8.5** for 循环的 init、ctrl 和 post 都可以被省略。省略 ctrl 等价于将其替换为一个非零常数，比如 1。

**8.6** 循环语句有其自己的作用域，且是它所在的作用域的子集。循环体也有其作用域，且是循环语句的作用域的子集。如果 for 循环的 init 是一条声明，则其所声明的变量所属的作用域是整个 for 循环语句的作用域（包含 init、ctrl、post 和循环体）。

> 例如，`for (int i=0;;i=i+1) { int i=1; return i; }` 是合法的代码片段。

**8.7** continue 语句和 break 语句要么出现在循环体里，要么其就是循环体。

**8.8** 执行一条 continue 语句，意味着将程序的执行跳转至该条 continue 语句所在的最小的循环语句的循环体的末尾。

> 例如，`for (int i=0;i<100;i++) { s+=i; continue; }` 等价于 `for (int i=0;i<100;i++) { s+=i; }`。

**8.9** 执行一条 break 语句，意味着终止该条 break 语句所在的最小的循环语句的执行。

