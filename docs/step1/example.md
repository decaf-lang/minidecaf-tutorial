# 通过例子学习，一个仅有 return 的主函数编译全流程：

本步骤主要涉及的语法为主函数和 return 语句，完成本步骤之后，你的编译器将支持将一个仅有 return 的主函数编译为 32 位 RISC-V 汇编代码，并通过 RISC-V 工具链生成可以在硬件模拟器上正确运行的程序。因为这是大家首次接触 MiniDecaf 编译实验框架，我们给大家的代码框架中已经包含所有 step1 的实现，大家可以直接运行通过 step1 的测试用例。并且，我们在每个步骤的文档中会详细梳理介绍在当前步骤中需要用到的知识点以及对应的代码片段和注释，如果我们认为当前步骤并不需要了解某部分知识点（如数据流分析、寄存器分配），我们会在后续的步骤中进行知识点的讲解。

下面我们将通过一个简单的 step1 测试用例，一起走过它的编译全流程：

```C
int main() {
    return 2022;
}
```

> 请注意，这里给出的生成结果（抽象语法树、三地址码、汇编）只是一种参考的实现，同学们可以按照自己的方式实现，只要能够通过测试用例即可。但是，严格杜绝抄袭现象，如果代码查重过程中发现有抄袭现象，抄袭者与被抄袭者将被记为0分。

## 词法分析 & 语法分析

