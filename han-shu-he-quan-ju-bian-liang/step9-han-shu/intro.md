# 任务概述

step9 开始，我们要支持多函数了。

1. 我们需要支持函数的声明和定义：  program  : function\*

   function  : type Identifier '\(' parameter\_list '\)' \(compound\_statement \| ';'\) &lt;/div&gt; parameter\_list : \(type Identifier \(',' type Identifier\)\*\)? &lt;/pre&gt;

2. 我们还需要支持函数调用： expression\_list : \(expression \(',' expression\)\*\)? unary  : postfix  \| \('-'\|'~'\|'!'\) unary

   postfix  : primary  \| Identifier '\(' expression\_list '\)' &lt;/div&gt; &lt;/pre&gt;

语义检查部分，我们需要检查函数的重复定义、检查调用函数的实参（argment）和形参（parameter）的个数类型一致。 我们不支持 void 返回值，直接忽略 int 返回值即可。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

