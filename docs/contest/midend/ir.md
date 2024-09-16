# 中间表示设计

这里我们以一种经典 IR —— 三地址码为例，介绍中间表示的设计。

## 三地址码

**三地址码**（Three Address Code, TAC）是一种经典的 IR 设计，TAC 看起来很像汇编，与汇编最大的区别在于 —— 汇编里面使用的是目标平台（如 risc-v, x86, mips）规定的物理寄存器，其数目有限；而 TAC 使用的是 **“虚拟寄存器”** （也可以称作临时变量），其数目不受限制，可以任意使用（这意味着直接将临时变量转化为物理寄存器可能会出现寄存器不够用的情况）。**在后端生成汇编代码时，我们再考虑如何为临时变量分配物理寄存器的问题。**

```asm
main:                  # main 函数入口标签
    _T0 = 1            # 加载立即数
    _T1 = _T0          # 临时变量赋值操作
    _T2 = ADD _T0, _T1 # 加法操作 _T2 = _T0 + _T1
    _T3 = NEG _T0      # 取负操作 _T3 = -_T0
    return _T2         # 函数返回
```

以上给出了一份 TAC 示例程序。请注意 TAC 代码只是一种中间表示，并不需要像汇编语言那样有严格的语法。因此，可以自由选择输出 TAC 代码的格式，只要方便自己调试即可。例如，你也可以将 _T2 = ADD _T0, _T1 输出成 _T2 = _T0 + _T1。下面是另一个IR输出格式的例子：
```asm
i32 main() {
_B0:
    i32 _T0 = 1
    i32 _T1 = _T0
    i32 _T2 = _T0 + _T1
    i32 _T3 = -_T0
    return i32 _T2
}
```
你会发现，这种IR输出格式包含了一些类型信息，也更加易读。

TAC 指令与汇编指令比较类似，每条 TAC 指令由操作码和操作数（最多3个，函数调用除外，由于函数参数可能有多个，使用严格的三个操作数反而会使得函数实现更为复杂）构成。操作数可能会有：临时变量、常量、标签（可理解为常量地址）和全局变量。

我们来思考一下，如果需要完整描述源程序的语义，需要哪些语句？

- 算术语句：这是计算机最基础的语义。
    - 二元运算（如加、减、乘、除）
        - 形式：dst = op src1, src2
        - 示例：_T2 = ADD _T0, _T1
    - 一元运算（如取负、取位反）
        - 形式：dst = op src
        - 示例：_T3 = NEG _T0
- 跳转语句：用于实现程序的控制流，如循环和条件跳转，通常结合标签使用。
    - 条件跳转语句
        - 形式：branch cond, label1, label2
        - 示例：branch _T0, _L1, _L2
    - 无条件跳转语句
        - 形式：jump label
        - 示例：jump _L0
- 函数调用语句
    - 形式：dst = call (func_name, arg1, arg2, ...)
    - 示例：_T2 = call (foo, _T0, _T1)
- 赋值语句
    - 形式：dst = src
    - 示例：_T2 = _T0
- 访存语句
    - 加载操作：dst = load addr, offset
    - 示例：_T2 = load _T0, 0
    - 存储操作：store src, addr, offset
    - 示例：store _T0, _T1, 0
- 内存申请语句（注意区分，这里指编译器静态分配，与运行时动态分配的 malloc 不同，主要用于在栈上分配内存）
    - 形式：dst = alloc size
    - 示例：_T2 = alloc 40
- 返回语句
    - 形式：return src
    - 示例：return _T0

有了这些语句以后，我们的IR就可以描述源程序的语义了。

## 内存数据结构

中间表示是一种内存数据结构，不仅需要方便**阅读**，还需要方便**进行后续操作**（如优化、翻译）。

我们可以为所有指令定义一个基类 `Instruction`，然后根据不同的指令类型定义不同的子类。

```c++
struct Instruction {
    Type type;
};
```