在词法分析 & 语法分析这一步中，我们需要将输入的程序字符流按照[语法规范](./spec.md)转化为后续步骤所需要的 AST，我们使用了 lex/yacc 库来实现这一点。[yacc](https://en.wikipedia.org/wiki/Yacc) 是一个根据 EBNF 形式的语法规范生成相应 LALR parser 的工具，支持基于属性文法的语法制导的语义计算过程。**你可以根据我们的框架中对 lex/yacc 的使用，结合我们的文档，来快速上手 lex/yacc，完成作业；也可以选择阅读一些较为详细的文档，来系统地进行 lex/yacc 的入门，但这不是必须的。**

为了方便同学们理解框架，我们将同时在这一段中说明为了加入取负运算所需要的操作。在实验框架中，我们使用的是 lex/yacc 的一个纯 python 实现，称为 python-lex-yacc（简称 ply），其使用方法与 lex/yacc 有一些差异。

[Python-lex-yacc 快速入门](https://www.dabeaz.com/ply/ply.html)

程序的入口点在 `main.py`，它通过调用 `frontend.parser.parser`（位于 `frontend/parser/ply_parser.py`）来完成语法分析的工作，而这一语法分析器会自动调用位于 `frontend/lexer/ply_lexer.py` 的词法分析器进行词法分析。语法的定义和语法分析器都位于 `frontend/parser/ply_parser.py`，而词法的定义位于 `frontend/lexer/lex.py`。AST 节点的定义位于 `frontend/ast/tree.py` 中。以下表示中的符号都出自于这几个文件。

这部分的工作流程如下，第一行是对应的函数：

```
                  读内容       词法分析 & 语法分析              语义分析
                 readCode       parser.parse    namer.transform & typer.transform
MiniDecaf 源文件 --------> 字节流 -----------> AST -------------------------------> ... 
```

当程序读入程序的字符流之后，它首先会被 lexer 处理，并被转化为如下形式的一个 Token 流：

`Int Identifier("main") LParen RParen LBrace Return Integer(2022) Comma RBrace`

并被 yacc 生成的 LALR(1) parser 转化为如下形式的 AST：

```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) Return
                |- (expr) IntLiteral(2022)
```

得到的这个 AST 也就是 `main.py` 中 `step_parse` 这一函数里 `parser.parse(...)` 的输出。

尝试运行 `python main.py --input example.c --parse` 你应该就能看到类似的输出。（记得自己写一个`example.c`）

## 语义分析

在 step1 语义分析步骤中，我们要遍历 AST，检验是否存在如下的语义错误：

* main 函数是否存在。

* return 语句是否有返回值。

* 返回值是否在 int 合法的范围内。

在实际操作中，我们遍历 AST 所用的方法就是的 [Visitor 模式](./visitor.md)，通过 Visitor 模式，我们可以从抽象语法树的根结点开始，遍历整颗树的所有语法结点，并针对特定的语法结点作出相应的操作，如名称检查和类型检查等。在编译器中，这种基于 Visitor 的对语法树进行一次遍历，完成某种检查或优化的过程，称为遍（pass）。不难想到，一个现代编译器是由很多遍扫描组成的，如 gcc 根据优化等级不同会有数百个不等的 pass。下面，我们将指出，step1 中我们是如何实现符号表构建 pass 和类型检查 pass 的，选择不同语言的同学，可以选择去看相应的代码注释与实现细节。

`frontend/typecheck/namer.py` 和 `typer.py` 分别对应了符号表构建和类型检查这两次遍历。在框架中，`Namer` 和 `Typer` 都是继承 `frontend/ast/visitor.py` 中的 `Visitor` 类来通过 Visitor 模式遍历 AST 的。其实现细节参见代码。

## 中间代码生成

在通过语义检查之后，编译器已经掌握了翻译源程序所需的信息（符号表、类型等），下一步要做的则是将抽象语法树翻译为便于移植和优化的中间代码，在本实验框架中就是三地址码。如何翻译抽象语法树？当然还是无所不能的 Visitor 模式，我们在中间代码生成步骤中再遍历一次语法树，对每个结点做对应的翻译处理。具体来说，在 step1 当中，我们只需要提取 return 语句返回的常量，为之分配一个临时变量，再生成相应的 TAC 返回指令即可。不难看出，本例对应的三地址码为：

```asm
main:           # main 函数入口标签
    _T0 = 2022  # 为立即数2022分配一个临时变量
    return _T0  # 返回
```

> 下面，我们同样也指出了在代码中我们是怎样实现这个中间代码生成 pass 的，大家可以参考注释和代码了解实现细节。

`frontend/tacgen/tacgen.py` 中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。

`frontend/utils/tac` 目录下实现了生成 TAC 所需的底层类。其中 `tacinstr.py` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。提供给生成 TAC 程序流程的主要接口在 `funcvisitor.py` 中，若你增加了 TAC 指令，则需要在 `FuncVisitor` 类中增加生成该指令的接口。在本框架中，TAC 程序的生成是以函数为单位，对每个函数（step1-8 中只有 main 函数）分别使用一个 `FuncVisitor` 来生成对应的 TAC 程序。除此之外的 TAC 底层类，同学们可以不作修改，也可以按照自己的想法进行修改。

## 目标代码生成

目标代码生成步骤是对中间代码的再一次翻译，在本例中，你需要了解并掌握的知识点有:

1. 如何将一个立即数装载到指定寄存器中？

   RISC-V 提供了 li <reg> <imm32> 指令来支持加载一个 32 位立即数到指定寄存器中，其中 <reg> 表示寄存器名，<imm32> 表示立即数值，如：`li t0, 2022`，就是将立即数 2022 加载到寄存器 t0 中。

2. 如何设置返回值？

   在 RISC-V 中，a0 和 a1 是 gcc 调用约定上的存储返回值的寄存器，返回值会按照其大小和顺序存储在 a0 和 a1 中。也就是说，如果你有一个 32 位的返回值，你可以放在 a0 中返回，如果你有两个 32 位的返回值，你就需要把它们分别放在 a0 和 a1 中返回。更多的返回值会全部放入内存返回，如约定好的栈的某个位置，这取决于函数调用约定。 

   在我们的实验要求中，返回值均是单个 32 位的值。因此在当前步骤中你只需要了解，将需要返回的值放入 a0 寄存器中，然后在后面加上一条 ret 指令即可完成函数返回的工作。

综上所述，我们上述中间代码翻译成如下 RISC-V 汇编代码：

```asm
    .text         # 代码段
    .global main  # 声明全局符号 main
main:             # 主函数入口符号
    li t0, 2022   # 加载立即数2022到t0寄存器中
    mv a0, t0     # 将返回值放到a0寄存器中
    ret           # 返回
```

>  关于实现细节，对应的代码位置在下面给出，代码中提供注释供大家学习：

实验框架中关于目标代码生成的文件主要集中 `backend` 文件夹下，step1 中你只需要关注 `backend/riscv` 文件夹中的 `riscvasmemitter.py` 以及 `utils/riscv.py` 即可。具体来说 `backend/asm.py` 中会先调用 `riscvasmemitter.py` 中的 `selectInstr` 方法对每个函数内的 TAC 指令选择相应的 RISC-V 指令，然后会进行数据流分析、寄存器分配等流程，在寄存器分配结束后生成相应的 `NativeInstr` 指令（即所有操作数都已经分配好寄存器的指令），最后通过 `RiscvSubroutineEmitter` 的 `emitEnd` 方法生成每个函数的 RISC-V 汇编。

## 细节呢？

为了帮大家再快一点了解实验框架。我们进一步看一个例子，如果我们想把返回值从 `2022` 变成 `-2022`，则在这一步中你可能需要进行以下操作（实际上这些实现已经在框架里提供）：

首先，我们应该把 `-` 看作一个符号，而不应该将 `-2022` 看作一个整体，因为我们还可能遇到 `-x` 这种求一个变量的相反数的操作，如果将其分开处理则会增加我们的工作量。因此我们需要在词法分析中加入对 `-` 的处理。

我们能发现 `-`, `!`, `~` 等符号都可以作为一元运算符出现，比如`!x`, `~a`, `-10`，我们将这类一元运算操作都称为 unary ，一并处理所有的一元运算符这样就不需要对每一种符号都专门生成一种语法规则和 AST 节点了。

因此我们希望生成的 AST 应当变为如下形式：

```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) Return
                |- (unary) -
                    |- (expr) IntLiteral(2022)
```

* 词法分析 & 语法分析
    
    在 `frontend/lex/lex.py` 里加入新的 lex token 定义，以便lexer可以解析 `-`：

    ```python
    t_Minus = "-"
    ```

    在 ply 的 lexer 中，定义的新 token 需要以 `t_`开头。更具体的解释见文件注释或[文档](https://www.dabeaz.com/ply/ply.html)。
    
    在 `frontend/ast/tree.py` 里加入新的 AST 节点定义（以及相应的其它东西），可能长这样：

    ```python
    class Unary(Expression):
        def __init__(self, op: Operator, operand: Expression):
            ...
    ```

    并在 `frontend/ast/visitor.py` 中加入相应的分派函数。

    它将在后续的 parser 语义计算中被用到。

    在 `frontend/parser/ply_parser.py` 里加入新的 grammar rule，可能包含（不限于）以下的这些：

    ```python
    def p_expression_precedence(p): # 定义的新语法规则名。可以随便起，但必须以 `p_` 开头以被 ply 识别。
        """
        expression : unary
        unary : primary
        """ # 以 [BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) 定义的新语法规则，以 docstring 的形式提供。
        p[0] = p[1] # 这条语法规则相应的语义计算步骤，下标对应着产生式中的相应符号。
        # 语法分析器直接产生的实际上是一棵语法分析树，而构建 AST 这一数据结构则通过相应语法制导的语义计算过程来完成。

    def p_unary_expression(p):
        """
        unary : Minus unary
        """
        p[0] = tree.Unary(UnaryOp.Neg, p[2])
    ```

    现在尝试运行 `python main.py --input example.c --parse` 看看效果吧。（记得修改`example.c`）

这样就基本完成了词法 & 语法分析步骤里加入取负运算的所有步骤。后续步骤中可能需要在某些 visitor 中实现相应的检查、转化至 TAC 的逻辑。