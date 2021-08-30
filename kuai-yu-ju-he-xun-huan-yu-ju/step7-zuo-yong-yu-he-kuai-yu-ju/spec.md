# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step7 语法规范

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

## step7 语义规范

**7.1** 根据其声明的位置，每一个标识符都属于一个作用域。目前我们有两种作用域：文件级和块级。如果是在块中声明，则标识符其声明所属的块的作用域中，例如局部变量；否则标识符在文件级（全局）作用域中，例如全局变量。

**7.2** （更新 5.6）如果一个标识符在两个作用域里面，这两个作用域必然是嵌套的，即一个内层作用域完全被另一个外层作用域所覆盖。且在内层作用域中，外层作用域里该标识符所指派（designate）的变量或函数是不可见的。

> 在初始化表达式中，其正在初始化的变量已被声明，会隐藏（shadow）外层作用域的同名变量，但其值不确定。例如在下面的代码片段中，`a + 1` 的值是不确定的。
>
> ```text
> int a = 1;
> {
>   int a = a + 1;
> }
> ```

**7.1** （更新 5.3）对于同一个标识符，在同一个作用域中至多有一个声明。

**7.3** （更新 5.4）使用不在当前开作用域中的变量名是不合法的。

