# Java-ANTLR
这个文档用来介绍 Java-ANTLR，以及解释它的实现和指导书的不同。

## 概述
本参考实现基于 Java （JDK 1.4）语言和 [Gradle](https://gradle.org/) 项目构建工具，使用 [ANTLR](https://www.antlr.org/) 工具进行词法语法分析。

本参考实现具有以下特点：
- **基于ANTLR的词法语法分析**，并且使用 Gradle 的 ANTLR 插件，十分简单易用；
- **单遍遍历**，代码比较短，但逻辑比较糅杂。

## 环境配置

可见于[这里](https://github.com/decaf-lang/minidecaf/blob/md-xxy/README.md)。

## 代码结构

下面是最终完整实现的 minidecaf 编译器中的代码结构

```
src/main
├── antlr/minidecaf/
│   └── MiniDecaf.g4        ANTLR 语法文件
├── java/minidecaf/
│   ├── Main.java           主体驱动部分
│   ├── MainVisitor.java    主体编译逻辑
│   ├── Type.java           基本类型，包括“无类型”、整型和指针
│   ├── FunType.java        函数类型
│   └── Symbol.java         符号
├── build.gradle            gradle 构建脚本
└── settings.gradle         gradle 配置文件
```

## 与总实验指导的区别

本参考框架在分析树上单遍遍历直接生成汇编代码，所以没有语义检查、生成 IR 等中间阶段，所以与总实验指导差别很大，建议大家优先阅读参考代码相邻版本之间的 diff 和参考代码中的注释。

### 局部变量（step 5）

由于我们只有单遍遍历，在遍历函数体之前不可能知道函数体中局部变量的数量。

为了在函数的序言部分为局部变量开出足够大的栈空间，我们需要使用 **代码回填** 技术。也就是在遍历完函数体，计算出局部变量的数量 x 和其所占的内存空间字节数 y = 4x，再将 `addi sp, sp, -y` 插入到函数序言中。

### 调用约定（step 9）

本参考实现遵循了 step 9 中描述的 GCC 调用约定。

### 全局变量（step 10）

为方便理解，我们会将全局变量放在一个单独的符号表里。

“全局变量的初始值只能是整数字面量”这一点我们不作为语义规范，而是直接将其在语法层面避免。我们会将 `declaration` 分为 `localDecl` 和 `globalDecl` 两种不同的非终结符，然后约定 `globalDecl` 的初始化表达式只能是一个整数字面量。

所以，本参考实现的语法相较于语法规范会在以下相应部分有所修改。

```
program:
	(function | globalDecl)*

block_item:
	statement
    | localDecl

globalDecl:
	type Identifier ('=' Integer)? ';'

statement:
	'for' '(' localDecl expression? ';' expression? ')' statement

localDecl:
	type Identifier ('=' expr)? ';'
```

### 指针（step 11）

由于我们只有单遍遍历，无法采用主指导书中对左值的处理方式（无法知道一个地方是否 **需要** 左值）。所以我们这里会使用另一种方式：

对于左值，我们会优先在栈中保留其地址，在需要用到其值的时候才将其值从地址中读出（将左值转换为右值）。
