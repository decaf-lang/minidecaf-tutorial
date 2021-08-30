# 任务概述

这一步我们终于要增加变量了，包括

* 变量的声明
* 变量的使用（读取/赋值）

并且，虽然还只有一个 main 函数，但 main 函数可以包含多条语句和声明了。

为了加入变量，我们需要确定：变量存放在哪里、如何访问。 为此，我们会引入 **栈帧** 的概念，并介绍它的布局。

语法上，step5 的改动如下：

```text


function
    : type Identifier '(' ')' '{' statement* '}'

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


primary
    : Integer
    | '(' expression ')'
    | Identifier
```

并且我们也要增加语义检查了：变量不能重复声明，不能使用未声明的变量。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

