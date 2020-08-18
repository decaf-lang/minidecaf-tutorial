
# 编写minidecaf编译器-step1

这是关于编写minidecaf编译器的第一个步骤。

编写minidecaf编译器是参考了使用Abdulaziz Ghuloum的[An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)和Nora Sandler的[Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)作为路线图。这里的minidecaf语言基本上是C语言的一个子集。你通过从编译minidecaf源语言的一个微不足道的子集开始，能够生成[RISC-V汇编代码](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-intro.md)，并能在RISC-V机器（目前是基于QEMU模拟器）上运行/测试你写的编译器生成的最终机器代码。然后你再一步一步地添加新的语言特性。在第一步中，你只是返回常量；在后面的步骤中，你处理加法和减法；以此类推。每一步都小到足以让人感觉到易于管理，而在每一步结束时，你都有一个可以工作的编译器。另外，通过足够详尽的[测试程序](https://github.com/decaf-lang/minidecaf-tests)，你可以随时验证你的编译器在每次更新后是否正常工作。

# 前言

在你开始之前，你需要决定两件事：用什么语言来写你的编译器，以及如何处理词法分析（lexing）和语法解析（parsing ） 。你可以用任何你喜欢的语言来实现编译器

> 提示：建议使用具有和[sum type](https://chadaustin.me/2015/07/sum-types/)和模式匹配（ pattern matching）的语言，比如OCaml、Haskell或Rust。如果你这样做的话，构建和遍历一个AST会变得更加简单。前提是你能接受学习和掌握这些编程语言的所投入的时间与精力。

你还需要决定是自己写语法解析器和词法分析器，还是使用自动解析器和扫描器生成器（例如[flex](https://github.com/westes/flex)，[bison](https://www.gnu.org/software/bison/)，[antlr4](https://www.antlr.org)）。在整个实验环节中，两种方式都会提供。我们将展示如何手工编写一个词法器（或扫描器）和递归下降解析器。使用解析器生成器可能更容易，缺点是了解底层运行细节和调试bug可能会困难一些。如果能够直接设计实现解析器生成器，那么对编译课上讲的很多原理、算法的理解会更加深入。

> 注意：设计实现解析器生成器不是基本实验要求。

# 准备

本教程使用自动词法分析和语法分析工具[antlr4](https://www.antlr.org)构建minidecaf编译器，因此这里将弱化词法分析和语法分析部分的代码实现，如想学习如何手工编写词法分析和语法分析器，请参考[chyyuu](https://github.com/decaf-lang/minidecaf-tutorial/tree/md-cy/docs)老师编写的详细文档。本教程将直接在`antlr4`自动生成的语法树上进行遍历、解释执行以及最终的代码生成，因此需要事先掌握`antlr4`的基本使用方法，相关的教程有很多（[antlr4 tutorial](https://github.com/antlr/antlr4/blob/4.8/doc/index.md)），大家也可以自行查找学习。

另外为了在遍历语法树的过程中不对其造成改变，并且针对多样的应用具有扩展性，我们将使用访问者模式对语法树进行遍历访问，你需要在开始开发之前学习[访问者模式](<https://www.runoob.com/design-pattern/visitor-pattern.html>)相关的知识，也可以查看[助教](<https://github.com/decaf-lang/minidecaf-tutorial/blob/md-dzy/step1/Visitor%20%E6%A8%A1%E5%BC%8F%E6%A6%82%E8%BF%B0.md>)提供的相关文档。

# 第一步 : 整数

## 解析源程序及建立语法分析树

本阶段我们将编译一个返回单个整数的minidecaf程序。万事开头难，在这一步你将定义语言特性对应的上下文无关文法，并使用`antlr4`将其解析为语法树，最终使用其提供的访问者接口遍历语法树生成`RISC-V`汇编代码。

> 注：虽然使用 antlr4 工具可以将我们从词法分析和语法分析以及构建语法树的工作中释放出来，但我们必须清楚每个步骤工具做了什么、我们需要给工具提供什么样的信息。

下面是一个我们要编译的程序 return_2.c

```c
int main() {
    return 2;
}
```

我们将只处理有一个函数 "main "的程序，它由一个返回语句组成。唯一不同的是返回的整数的值，我们不会处理十六进制或八进制的整数，只处理十进制。为了验证你的编译器是否正常工作，你需要编译一个程序，运行它，并检查它的返回代码。

综合考虑目标语法特性的**可编译运行性**（有主函数和返回语句支持）和**实现简易性**，在这一步我们将`int`, `main`, `(`, `)`, `{`, `}`, `;`, `return`, 均定义为标记（token），并且添加`INTEGER`标记指挥词法分析器将源文件中可能出现的整数识别为一个 token，因此我们实现的文法规则类似如下：

``` 
grammar minidecaf;
# 定义文法规则
program : 'int' 'main' '(' ')' '{' 'return' INTEGER ';' '}';
# 定义token以便你在后续的操作中可以访问到它们
INT : 'int';
INTEGER : [0-9]+;
......
# 剩余部分自行实现，你一定可以
```

在定义完成文法规则后，`antlr4`接受其作为输入，进行词法、语法分析，最终会生成类似于下图所示的语法树。

> 注：由于简易的实现方案，上述文法会产生一颗以program作为根节点，其余标记作为叶子结点的语法分析树，语法树的结构和你定义的文法规则息息相关。下图只是一个语法树的例子，并不和上述文法直接关联。

![Image of diagram; text outline follows](./pics/return_2_ast.svg)

## 代码生成

现在我们已经得到了一个语法分析树，`antlr4`也为我们提供了便利的语法树节点访问接口，我们已经准备好生成汇编代码了！就像我们之前看到的，我们只需生成几行汇编码。为此，我们将大致按照程序执行的顺序遍历语法分析树，对我们关心的节点做处理。本例中，我们关心的节点为`program`和`INTEGER`，其中`program`为语法树的根节点，`interger`为需要返回的常数节点。

> 注：虽然你需要聚焦于某些特殊节点，但是你需要保证对语法树的访问过程要能顺利进行，因此对不需特殊关心的节点，我们需要指定遍历其子节点的操作。

下面是我们要生成汇编码：

1. 生成主函数入口

```
	.globl main
main:
    <FUNCTION BODY GOES HERE>
```

2. 生成一个返回语句（如：`return 2;`）的汇编码

```
    li a0, 2
    ret
```

> 由于这可能是你第一次接触 RISC-V 汇编，我们对上述程序做简单解释。`li`指令代表的操作为向指定寄存器加载相应立即数，`a0` 为 RISC-V 中常用于保存函数返回值的寄存器，这条指令将立即数`2`加载到了`a0`寄存器中用于函数返回。

## 附：Visitor访问方法

本例中我们在遍历语法分析树的同时生成汇编代码，下面给出此过程的示例代码：

```C++
void visitProgram (ProgramContext *ctx) { 
    # 由于本例中语法树较为简单，只需访问根节点即可
    code_ << "\t.globl main\n"
    	  << "main:\n";
   	# 获取 INTEGER 节点的文本信息，并将其附加到指令中
    code_ << "\tli a0, " << ctx->INTEGER()->getText() << "\n";
    # 最终返回
    code_ << "\tret";
}
```

> 注：上述程序中使用了Antlr4中的某些接口，在表意同时也保证了运行正确性。另外输出中的`\t`制表符是为了让输出的汇编码缩进规范。

## 测试

整个从源代码到`RISC-V`机器码的编译测试流程大致如下：

```shell
$ YOUR_COMPILER return_2.c # 用例的编译器会把return_2.c编译为 return.s 汇编程序
$ riscv64-unknown-elf-gcc return_2.s -o return_2 # riscv-64汇编器把return.s翻译为return_2执行程序
$ qemu-riscv64 ./return_2 # 用QEMU for riscv-64硬件模拟器运行return_2执行程序
$ echo $? # 检查return_2执行程序的执行结果，应该是 2
2 
```

你可以修改[minidecaf测试](https://github.com/decaf-lang/minidecaf-tests)中的自动批量测试脚本，来测试你的编译器是否正常通过所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)。它将使用你的编译器编译一组测试程序，执行它们，并确保它们返回正确的值。


为了用脚本自动批量测试一组程序，你写的编译器需要遵循这个规范。

1. 它可以从命令行中调用，只需要一个C源文件作为参数，例如：1: `./YOUR_COMPILER /path/to/program.c`。
2. 当传入`program.c`时，它会在同一目录下生成`program.s`汇编代码文件。
3. 如果解析失败，它不会生成汇编代码文件。

脚本不会检查你的编译器是否输出合理的错误信息。

## 下一步

在[下一步]()中，我们将增加三个单数运算符。`-`、`~`和`！`。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
