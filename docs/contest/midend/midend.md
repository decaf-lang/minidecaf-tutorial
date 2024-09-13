# 中端介绍

中端的设计包括：中间表示的设计、中端代码生成和中端优化。

## 中间表示

前端的解析和中端设计密不可分，通常，我们需要设计一个中间表示（Intermediate Representation, IR）来连接前端和后端。也只有我们定义好了中间表示，才能将来自于前端的AST转换为中端代码。

### 什么是中间表示？

中间表示（也称中间代码，intermediate representation / IR）是介于语法树和汇编代码之间的一种程序表示。 它不像语法树一样保留了那么多源程序的结构，也不至于像汇编一样底层。

由于源语言（MiniDecaf）和目标语言（RISC-V 汇编）一般存在较大的差别，因此直接把源语言翻译为目标语言中的合法程序通常是比较困难的。大多数编译器实现中所采取的做法，是首先把源语言的程序翻译成一种相对接近目标语言的中间表示形式，然后再从这种中间表示翻译成目标代码。中间表示（IR）的所带来的优势如下：

- 缩小调试范围，通过把 AST 到汇编的步骤一分为二。如果目标代码有误，通过检查 IR 是否正确就可以知道：是AST 到 IR 翻译有误，还是 IR 到汇编翻译有误。 将 AST 转换到汇编的过程分成两个步骤，每个步骤代码更精简，更易于调试。
- 适配不同指令集（RISC-V, x86, MIPS, ARM...）和源语言（MiniDecaf, C, Java...）。由于不同源语言的 AST 不同，直接从 AST 生成汇编的话，为了支持 N 个源语言和 M 个目标指令集，需要写 N * M 个目标代码生成模块。如果有了 IR，只需要写 N 个 IR 生成器和 M 个汇编生成器，只有 N + M 个模块。

- 便于优化，中间表示可以附带一些额外信息，比如类型信息、控制流信息等，这些信息辅助编译器进行优化。

例如以下是一个IR代码的例子：

```assembly
_main:
    _T1 = 0
    _T2 = 100
    _T3 = 0
_L0:
    _T4 = _T1 < _T2
    beqz _T4, _L1, _L2
_L1:
    _T3 = _T1 + _T3
    _T1 = _T3 + 1
    jump _L0
_L2:
    _T5 = 2
    ret _T5
```

从这个IR例子中，我们可以看到，相对于c语言，IR中没有了while、for这样的循环语句，而是通过标签和jump、branch指令来实现循环。高级语言的许多特性在IR中都被抹去了，让代码更加简洁，便于优化。而相对于汇编代码，IR中无需关注寄存器、函数调用的上下文切换等信息，与具体的硬件架构解耦。

我们将在[中间表示设计](./ir.md)中介绍IR设计时候需要考虑的地方和并列举一些实例。

## 中间代码生成

前端解析后，我们会得到一棵抽象语法树，接下来我们需要将这棵抽象语法树转换为中间代码。依据你设计的IR，你需要在保证语义的情况下，将AST用你的IR表示出来。可以参考基础实验框架中`frontend/tacgen/`的代码。

如以下是一个简单的例子：

```C
int main(){
    int a = 2;
    int b = 0;
    if(a)
        b = 1;
    else
        b = -1;
    return b;
}
```

生成的AST可能如下：
```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) VarDecl
                |- (type) TInt
                |- (ident) Identifier("a")
                |- (init) IntLiteral(2)
            |- (children[1]) VarDecl
                |- (type) TInt
                |- (ident) Identifier("b")
                |- (init) IntLiteral(0)
            |- (children[2]) If
                |- (cond) Identifier("a")
                |- (children[0]) Assign
                    |- (lhs) Identifier("b")
                    |- (rhs) IntLiteral(1)
                |- (children[1]) Assign
                    |- (lhs) Identifier("b")
                    |- (rhs) UnaryOp(NEG)
                        |- (expr) IntLiteral(1)
            |- (children[3]) Return
                |- (expr) Identifier("b")
```

你需要通过遍历AST的节点来将其转换为IR。例如，当你遇到一个`if`节点时，你可以先生成三个标签，一个用于表示`if`语句的开始，一个用于表示`else`语句的开始，一个用于表示整个`if`语句的结束。先生成一个判断语句，在生成if条件满足对应的标签以及代码，最后生成一个跳转语句，跳过else块。然后在生成else块的标签和代码。

例如上述代码转化为IR后可能如下：

```asm
_main:
    _T0 = 2  # 代表a = 2
    _T1 = 0  # 代表b = 0
    bnez _T0, _L0, _L1 # 如果a != 0，跳转到_L0，否则跳转到_L1
_L0:
    _T2 = 1  # 代表b = 1
    jump _L2 # 跳转到_L2，跳过else块
_L1:
    _T2 = -1 # 代表b = -1
    jump _L2 # 跳转到_L2
_L2:
    ret _T2
``` 

## 中端优化

中端的优化是编译器的一个重要组成部分，它可以在保持程序功能不变的前提下，提高程序的性能。中端优化的目标是提高程序的性能，减少程序的运行时间和资源消耗。中端优化的方法有很多，比如常量传播、死代码消除、循环不变量外提、循环展开、函数内联等。

一个经典的例子是常量传播。常量传播是指将一个常量值替换为它的值，以便于在中端直接完成一些计算以降低运行时开销。比如，对于下面的 IR 代码：

```asm
_T1 = 5
_T2 = _T1 + 6
_T3 = _T2 + 7
_T4 = _T3 + 8
_T5 = _T4 + 9
ret _T5
```

经过常量传播优化后，可以得到：

```asm
_T1 = 5
_T2 = 11
_T3 = 18
_T4 = 26
_T5 = 35
ret _T5
```

进一步如果我们进行死代码消除，可以得到：
> 死代码消除是指删除程序中没有用到的代码，以减少程序的运行时间和资源消耗。

```asm
_T5 = 35
ret _T5
```

中端优化依赖与数据流、控制流分析，你需要先了解一些数据流分析的基础知识才能进行一些中端优化。

我们的文档里在[数据流分析](../../step6/dataflow.md)中对数据流分析进行了简单介绍，你可以在这里了解一些数据流分析的基础知识。除了这个文档中介绍的数据流分析，还有很多其他的数据流分析方法，比如Use-Def链、Def-Use链、可达定义分析等。

我们在文档中对两个优化进行简单介绍，详见[常量传播](./cp.md)和[死代码消除](./dce.md)。

## 中端参考资料

本章中我们以几个简单的例子介绍了什么是中间表示、中端优化以及如何做中端优化。此外我们也将会在这里给出一些中端优化的参考资料，供大家学习。

- [GCM & GVM](https://courses.cs.washington.edu/courses/cse501/06wi/reading/click-pldi95.pdf) 

- [Engineering A Compiler](https://github.com/lighthousand/books/blob/master/Engineering%20A%20Compiler%202nd%20Edition%20by%20Cooper%20and%20Torczon.pdf)

- [LLVM IR](https://llvm.org/docs/LangRef.html)

- [SSA book](https://pfalcon.github.io/ssabook/latest/book-full.pdf)


## 预期目标

完成这部分内容后，你的编译器应该能将 MiniDecaf 程序翻译成 IR，并能够输出 IR。进一步地，如果你希望参加性能评测，你还需要实现一些中端优化。

