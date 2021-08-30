# 任务概述

step11 支持的是数组和指针算术：

语法上没有太大改动， 1. 数组的声明：

```text

declaration
    : type Identifier ('[' Integer ']')* ('=' expression)? ';'
```

1. 数组和指针的下标操作

   ```text

   postfix
       : primary
       | Identifier '(' expression_list ')'
       | postfix '[' expression ']'
   ```

2. 指针算术：语法不变，但允许：指针加/减整数、整数加指针、指针减指针了。

step11 难度不大，但有了数组让我们能够写很多有意思的程序了，step11 之前甚至 MiniDecaf 连快速排序都写不了。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

