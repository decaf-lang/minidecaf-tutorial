# Java-ANTLR
这个文档用来介绍 Java-ANTLR，以及解释它的实现和指导书的不同。

## 概述
本参考实现基于 Java （JDK 1.4）语言和 [Gradle](https://gradle.org/) 项目构建工具，使用 [ANTLR](https://www.antlr.org/) 工具进行词法语法分析。

本参考实现具有以下特点：
- **基于ANTLR的词法语法分析**，并且使用 Gradle 的 ANTLR 插件，十分简单易用；
- **单遍遍历**，代码很短。

本框架预计会有 12 个 commit 来展现完成每个 step 的过程，不过助教还在整理代码，目前整理到了 step 1 (updated at 9.15)。

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

本参考框架在分析树上单遍遍历直接生成汇编代码，所以没有 IR。

TODO: 关于后续步骤的更详细的区别会在之后更新。