下面以二元运算指令为例，展示如何定义一个具体的指令类。

二元运算需要两个操作数，并且会产生一个计算结果。

而操作数可能是一个立即数，也可能是一个变量。例如以下的情况：

```
_T2 = ADD _T0, _T1
_T3 = ADD _T0, 2
```

因此为了指令实现方便，我们可以将操作数定义为一个如下的结构体：

```c++
struct Operand {
    union{
        int value;
        int reg_id;
    };
    bool is_reg;
    ... ...
};
```

我们使用一个 `union` 来存储操作数的值或者寄存器编号，使用一个 `bool` 来标记操作数是否是一个寄存器。当然，你可以要求操作数必须是寄存器，这样就不需要 `is_reg` 这个标记了。这样你需要增加一条指令，将立即数分配到一个寄存器中。

有了操作数，我们就可以定义指令了，我们将二元运算指令定义为如下的结构体，其中Opcode是操作码，用来标记不同的二元运算类型，src1和src2是两个操作数，dst是运算结果存放的寄存器：

```c++
enum Opcode {
    ADD, SUB, MUL, DIV
};

struct Binary : public Instruction {
    Opcode opcode;           // 操作码
    Operand src1;            // 操作数一
    Operand src2;            // 操作数二
    Operand dst;             // 目标寄存器
};
```

一元运算指令的定义与二元运算指令的定义类似，这里不再赘述。

跳转语句应该怎么定义？这里我们需要引入基本块的概念。

在中端进行优化时，我们需要进行[数据流分析和控制流分析](../../step6/dataflow.md)，控制流分析过程中我们会将程序分解为多个基本块，基本块是一系列连续的指令序列，基本块内部指令序列的执行顺序是固定的，且不会被其他指令打断。我们可以将基本块定义为如下的结构体：

```c++
struct BasicBlock {
    std::vector<Instruction *> instructions;
    std::string label;
};
```

基本块的引入可以让我们便捷地进行各种编译优化，同时也简化了跳转语句的设计，只需要一个目标基本块即可：

```c++
struct Jump : public Instruction {
    BasicBlock *target; // 跳转目标
};
```

我们是以函数为单位来组织基本块的，函数定义为如下的结构体：

```c++
struct Function {
    std::string name;
    std::vector<BasicBlock> blocks;
};
```

整个程序又是由多个函数和全局变量组成的，因此我们可以将程序定义为如下的结构体：

```c++
struct Program {
    std::vector<Function *> functions;
    std::vector<GlobalVariable *> globals;
};
```

你会发现，我们的程序组织成了一个树状结构，即 `Program` 包含多个 `Function`，每个 `Function` 包含多个 `BasicBlock`，每个 `BasicBlock` 包含多条 `Instruction`。

一些tips：
- 你可以在`Instruction`的层次上再次进行抽象，将运算指令和跳转分开，设计专门的运算指令类和跳转指令类，这样可以让程序的结构更加清晰，比如你可以将 `Binary` 和 `Unary` 都继承自 `Arithmetic`，将 `Jump` 继承自 `ControlFlow`， `Arithmetic` 和 `ControlFlow` 都继承自 `Instruction`。
- 你可以在`Instruction`中添加一些成员变量，如`use`和`def`，用于在数据流分析后记录一些中间结果用于优化。
- 你完全可以不按照我们给出的这些结构来设计你的 IR，这里有一些参考：
    - [北大编译实验Koopa IR](https://pku-minic.github.io/online-doc/#/lv0-env-config/koopa)
    - [LLVM IR](https://llvm.org/docs/LangRef.html)

### 静态单赋值（SSA）

进一步地，你可以实现符合[静态单赋值](./ssa.md)要求的 IR ，静态单赋值的 IR 在编译器中有着广泛的应用，比如 LLVM 的 IR 就是一种静态单赋值的 IR。在静态单赋值的 IR 中，每个变量只被赋值一次，这使得编译器可以更容易地进行优化。