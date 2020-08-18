
# 编写minidecaf编译器-step1

这是关于编写minidecaf编译器的第一个步骤。

编写minidecaf编译器是参考了使用Abdulaziz Ghuloum的[An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)和Nora Sandler的[Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)作为路线图。这里的minidecaf语言基本上是C语言的一个子集。你通过从编译minidecaf源语言的一个微不足道的子集开始，能够生成[RISC-V汇编代码](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-intro.md)，并能在RISC-V机器（目前是基于QEMU模拟器）上运行/测试你写的编译器生成的最终机器代码。然后你再一步一步地添加新的语言特性。在第一步中，你只是返回常量；在后面的步骤中，你处理加法和减法；以此类推。每一步都小到足以让人感觉到易于管理，而在每一步结束时，你都有一个可以工作的编译器。另外，通过足够详尽的[测试程序](https://github.com/decaf-lang/minidecaf-tests)，你可以随时验证你的编译器在每次更新后是否正常工作。

# 前言

在你开始之前，你需要决定两件事：用什么语言来写你的编译器，以及如何处理词法分析（lexing）和语法解析（parsing ） 。你可以用任何你喜欢的语言来实现编译器

> 提示：建议使用具有和[sum type](https://chadaustin.me/2015/07/sum-types/)和模式匹配（ pattern matching）的语言，比如OCaml、Haskell或Rust。如果你这样做的话，构建和遍历一个AST会变得更加简单。前提是你能接受学习和掌握这些编程语言的所投入的时间与精力。

你还需要决定是自己写语法解析器和词法分析器，还是使用自动解析器和扫描器生成器（例如[flex](https://github.com/westes/flex)，[bison](https://www.gnu.org/software/bison/)，[antlr4](https://www.antlr.org)）。在整个实验环节中，两种方式都会提供。我们将展示如何手工编写一个词法器（或扫描器）和递归下降解析器。使用解析器生成器可能更容易，缺点是了解底层运行细节和调试bug可能会困难一些。如果能够直接设计实现解析器生成器，那么对编译课上讲的很多原理、算法的理解会更加深入。

> 注意：设计实现解析器生成器不是基本实验要求。

# 最简单的实现

本阶段我们将编译一个返回单个整数的minidecaf程序。我们将首先实现一个最简单的能正确运行的编译器，然后再将其重构为一个更有可扩展性的实现。

下面是一个我们要编译的程序：`return_2.c`。

```c
int main() {
    return 2;
}
```

我们将只处理有一个函数 `main` 的程序，它由一个返回语句组成。唯一可变的是返回的整数的值，且只处理十进制。

为了实现一个尽量简单的编译器，我们把 `int`、`main`、`(`、`)`、`{`、`}`、`return`、`;` 全都定义成词法分析器识别的标记（token），另外定义一个整数标记 `Integer` ，识别 `[0-9]+`。最后利用语法解析器解析上下文无关文法：

```
Program ::= "int" "main" "(" ")" "{" "return" Integer "}"
```

你可以使用 antlr 等解析器生成器来识别上述标识和文法，也可以自己实现词法分析器和语法解析器。如果你决定自己实现，可以先利用正则表达式编写出一个能运行的程序，再重构为真正的 LL 或 LR 分析器。

> 注意：我们不能对负整数进行词法分析。这并不是偶然的——C 语言没有负整数常量。它只是有一个负一元运算符，可以应用于正整数。我们将在下一步添加负一元运算。

解析了上述文法后，你的程序就知道了 `return` 关键字之后的整数到底是多少，这样就可以生成目标代码了。最简单的 RISC-V 目标代码如下：

```asm
.global main
main:
	mv a0, X  # 此处 X 为识别出的整数
	ret
```

这一段汇编代码首先声明 `main` 是全局可见的符号，此为程序的入口。在 `main` 符号后，程序向保存返回值的寄存器 `a0` 中存入要返回的整数，最后返回。

为了验证你的编译器是否正常工作，你可以用下列命令运行它，并检查它的返回代码。

```
$ YOUR_COMPILER return_2.c  # 用例的编译器会把 return_2.c 编译为 return_2.S 汇编程序
$ riscv64-unknown-elf-gcc return_2.S -o return_2  # riscv-64 汇编器把 return.S 翻译为return_2 执行程序
$ qemu-riscv64 ./return_2  # 用QEMU for riscv-64 硬件模拟器运行 return_2 可执行程序
$ echo $?  # 检查 return_2 执行程序的执行结果，应该是 2
2 
```

## 重构：抽象语法树

我们已经完成了一个能编译 `return_2.c` 的最简单编译器。这种实现方式虽然很简洁，但很难扩展到更复杂的语法。下一步，我们要引入抽象语法树（Abstract  Syntax Tree，AST）来表示程序。`return_2.c` 的 AST 可以如下图，你也可以根据自己的喜好调整各结点的定义。

![Image of diagram; text outline follows](./pics/return_2_ast.svg)

请用自己熟悉的语言实现这一 AST 的构建及遍历。接下来，我们将通过遍历 AST 的方式完成语法生成，在各结点输出改结点对应的汇编代码，而不是直接输出整个汇编程序。这一过程的伪代码如下：

```c++
void visit(Program *node) {
    printf(".global main\n");
    for (Function *func : node->functions) {
    	visit(func)
    }
}

void visit(Function *node) {
    printf("main:\n");
   	for (Statement *stmt : node->statements) {
        visit(stmt)
    }
}

void visit(ReturnStmt *node) {
    visit(node->expr);
    printf("ret\n")
}

void visit(Integer *node) {
    printf("mv a0, %d", node->val);
}
```

>  注意：上述伪代码仅供示意。实际实现中，你可能会遇到更具体的问题，例如如何判断一个表示 AST 结点的对象到底是什么类型的。不同语言中，可能有各自不同的最优实现。在 Java 和 C++ 等语言中，你可以使用类多态的方式实现各结点，并添加专门的成员函数返回特定对象的类型；而在支持模式匹配的语言中，直接利用模式匹配会使实现更加简单。

运行重构后的编译器，我们将生成与前述最简单编译器完全相同的目标代码。至此，我们完成了单整数程序的编译，并引入了一个中间表达：抽象语法树。

## 下一步

在[下一步]()中，我们将增加三个单数运算符。`-`、`~`和`！`。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
