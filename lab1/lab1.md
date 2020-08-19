> 注：这只是一份草稿。

# 编写minidecaf编译器-step1

这是关于编写minidecaf编译器的第一个步骤。

minidecaf编译器参考了Abdulaziz Ghuloum的[An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)和Nora Sandler的[Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)作为路线图。大致来讲，minidecaf语言是C语言的一个子集。你将从编译minidecaf源语言的一个微不足道的子集开始，能够生成[RISC-V汇编代码](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-intro.md)，并能在RISC-V机器（目前是基于QEMU模拟器）上运行/测试你写的编译器生成的最终机器代码。然后你再一步一步地添加新的语言特性，直至实现一个足够完整的 minidecaf 语言。在第一步中，你只是返回常量；在后面的步骤中，你处理加法和减法；等等。每一步都会小到让人感觉易于管理，在每一步结束时，你都会有一个可以工作的编译器。另外，通过足够详尽的[测试](https://github.com/decaf-lang/minidecaf-tests)，你可以随时验证你的编译器在每次更新后是否正常工作。

## 前言

本框架使用Java语言，最前端使用[ANTLR](https://www.antlr.org)来作词法和语法解析，ANTLR是一个语法解析器生成器（parser generator），你只需要写出你的词法和语法，ANTLR便会为你生成一棵分析树（parse tree），并提供遍历分析树的接口。在本框架中，我们会使用ANTLR的visitor模式，它基于Java的访问者模式（visitor pattern），简单来说这是一种遍历由不同类型的节点组成的树的方式，你需要先对此有一定的了解。与其他框架不同的是，为了简便起见，本框架只有一个阶段，你将会直接从分析树生成RISCV汇编。

（也许我们应该提供*The definitive ANTLR 4 reference*）

## 环境配置

我觉得配环境真的好难，我也还不太会，这肯定是要讲一下的吧QAQ
- JDK and Gradle
- ANTLR and ANTLR Plugin
- RISCV Toolkit (Cross Compiler & Simulator)：这个我们会提供

## 第一步 : 整数

下面是一个我们要编译的程序 return_2.c

```c
int main() {
    return 2;
}
```

在一开始，我们将只处理只有一个 main 函数的程序，它由一个返回语句组成。唯一不同的是返回的整数的值，我们只处理十进制。

我们先来看看我们期望达成的效果是什么样的，为了验证你的编译器是否正常工作，你需要编译一个程序，运行它，并检查它的返回代码。

```bash
$ YOUR_COMPILER return_2.c # 用例的编译器会把return_2.c编译为 return.s 汇编程序
$ riscv64-unknown-elf-gcc return_2.s -o return_2 # riscv-64汇编器把return.s翻译为return_2执行程序
$ qemu-riscv64 ./return_2 # 用QEMU(riscv-64)硬件模拟器运行return_2执行程序
$ echo $? # 检查return_2执行程序的执行结果，应该是 2
2 
```

你的编译器会产生risc-v汇编代码。我们不会自己将汇编文件转化为可执行文件--那是汇编器和链接器的工作（最好有个链接介绍汇编器和连接器）。为了看看这个程序在汇编中的样子，让我们先来用gcc来编译它。

```bash
$ riscv64-unknown-elf-gcc -S -O3 return_2.c
$ cat return_2.s
        .file   "return_2.c"
        .option nopic
        .text
        .align  1
        .globl  main
        .type   main, @function
main:
        addi    sp,sp,-16
        sd      s0,8(sp)
        addi    s0,sp,16
        li      a5,2
        mv      a0,a5
        ld      s0,8(sp)
        addi    sp,sp,16
        jr      ra
        .size   main, .-main
        .ident  "GCC: (GNU) 8.2.0"
```

这些汇编原语可参见[这里的介绍](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-directives.md)，但其中大部分我们暂且无需关心（因为我也看不懂QAQ），我们可以将其简化一下。

最后，我们有了实际的汇编指令。

```asm
	.globl	main # 让 main 这个标签对链接器可见
main: # 一个用于标示主函数入口地址的标签
	li	a0,2 # 将 2 载入寄存器 a0
	ret # jr ra 的缩写，也就是从当前函数中返回，返回值存在 a0 中
```

## ANTLR 简介

我们或许不需要全面地讲解 ANTLR，但也许还是需要简单讲一下我们会如何使用 ANTLR，以及我们会如何使用 Visitor Pattern。

## 词法分析

词法分析器（也叫扫描器或标记器）是编译器的一个阶段，它将一个字符串（源代码）分解成一个标记列表（token list）。一个标记（token）是语法解析器（parser）能够理解的最小单位——如果一个程序就像一个段落，那么标记就像一个个单词。变量名（variable names）、关键字（keywords）、常量（constants）以及像括号（braces）这样的标点符号都是标记的例子。下面是 return_2.c 中所有标记的列表。

不过，antlr 会帮我们自动处理那种只有一个固定值的标记（比如关键字或括号），我们无需再额外关心他们。目前，我们只需要关心两种 token：

```c++
WS: [ \t\r\n\u000C] -> skip; // 空白字符，可以直接忽略
NUM: [0-9]+; // 十进制整数字面量（decimal literal）
```

> 注意：我们不能对负整数进行词法分析。这并不是偶然的，因为C语言没有负整数常量。在C语言中表示负数，需要的是整数常量和一个可以应用于正整数的“负”一元运算符。我们将在下一步添加负一元运算。

## 语法解析

下一步是将我们的标记列表转化为分析树（Parsing Tree），目前我们定义如下的简单语法（方便起见，这里我们直接以 antlr 的语法格式来写了）：

```c++
prog: func;
func: 'int' 'main' '(' ')' '{' stmt '}';
stmt: 'return' expr ';';
expr: NUM;
```

上面的每一行都是一个产生式（*production*），定义了如何从一种形式语言（ANTLR-style Extended Backus-Naur form）来表述另外一个语言（minidecaf）的语法。每一个出现在产生式左侧（也就是`:`左侧）的符号（即`prog`、`func`、`stmt`）都是一个非终结符（non-terminal symbol）。右侧则由终结符（关键字、括号、分号或自定义的词法标记）和非终结符构成。现在的语法非常简单，每个非终结符只有一条产生式。在后续的实验中，一些非终结符将有多个产生式。

ANTLR可以自动生成lexer和parser的代码，你可以粗略地阅读一下生成的代码，了解可用的方法和接口。

## 代码生成

现在我们已经建立了一个分析树，下面就可以来生成汇编代码了！为此，我们将遍历我们的分析树。

下面是一份伪代码

```java
// 在最顶端，我们不做任何操作
visitProg(ProgContext ctx) {
    visit(ctx.func());
}

visitFunc(FuncContext ctx) {
    // 打印 "main" 这个 label，并让其对链接器可见
    print(".global main\n");
    print("main:\n");
    
    // 遍历函数体，在这里就是一个 stmt
    visit(ctx.stmt());

    // 从函数中返回
    print("\tret\n");
}

// 在 stmt 无需任何操作
visitStmt(StmtContext ctx) {
    visit(ctx.expr());
}

visitExpr(ExprContext ctx) {
    // 读取出 NUM，并将其作为 Integer 存下来
    Integer num = Integer.valueOf(ctx.NUM().getText());
    // 载入寄存器 a0
    print("\tli a0, %d\n", num);
}
```

这里我们尚未处理报错，对于超过 64 位整数类型的情况尚没有做任何处理。

## 测试

理想情况下，我们应该是用 GitLab 的 CI 来测试？

## 下一步

在[下一步]()中，我们将增加三个单目运算符：`-`、`~`和`！`。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
