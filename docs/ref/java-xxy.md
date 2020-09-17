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

## 与实验指导的区别

本参考框架在分析树上单遍遍历直接生成汇编代码，所以没有 IR、语义检查等中间阶段。

### 局部变量（step 5）

为了在函数的序言部分为局部变量开出足够大的栈空间，我们需要使用 **代码回填**，也就是在遍历完函数体，计算出局部变量的数量 x 和其所占的内存空间 y = 4x，再将 `addi sp, sp, -y`。

### 调用约定（step 9）

本参考实现遵循了 step 9 中描述的 GCC 调用约定。
