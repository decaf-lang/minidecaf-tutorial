# 通过例子学习，一个仅有 return 的主函数编译全流程：

本步骤主要涉及的语法为主函数和 return 语句，完成本步骤之后，你的编译器将支持将一个仅有 return 的主函数编译为 32 位 RISC-V 汇编代码，并通过 RISC-V 工具链生成可以在硬件模拟器上正确运行的程序。因为这是大家首次接触 MiniDecaf 编译实验框架，我们给大家的代码框架中已经包含所有 step1 的实现，大家可以直接运行通过 step1 的测试用例。并且，我们在每个步骤的文档中会详细梳理介绍在当前步骤中需要用到的知识点以及对应的代码片段和注释，如果我们认为当前步骤并不需要了解某部分知识点（如数据流分析、寄存器分配），我们会在后续的步骤中进行知识点的讲解。

下面我们将通过一个简单的 step1 测试用例，一起走过它的编译全流程：

```C
int main() {
    return 2023;
}
```

## 词法分析 & 语法分析

在词法分析 & 语法分析这一步中，我们需要将输入的程序字符流按照[语法规范](./spec.md)转化为后续步骤所需要的 AST，我们使用了 lex/yacc 库来实现这一点。[yacc](https://en.wikipedia.org/wiki/Yacc) 是一个根据 EBNF 形式的语法规范生成相应 LALR parser 的工具，支持基于属性文法的语法制导的语义计算过程。**你可以根据我们的框架中对 lex/yacc 的使用，结合我们的文档，来快速上手 lex/yacc，完成作业；也可以选择阅读一些较为详细的文档，来系统地进行 lex/yacc 的入门，但这不是必须的。**

在实验框架中，我们使用的是 lex/yacc 的一个纯 python 实现，称为 python-lex-yacc（简称 ply），其使用方法与 lex/yacc 有一些差异。

[Python-lex-yacc 快速入门](https://www.dabeaz.com/ply/ply.html)

程序的入口点在 `main.py`，它通过调用 `frontend.parser.parser`（位于 `frontend/parser/ply_parser.py`）来完成语法分析的工作，而这一语法分析器会自动调用位于 `frontend/lexer/ply_lexer.py` 的词法分析器进行词法分析。语法的定义和语法分析器都位于 `frontend/parser/ply_parser.py`，而词法的定义位于 `frontend/lexer/lex.py`。AST 节点的定义位于 `frontend/ast/tree.py` 中。以下表示中的符号都出自于这几个文件。

这部分的工作流程如下：

```
                  读内容       词法分析 & 语法分析              语义分析
                 readCode       parser.parse    Namer.transform & Typer.transform
MiniDecaf 源文件 --------> 字节流 -----------> AST -------------------------------> ... 
```

当程序读入程序的字符流之后，它首先会被 lexer 处理，并被转化为如下形式的一个 Token 流：

`Int Identifier("main") LParen RParen LBrace Return Integer(2023) Semi RBrace`

在`frontend/lexer/lex.py`文件中你可以看到每个 Token 是如何定义的，每个`token`都会以`t_`开头。如`t_Semi = ";"`代表分号被解析以后会转化为 `Semi` 这个Token。而对于一些复杂的 Token，我们需要在`lexer`中定义一个正则表达式来匹配它，lex中通过定义一个函数来实现正则匹配。以匹配整数为例，函数的第一行`r"[0-9]+" `代表匹配用到的正则表达式，而函数的参数`t`则是被匹配得到的字符串，我们通过python中的类型转换将其变为一个整数，你可以在文件中看到以下代码：
    
```python
def t_Integer(t):
    r"[0-9]+"  # can be accessed from `t_Interger.__doc__`
    t.value = int(t.value)
    return t
```

之后，这些 token 会被 yacc 生成的 LALR(1) parser 转化为如下形式的 AST：

```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) Return
                |- (expr) IntLiteral(2023)
```

得到的 AST 也就是 `main.py` 中 `step_parse` 这一函数里 `parser.parse(...)` 的输出。

在`frontend/parser/ply_parser.py`文件中，你可以看到我们是如何定义语法规则的，文件的最末尾有`parser = yacc.yacc(start="program")`代表了parser的入口点是`program`，而`program`的定义在`p_program`函数中，你可以看到这个函数的docstring中定义了`program`的语法规则。**注意docstring在这里并非注释，而是用来定义语法规则的**。

```
def p_program(p):
    """
    program : function
    """
    p[0] = Program(p[1])

def p_function_def(p):
    """
    function : type Identifier LParen RParen LBrace block RBrace
    """
    p[0] = Function(p[1], p[2], p[6])
```

我们先看`p_program`函数，我们定义的语法规则是`program`由一个`function`组成，对应的上下文无关表达式就是`program -> function`，同时代码中的`p[0] = Program(p[1])`代表了构建AST的计算过程，这里的`p[0]`代表的是当前语法规则的左部，`p[1]`代表的是当前语法规则的右部第一个符号（即`function`），`p[2]`代表的是当前语法规则的右部第二个符号（这里没有），以此类推。这样递归下去，就能解析完整个程序。`p[0] = Program(p[1])`最后就会变为`p[0] = Program(Function(...))`，这里`Program`、`Function`类的定义在`frontend/ast/tree.py`文件中，你可以看到`Function`这个类的构造函数接受了三个参数，分别是返回值类型、函数名和函数体。

尝试运行 `python main.py --input example.c --parse` 你应该就能看到类似的输出。（记得自己写一个`example.c`）

## 语义分析

在 step1 语义分析步骤中，我们要遍历 AST，检验是否存在如下的语义错误：

* main 函数是否存在。（`frontend/typecheck/namer.py:37`）

在实际操作中，我们遍历 AST 所用的方法就是的 [Visitor 模式](./visitor.md)，通过 Visitor 模式，我们可以从抽象语法树的根结点开始，遍历整颗树的所有语法结点，并针对特定的语法结点作出相应的操作，如名称检查和类型检查等。在编译器中，这种基于 Visitor 的对语法树进行一次遍历，完成某种检查或优化的过程，称为遍（pass）。不难想到，一个现代编译器是由很多遍扫描组成的，如 gcc 根据优化等级不同会有数百个不等的 pass。下面，我们将指出，step1 中我们是如何实现符号表构建 pass 和类型检查 pass 的，同学们可以选择去看相应的代码注释与实现细节。

`frontend/typecheck/namer.py` 和 `typer.py` 分别对应了符号表构建和类型检查这两次遍历。在框架中，`Namer` 和 `Typer` 都是继承 `frontend/ast/visitor.py` 中的 `Visitor` 类来通过 Visitor 模式遍历 AST 。

## 中间代码生成

在通过语义检查之后，编译器已经掌握了翻译源程序所需的信息（符号表、类型等），下一步要做的则是将抽象语法树翻译为便于移植和优化的中间代码，在本实验框架中就是三地址码。如何翻译抽象语法树？当然还是无所不能的 Visitor 模式，我们在中间代码生成步骤中再遍历一次语法树，对每个结点做对应的翻译处理。具体来说，在 step1 当中，我们只需要提取 return 语句返回的常量，为之分配一个临时变量，再生成相应的 TAC 返回指令即可。不难看出，本例对应的三地址码为：

```asm
main:           # main 函数入口标签
    _T0 = 2023  # 为立即数2023分配一个临时变量
    return _T0  # 返回
```

> 下面，我们同样也指出了在代码中我们是怎样实现这个中间代码生成 pass 的，大家可以参考注释和代码了解实现细节。

`frontend/utils/tac` 目录下实现了生成 TAC 所需的底层类。其中 `tacinstr.py` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。

`frontend/tacgen/tacgen.py` 中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。这个文件里除了类型`TACGen`之外还有一个辅助类`TACFuncEmitter`，它用于处理产生TAC代码过程中一些相对底层的细节。在本框架中，TAC 程序的生成以函数为单位，对每个函数（step1-8 中只有 main 函数）分别使用一个 `TACFuncEmitter` 来生成对应的 TAC 函数代码。如果你增加了 TAC 指令，则可能需要在 `TACFuncEmitter` 类中增加生成相应指令的代码。

## 目标代码生成

目标代码生成步骤是对中间代码的再一次翻译，在本例中，你需要了解并掌握的知识点有:

1. 如何将一个立即数装载到指定寄存器中？

   RISC-V 提供了 li <reg> <imm32> 指令来支持加载一个 32 位立即数到指定寄存器中，其中 <reg> 表示寄存器名，<imm32> 表示立即数值，如：`li t0, 2023`，就是将立即数 2023 加载到寄存器 t0 中。

2. 如何设置返回值？

   在 RISC-V 中，a0 和 a1 是 gcc 调用约定上的存储返回值的寄存器，返回值会按照其大小和顺序存储在 a0 和 a1 中。也就是说，如果你有一个 32 位的返回值，你可以放在 a0 中返回，如果你有两个 32 位的返回值，你就需要把它们分别放在 a0 和 a1 中返回。更多的返回值会全部放入内存返回，如约定好的栈的某个位置，这取决于函数调用约定。 

   在我们的实验要求中，返回值均是单个 32 位的值。因此在当前步骤中你只需要了解，将需要返回的值放入 a0 寄存器中，然后在后面加上一条 ret 指令即可完成函数返回的工作。

综上所述，我们上述中间代码翻译成如下 RISC-V 汇编代码：

```asm
    .text         # 代码段
    .global main  # 声明全局符号 main
main:             # 主函数入口符号
    li t0, 2023   # 加载立即数2023到t0寄存器中
    mv a0, t0     # 将返回值放到a0寄存器中
    ret           # 返回
```

实验框架中关于目标代码生成的文件主要集中 `backend` 文件夹下，step1 中你只需要关注 `backend/riscv` 文件夹中的 `riscvasmemitter.py` 以及 `utils/riscv.py` 即可。具体来说 `backend/asm.py` 中会先调用 `riscvasmemitter.py` 中的 `selectInstr` 方法对每个函数内的 TAC 指令选择相应的 RISC-V 指令，然后会进行数据流分析、寄存器分配等流程，在寄存器分配结束后生成相应的 `NativeInstr` 指令（即所有操作数都已经分配好寄存器的指令），最后通过 `RiscvSubroutineEmitter` 的 `emitEnd` 方法生成每个函数的 RISC-V 汇编。

## 细节呢？

>  关于实现细节，对应的代码位置在下面给出，代码中提供注释供大家学习，但是应该有同学不想读冗长的代码，因此有了这部分。

为了帮大家再快一点了解实验框架。我们进一步看一个例子，如果我们想把返回值从 `2023` 变成 `-2023`，则在这一步中你可能需要进行以下操作（实际上这些实现已经在框架里提供）：

首先，我们应该把 `-` 看作一个符号，而不应该将 `-2023` 看作一个整体，因为我们还可能遇到 `-x` 这种求一个变量的相反数的操作，如果将其分开处理则会增加我们的工作量。因此我们需要在词法分析中加入对 `-` 的处理。

我们能发现 `-`, `!`, `~` 等符号都可以作为一元运算符出现，比如`!x`, `~a`, `-10`，我们将这类一元运算操作都称为 unary ，一并处理所有的一元运算符这样就不需要对每一种符号都专门生成一种语法规则和 AST 节点了。

因此我们希望生成的 AST 应当变为如下形式：

```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) Return
                |- (expr) Unary
                    |- (op) Minus
                    |- (expr) IntLiteral(2023)
```

看到这里，你可能会好奇，为什么这里多了如 (expr) Unary 这样的奇怪的 AST 节点。在编译器中，我们将所有的值、或者运算产生的结果称为一个表达式。比如 `2023` 这个数字是一个表达式， `-2023` , `y-x`同样也是表达式，其会生成一个值。而带返回值的 `return` 语句需要一个值，我们可以理解为带返回值的 `return` 语句后需要接一个表达式，这样在语义上才是正确的（例如，我们能见到`return 1;`这样的语句，但是不会见到`return if;`这样的语句，因为 `if` 并不是一个会产生值的表达式）。

* 词法分析 & 语法分析
    
    在 `frontend/lex/lex.py` 里加入新的 lex token 定义，以便lexer可以解析 `-`：

    ```python
    t_Minus = "-"
    ```

    在 ply 的 lexer 中，定义的新 token 需要以 `t_`开头。更具体的解释见文件注释或[文档](https://www.dabeaz.com/ply/ply.html)（太长了助教也读不下去）。
    
    在 `frontend/ast/tree.py` 里加入新的 AST 节点定义（以及相应的其它东西）：

    ```python
    class Unary(Expression):
        def __init__(self, op: Operator, operand: Expression):
            ...
    ```

    并在 `frontend/ast/visitor.py` 中加入相应的分派函数。

    它将在后续的 parser 语义计算中被用到。

    在 `frontend/parser/ply_parser.py` 里加入新的 grammar rule：

    ```
    def p_expression_precedence(p): # 定义的新语法规则名。可以随便起，但必须以 `p_` 开头以被 ply 识别。
        """
        expression : unary
        unary : primary
        """ 
        # 以 [BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) 定义的新语法规则，以 docstring 的形式提供。
        p[0] = p[1] # 这条语法规则相应的语义计算步骤，下标对应着产生式中的相应符号。
        # 语法分析器直接产生的实际上是一棵语法分析树，而构建 AST 这一数据结构则通过相应语法制导的语义计算过程来完成。

    def p_unary_expression(p):
        """
        unary : Minus unary
        """
        p[0] = tree.Unary(UnaryOp.Neg, p[2])
    ```

    这里其实就是上下文无关文法，大家要看懂文法和代码的对应关系，注意看这条生成规则`unary : Minus unary`，其中p[0]代表的就是第一个`unary`, p[1]则是`Minus`，p[2]为第二个`unary`。你会看到我们框架代码和这里不太一样，因为unary符号不止有减号，我们通过将lex解析得到的`-`通过`backward_search`对应到我们在代码中enum的`UnaryOp.Neg`（frontend/ast/node.py:40）。

    现在尝试运行 `python main.py --input example.c --parse` 看看效果吧。（记得修改`example.c`）

* 怎么从 AST 变为 TAC 的？

    什么是 [TAC](./arch.md#三地址码) ，如果你没读前面的章节，你可以快速看看这一部分。

    这一步就是 `TACGen.transform` 函数(frontend/tacgen/tacgen.py)做的事了， `TACGen.transform` 接受一个AST树输入，输出一个TAC表示，请确保你已经对[Visitor 模式](./visitor.md)有所了解，或者假设你已经知道在遍历 AST 时 accept 函数会对不同类型的 AST Node 调用不同的visit 函数。例如，visit `(children[0]) Return` 时，遇到的子节点是 `(expr) Unary`，那么 `accept` 最终会调用`visitUnary`，你的lint工具应该是没法做到点一下就跳转到对应的位置，所以你需要自己判断我们在遍历某个节点的时候其子节点的类型。

    **下面的描述中一定要记得区分accept和直接对于mv.visitXXX的调用，前者是在遍历AST时调用的，后者是在 TACFuncEmitter 类中调用的。并且希望大家一定要对着代码看。**
    
    ```
    Program
        |- (children[0]) Function
            |- (ret_t) TInt
            |- (ident) Identifier("main")
            |- (body) Block
                |- (children[0]) Return
                    |- (expr) Unary
                        |- (op) Minus
                        |- (expr) IntLiteral(2023)
    ```

    继续看上述例子，我们先关注只有 `main` 函数的 Minidecaf 程序，我们将`TACGen.transform`代码贴了一些在这里：
    
    ```python
    def transform(self, program: Program) -> TACProg:
        labelManager = LabelManager()
        tacFuncs = []
        for funcName, astFunc in program.functions().items():
            # in step9, you need to use real parameter count
            emitter = TACFuncEmitter(FuncLabel(funcName), 0, labelManager)
            astFunc.body.accept(self, emitter)
            tacFuncs.append(emitter.visitEnd())
        return TACProg(tacFuncs)
    ```

    现在我们开始正式遍历 AST 树，`transform` 会先遍历每一个函数进行代码翻译，因为我们目前只有一个函数`main`，我们只考虑没有参数的函数，我们需要对函数体进行翻译，函数体首先在一个block中（花括号括起来的部分），因此会先进入 `visitBlock` 函数，`visitBlock` 函数对于在block中的所有子节点调用了`child.accept(self, mv)`，在这个例子中则会调用`Return` 语句对应的visitor，进入`visitReturn`。继续向下，`visitReturn` 又对于 return AST Node 中的 expr 调用了 `stmt.expr.accept(self, mv)` ，又进入了`visitUnary`，同理，`expr.operand.accept(self, mv)`会进入`visitIntLiteral`。
    
    到了此处出现了不同，我们发现`visitIntLiteral`中第一次调用了mv的成员函数 `mv.visitLoad(expr.value)` 这里进入了`TACFuncEmitter.visitLoad`：

    ```python
    def visitLoad(self, value: Union[int, str]) -> Temp:
        temp = self.freshTemp()
        self.func.add(LoadImm4(temp, value))
        return temp
    ```

    `self.freshTemp()`分配了一个虚拟寄存器 `temp` ，并且产生了一条立即数加载语句（你可以认为现在的所有指令就是用一个大数组存放了起来）。至此，我们翻译出了第一条语句，将2023 load到一个虚拟寄存器 `temp` 中。剩下的部分，对着代码和上面的AST看一下相信大家也知道发生了什么了。

    到此为止我们得到的TAC代码如下：

    ```asm
    FUNCTION<main>:
    _T0 = 2023
    _T1 = - _T0
    return _T1
    ```

    现在尝试运行 `python main.py --input example.c --tac` 看看效果吧。

* 怎么从TAC到汇编代码

    这一步是 `Asm.transform` 函数(backend/asm.py)处理的，`Asm.transform` 接受一个 TAC 输入，输出汇编代码。
    
    ```python
    def transform(self, prog: TACProg):
        analyzer = LivenessAnalyzer()

        for func in prog.funcs:
            pair = self.emitter.selectInstr(func)
            builder = CFGBuilder()
            cfg: CFG = builder.buildFrom(pair[0])
            analyzer.accept(cfg)
            self.regAlloc.accept(cfg, pair[1])

        return self.emitter.emitEnd()
    ```

    我们先忽略`LivenessAnalyzer`和`CFG`以及寄存器分配的部分（助教写了一个非常简单暴力的寄存器分配，如果你觉得它不够好，你可以在后面的step换掉它），实际上，我们这里最主要的是`selectInstr`，`selectInstr`函数中，我们也采用了visitor模式遍历指令序列， `_T0 = 2023` 这句比较直接，我们也能较为容易的想到一个简单的汇编指令对应，这句的翻译我们不在赘述，主要讲讲和`_T1 = - _T0` 和 `return _T1`翻译过程发生了什么。
    
    先看`visitUnary`函数：

    ```python
    def visitUnary(self, instr: Unary) -> None:
        op = {
            TacUnaryOp.NEG: RvUnaryOp.NEG,
            # You can add binary operations here.
        }[instr.op]
        self.seq.append(Riscv.Unary(op, instr.dst, instr.operand))
    ```
    这里将中端的`TacUnaryOp.NEG`翻译为了后端的`RvUnaryOp.NEG`，在后端输出汇编时，我们直接将`RvUnaryOp.NEG`转换为小写字符串取了11位以后的字符，直接输出为`neg`（参考`Unary.__str__`函数），因此后续希望添加其他后端的符号时，你应该直接在`RvUnaryOp`中增加对应的同名的enum字段。

    **你可以试试，将`RvUnaryOp.NEG`中名字改为`RvUnaryOp.XXX`看看输出的汇编代码会发生什么变化吧。**

    再看`visitReturn`函数，我们这里的`return`是一个带返回值函数的`return`
    
    ```python
    def visitReturn(self, instr: Return) -> None:
        if instr.value is not None:
            self.seq.append(Riscv.Move(Riscv.A0, instr.value))
        else:
            self.seq.append(Riscv.LoadImm(Riscv.A0, 0))
        self.seq.append(Riscv.JumpToEpilogue(self.entry))
    ```

    这里会进入第一个分支，由于 Risc-V 的调用约定将A0寄存器定为存放返回值的寄存器，因此在返回时我们产生了一条Move指令，这里的`instr.value`则是返回值对应的表达式使用的寄存器。

    你可能会觉得，这一步不就是将 TAC 一一对应为一个汇编指令序列嘛，有什么必要吗？其实这一步是必要的，首先有的中间表示可能无法由一条汇编指令完成，比如`T2 = T1 || T0`，这里的逻辑或需要将T1、T0进行或操作后，再判断其值是否为`1`。为什么这一步不在产生 TAC 时就处理了？因为我们希望中间表示能在一定程度上与平台无关（不同后端目标架构的指令选择可能存在较大差异），中间表示有一定抽象能力能简化整体编译器的设计。

    物理寄存器分配我们暂时跳过。至此我们已经完成了从源代码到汇编代码的翻译。
    
    现在尝试运行 `python main.py --input example.c --riscv` 看看效果吧。

## 思考题

1. 在我们的框架中，从 AST 向 TAC 的转换经过了 `namer.transform`, `typer.transform`两个步骤，如果没有这两个步骤，以下代码能正常编译吗，为什么？

    ```c
    int main(){
        return 10;
    }
    ```

2. 我们的框架现在对于main函数没有返回值的情况是在哪一步处理的？报的是什么错？

3. 为什么框架定义了 `frontend/ast/tree.py:Unary`、`utils/tac/tacop.py:TacUnaryOp`、`utils/riscv.py:RvUnaryOp` 三种不同的一元运算符类型？