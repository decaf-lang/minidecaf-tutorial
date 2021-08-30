# 任务概述

step4 我们要增加的是：

1. 比较大小和相等的二元操作：`<`、`<=`、`>=`, `>`, `==`, `!=`  equality  : relational  \| equality \('=='\|'!='\) relational

   relational  : additive  \| relational \('&lt;'\|'&gt;'\|'&lt;='\|'&gt;='\) additive&lt;/div&gt;&lt;/pre&gt;

2. 逻辑与 `&&`、逻辑或 `||`  expression  : logical\_or

   logical\_or  : logical\_and  \| logical\_or '\|\|' logical\_and

   logical\_and  : equality  \| logical\_and '&&' equality&lt;/div&gt;&lt;/pre&gt;

新特性的语义、优先级、结合性和 C 以及常识相同，例如 `1<3 == 2<3 && 5>=2` 是逻辑真（int 为 `1`）。 但特别注意，C 中逻辑运算符 `||` 和 `&&` 有短路现象，我们不要求。

你需要： 1. 改进你的编译器，支持本节引入的新特性，通过相关测试。 2. 完成实验报告（具体要求请看网络学堂的公告）。

