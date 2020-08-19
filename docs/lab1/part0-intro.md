# Lab1：整数

这是关于编写minidecaf编译器的第一个步骤。

编写minidecaf编译器是参考了使用Abdulaziz Ghuloum的[An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)和Nora Sandler的[Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)作为路线图。这里的minidecaf语言基本上是C语言的一个子集。你通过从编译minidecaf源语言的一个微不足道的子集开始，能够生成[RISC-V汇编代码](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-intro.md)，并能在RISC-V机器（目前是基于QEMU模拟器）上运行/测试你写的编译器生成的最终机器代码。然后你再一步一步地添加新的语言特性。在第一步中，你只是返回常量；在后面的步骤中，你处理加法和减法；以此类推。每一步都小到足以让人感觉到易于管理，而在每一步结束时，你都有一个可以工作的编译器。另外，通过足够详尽的[测试程序](https://github.com/decaf-lang/minidecaf-tests)，你可以随时验证你的编译器在每次更新后是否正常工作。

# 前言

在你开始之前，你需要决定两件事：用什么语言来写你的编译器，以及如何处理词法分析（lexing）和语法解析（parsing ） 。你可以用任何你喜欢的语言来实现编译器

> 提示：建议使用具有和[sum type](https://chadaustin.me/2015/07/sum-types/)和模式匹配（ pattern matching）的语言，比如OCaml、Haskell或Rust。如果你这样做的话，构建和遍历一个AST会变得更加简单。前提是你能接受学习和掌握这些编程语言的所投入的时间与精力。

你还需要决定是自己写语法解析器和词法分析器，还是使用自动解析器和扫描器生成器（例如[flex](https://github.com/westes/flex)，[bison](https://www.gnu.org/software/bison/)，[antlr4](https://www.antlr.org)）。在整个实验环节中，两种方式都会提供。我们将展示如何手工编写一个词法器（或扫描器）和递归下降解析器。使用解析器生成器可能更容易，缺点是了解底层运行细节和调试bug可能会困难一些。如果能够直接设计实现解析器生成器，那么对编译课上讲的很多原理、算法的理解会更加深入。

> 注意：设计实现解析器生成器不是基本实验要求。

本阶段我们将编译一个返回单个整数的minidecaf程序。我们还将建立编译器的三个基本阶段（pass）：词法、解析和代码生成。。第一步将有比较大的工作量，即建立了一个编译器的框架，该框架将使以后添加更多语言特性变得容易，对后续实验步骤有较大的帮助，

下面是一个我们要编译的程序 return_2.c

```
int main() {
    return 2;
}
```

我们将只处理有一个函数 "main "的程序，它由一个返回语句组成。唯一不同的是返回的整数的值，我们不会处理十六进制或八进制的整数，只处理十进制。我们不会处理十六进制或八进制的整数，只处理十进制。为了验证你的编译器是否正常工作，你需要编译一个程序，运行它，并检查它的返回代码。

```
$ YOUR_COMPILER return_2.c # 用例的编译器会把return_2.c编译为 return.s 汇编程序
$ riscv64-unknown-elf-gcc return_2.s -o return_2 # riscv-64汇编器把return.s翻译为return_2执行程序
$ qemu-riscv64 ./return_2 # 用QEMU for riscv-64硬件模拟器运行return_2执行程序
$ echo $? # 检查return_2执行程序的执行结果，应该是 2
2 
```

你的编译器会产生risc-v汇编代码。我们不会自己将汇编文件转化为可执行文件--那是汇编器和链接器的工作（最好有个链接介绍汇编器和连接器）。为了看看这个程序在汇编中的样子，让我们用GCC来编译它。

```
$ riscv64-unknown-elf-gcc -S -O3 return_2.c
$ cat return_2.s
    .section __TEXT,__text_startup,regular,pure_instructions
    .align 4
    .globl _main
_main:
    movl    $2, %eax
    ret
    .subsections_via_symbols
```

现在，让我们看看汇编程序本身。我们可以忽略`.section`、`.align`和`.subsections_via_symbols`指令，这些汇编原语可参加[这里的介绍](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-directives.md)。--如果你删除它们，你仍然可以生成并运行return_2执行程序。`.globl main`表示`main`符号应该对链接器可见，否则它找不到程序的入口点。

最后，我们有了实际的汇编指令。

```
main:                  ; label for start of "main" function
    movl    $2, %eax    ; move constant "2" into the EAX register
    ret                 ; return from function
```

这里最重要的一点是，当一个函数返回时，XXX寄存器[5](https://norasandler.com/2017/11/29/Write-a-Compiler.html#fn5)将包含其返回值。`main`函数的返回值将是程序的退出代码。在上面的汇编片段中，唯一可以改变的是返回值。

> 注意：在实验指导中，将使用AT&T汇编语法。每当你在阅读汇编时，请确保你知道它使用的是什么语法!

