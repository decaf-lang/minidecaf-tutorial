# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step9 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : function*

function
    : type Identifier '(' parameter_list ')' compound_statement

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

> 我们暂不要求支持不包含函数体的函数声明。

## step9 语义规范

**9.1** 在函数调用中，实参和形参的参数个数必须相同，同一位置的参数类型也必须相同。

**9.2** 在准备函数的调用时，所有的实参会被求值，然后赋给相应位置上的形参。

> 在函数体中，形参的值可能会被改变，但即便实参是一个可修改的左值，被调用函数中形参的改变也不会影响实参的值。

**9.3** 函数是可以递归调用的。

**9.4** （更新 5.10）执行一条 `return` 语句，意味着终止当前函数的执行，并将控制权交还给调用当前函数的 caller，语句中的表达式的值会返还给 caller 作为函数调用的表达式的值。一个函数可以有任意多条 `return` 语句。

**9.5** 函数的形参可以被视为在函数体的开头被定义（被以实参的值初始化）的局部变量。所有形参均为左值，且不能被在函数体中直接重定义（除非是在一个更小的嵌套的块中）。

> 例如，`int f(int x) { int x; }` 不合法，但 `int f(int x) { { int x; } }` 合法。

**9.6** 如果一个不是 `main` 的函数执行到了它的 `}`，且其返回值被 caller 所使用，则这是一个未定义行为。

> 对于感兴趣的同学：C 语言中规定只有使用了返回值才是未定义行为，而 C++ 中规定不管返回值有没有被使用，都是未定义行为。
>
> 我们没有支持 void 类型，但可以忽略返回值达到类似的效果。
>
> “执行到了 `}`” 意味着执行时没有通过 `return` 返回，例如 `int f(){if(0) return 0;}`。
>
> 实现的时候，你可以直接让所有函数都默认返回 0，语义规范说 main 之外的函数没有 return 是未定义行为，未定义行为的意思就是你想怎么处理都可以，所以全部默认返回 0 当然也是可以的，而且更清晰简单。

