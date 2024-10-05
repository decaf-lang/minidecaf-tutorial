# step2 实验指导
我们按照上一节划分的编译器阶段，分阶段给出 step2 实验指导。本实验指导使用的例子为：

> 需要注意的是，我们为了简化描述，提取出了测试用例中和本步骤最相关的部分，实际的测试用例还是一个完整的，带有主函数的 MiniDecaf 程序。

```C
-1
```

## 词法语法分析

在 step2 中，我们引入了一元运算，因此需要引入新的抽象语法树节点：

| 节点 | 成员 | 含义 |
| --- | --- | --- |
| `Unary` | 操作数 `operand`，运算类型 `op` | 一元运算 |

注意由于各种一元运算的形式是一样的，只是运算规则不同，所以用统一的一元运算节点来表示，在后续步骤中，再根据具体的运算种类翻译为不同的 TAC 与 RISC-V 指令。

## 语义分析

由于现在 return 语句的返回值不再是整型常量，而是表达式，因此语义分析时需要**递归地访问运算操作结点的子结点**，才能访问到作为叶子结点的整型常量，完成 step1 中实现的整型常量越界检查。

代码没有特别需要修改的地方。

## 中间代码生成
在 step1 中，我们只需为 return 语句的返回的整型常量分配一个临时变量即可。而从 Step2 开始，语法树上出现了各种运算操作结点。在生成 TAC 的过程中，我们需要为运算结点分配一个临时变量，并生成一条指令，该指令根据子结点的临时变量进行计算，将结果赋予该结点的临时变量。

针对取负操作，我们显然需要设计一条中间代码指令来表示它，给出的参考定义如下：

> 请注意，TAC 指令的名称只要在你的实现中是一致的即可，并不一定要和文档一致。

| 指令 | 参数 | 含义 |
| --- | --- | --- |
| `NEG` | `T0` | 对参数取负 |

按照上文说的，-1 在语法树上对应父-子两个结点，父结点为取负操作，子结点为常量 1。在生成过程中，首先使用 Visitor 模式递归地访问子结点，我们使用一个临时变量加载该立即数。之后，在父结点，我们根据子结点的临时变量，生成一条取负指令，将这条指令得到的目标临时变量设置为父结点的临时变量。

因此，测例可以翻译成如下的中间代码：

```asm
_T0 = 1
_T1 = NEG _T0
```

## 目标代码生成
step2 目标代码生成步骤的关键点在于，针对中间代码指令，选择合适的 RISC-V 指令来完成翻译工作。以 NEG 中间表达指令为例，RISC-V 汇编中有 neg 指令与其对应，因此上述中间代码可以翻译为如下的 RISC-V 汇编：

```assembly
li t0, 1
neg t1, t0
```

如果你不知道某个运算符应该翻译成怎样的汇编代码，你可以看[这里](../ref/riscv.md)

## 实现细节

>  关于实现细节，对应的代码位置在下面给出，代码中提供注释供大家学习。

相比于step 0, 我们实现了把返回值从一个整数（如：`2024`、`1`）变成单目表达式（如：`-1`），则在这一步中你可能需要进行以下操作（实际上这些实现已经在框架里提供）：

首先，我们应该把 `-` 看作一个符号，而不应该将 `-1` 看作一个整体，因为我们还可能遇到 `-x` 这种求一个变量的相反数的操作，如果将其分开处理则会增加我们的工作量。因此我们需要在词法分析中加入对 `-` 的处理。

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
                    |- (expr) IntLiteral(1)
```

看到这里，你可能会好奇，为什么这里多了如 (expr) Unary 这样的奇怪的 AST 节点。在编译器中，我们将所有的值、或者运算产生的结果称为一个表达式。比如 `1` 这个数字是一个表达式， `-1` , `y-x`同样也是表达式，其会生成一个值。而带返回值的 `return` 语句需要一个值，我们可以理解为带返回值的 `return` 语句后需要接一个表达式，这样在语义上才是正确的（例如，我们能见到`return 1;`这样的语句，但是不会见到`return if;`这样的语句，因为 `if` 并不是一个会产生值的表达式）。

### 词法分析 & 语法分析
    
在 `frontend/lexer/lex.py` 里加入新的 lex token 定义，以便lexer可以解析 `-`：

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

### 怎么从 AST 变为 TAC 的？

什么是 [TAC](../step1/arch.md#三地址码) ，如果你没读前面的章节，你可以快速看看这一部分。

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
                    |- (expr) IntLiteral(1)
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

`self.freshTemp()`分配了一个虚拟寄存器 `temp` ，并且产生了一条立即数加载语句（你可以认为现在的所有指令就是用一个大数组存放了起来）。至此，我们翻译出了第一条语句，将 `1` load 到一个虚拟寄存器 `temp` 中。剩下的部分，与这条语句的翻译也十分相似，因此不再赘述。

到此为止我们得到的TAC代码如下：

```asm
FUNCTION<main>:
_T0 = 1
_T1 = - _T0
return _T1
```

现在尝试运行 `python main.py --input example.c --tac` 看看效果吧。

### 怎么从TAC到汇编代码

这一步是 `Asm.transform` 函数(backend/asm.py)处理的，`Asm.transform` 接受一个 TAC 输入，输出汇编代码。

```python
def transform(self, prog: TACProg):
    analyzer = LivenessAnalyzer()
    
    for func in prog.funcs:
        emitter = RiscvAsmEmitter(Riscv.AllocatableRegs, Riscv.CallerSaved)
        reg_alloc = BruteRegAlloc(emitter)
        pair = emitter.selectInstr(func)
        builder = CFGBuilder()
        cfg: CFG = builder.buildFrom(pair[0])
        analyzer.accept(cfg)
        reg_alloc.accept(cfg, pair[1])

    return emitter.emitEnd()
```

我们先忽略`LivenessAnalyzer`和`Control Flow Graph(CFG)`以及寄存器分配的部分（助教写了一个非常简单暴力的寄存器分配，如果你觉得它不够好，你可以在后面的step换掉它），实际上，我们这里最主要的是指令选择（`selectInstr`），指令选择将中端TAC代码转换为riscv汇编代码，`selectInstr`函数中，我们也采用了visitor模式遍历指令序列， `_T0 = 1` 这句比较直接，我们也能较为容易的想到一个简单的汇编指令对应（`li _T0, 1`），主要讲讲和`_T1 = - _T0` 和 `return _T1`翻译过程发生了什么。

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


# 思考题

1. 我们在语义规范中规定整数运算越界是未定义行为，运算越界可以简单理解成理论上的运算结果没有办法保存在32位整数的空间中，必须截断高于32位的内容。请设计一个 minidecaf 表达式，只使用`-~!`这三个单目运算符和从 0 到 2147483647 范围内的非负整数，使得运算过程中发生越界。

> 提示：发生越界的一步计算是`-`。

# 总结
本步骤中其他运算符的实现逻辑和方法与取负类似，大家可以借鉴取负的实现方法实现剩下的逻辑非和按位非。并且，我们在实验框架中已经给出了取负的参考实现，希望能够帮助大家快速上手编译实验。
