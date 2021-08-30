# 任务概述

step6 我们要支持 if 语句和条件表达式（又称三元/三目表达式，ternary expression）。

语法上的改动是：

1. if 表达式

   ```text

   statement
       : 'return' expression ';'
       | expression? ';'
       | 'if' '(' expression ')' statement ('else' statement)?
   ```

2. 条件表达式

   ```text

   assignment
       : conditional
       | Identifier '=' expression

   conditional
       : logical_or
       | logical_or '?' expression ':' conditional
   ```

3. `block_item`：为了下一阶段做准备

   ```text

   function
       : type Identifier '(' ')' '{' block_item* '}'

   block_item
       : statement
       | declaration
   ```

if 语句的语义和 C 以及常识相同，条件表达式优先级只比赋值高。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

