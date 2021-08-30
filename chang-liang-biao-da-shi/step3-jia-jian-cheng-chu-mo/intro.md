# 任务概述

step3 我们要增加的是：加 `+`、减 `-`、乘 `*`、整除 `/`、模 `%` 以及括号 `(` `)`。

语法上我们继续修改 `expression`，变成

```text

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

新特性的语义、优先级、结合性和 C 以及常识相同，例如 `1+2*(4/2+1) == 7`。

我们这种表达式语法写法可能比较繁琐，但它有几个好处： 1. 和[C99 标准草案](../../can-kao-zi-liao/reference.md)保持一致 2. 把优先级和结合性信息直接编码入语法里，见[优先级和结合性](qi-ta/precedence.md)一节。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

