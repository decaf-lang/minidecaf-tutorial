# 规范

## 规范

每个步骤结尾的 **规范** 一节都会对这个步骤中的新特性给出规范，方便大家查阅。

## step3 语法规范

灰色部分表示相对上一节的修改。

```text


program
    : function

function
    : type Identifier '(' ')' '{' statement '}'

type
    : 'int'

statement
    : 'return' expression ';'

expression
    : additive

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
```

## step3 语义规范

**3.1** 二元操作符 `*` 的结果是操作数的乘积。

**3.2** 二元操作符 `/` 的结果是第一个操作数除以第二个操作数所得的商的整数部分（即所谓“向零取整”），二元操作符 `%` 的结果是第一个操作数除以第二个操作数所得的余数。在两种操作中，如果第二个操作数为 0，则其行为都是未定义的。当 `b` 不为 0 时，表达式 `(a/b)*b + a%b` 应该等于 `a`。

**3.3** 二元操作符 `+` 的结果是操作数的和。

**3.4** 二元操作符 `-` 的结果是第一个操作数减去第二个操作数所得的差。

**3.5** 除非特别声明，子表达式求值顺序是**未规定行为**（unspecified behavior），即其行为可以是多种合法的可能性之一。也就是说，以任意顺序对子表达式求值都是合法的。 例如：执行 `int a=0; (a=1)+(a=a+1);` 之后 a 的值是未规定的（待我们加上变量和赋值运算符后，这个问题才会产生真正切实的影响）。

