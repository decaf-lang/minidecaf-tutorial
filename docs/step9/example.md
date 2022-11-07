# step9 实验指导

本实验指导使用的例子为：

```C
int func(int x, int y);
int main() { return func(1, 2); }
int func(int x, int y) { return x + y; }
```

## 词法语法分析

针对函数特性，我们需要设计 AST 节点来表示它，给出的参考定义如下：

| 节点 | 成员 | 含义 |
| --- | --- | --- |
| `Function` | 返回类型 `return_type`，函数名 `ident`，参数列表 `params`，函数体 `body` | 函数 |
| `Parameter` | 参数类型 `var_type`，变量名 `ident` | 函数参数 |
| `Call` | 调用函数名 `ident`，参数列表 `argument_list` | 函数调用 |

## 语义分析

本步骤中引入了函数，和局部变量类似，不允许调用未声明的函数，也不允许重复定义同名函数（允许重复声明，但要求声明类型一致）。因此，需要在全局作用域的符号表里维护函数符号。函数符号存放在栈底的全局作用域中，在遍历 AST 构建符号表的过程中，栈底符号表一直存在，不会被弹出。

此外，由于函数体内部除了局部变量以外，还有**函数参数**（argument）。因此，我们进入一个函数，开启函数体局部作用域时，需要将所有的参数加进该作用域的符号表中。举例来说，如果我们将示例改成：

```C
int func(int x, int y) { int x = 1; return x + y; }
```

那么语义检查时应当报错。

### Python 框架

`frontend/symbol/funcsymbol.py` 里实现了函数符号。

### C++ 框架

`symb/symbol.hpp` 中 Function 类表示函数符号。`scope/scope.hpp` 中，FuncScope 表示函数作用域。

## 中间代码生成

为了实现函数，我们需要设计两条中间代码指令，分别表示设置参数和函数，给出的参考定义如下：

> 请注意，TAC 指令的名称只要在你的实现中是一致的即可，并不一定要和文档一致。

| 指令 | 参数 | 含义 |
| --- | --- | --- |
| `PARAM` | `T0` | 将 T0 设置为下一个参数 |
| `CALL` | `LABEL` | 调用函数 LABEL |

假设我们有若干个参数，可以依次使用 PARAM 命令将它们加入参数列表。在调用函数时，这些参数的值会自动依次按顺序装载到临时变量 _T0, _T1 ... 中。比如我们有这样一段 TAC 程序：

```assembly
PARAM A
PARAM B
PARAM C
XX = CALL XXX
```

那么，在进入 XXX 函数时，相当于执行了：

```assembly
_T0 = A
_T1 = B
_T2 = C
```

因此，示例可以对应如下的 TAC 程序：

```assembly
func:
	_T2 = ADD _T0, _T1
    return _T2        # 参数 x 和 y 分别对应 _T0, _T1
main:
    _T0 = 1
    PARAM _T0         # 将 _T0 的值作为参数 x
    _T1 = 2
    PARAM _T1         # 将 _T1 的值作为参数 y
    _T3 = CALL func   # 调用函数
    return _T3
```

同学们可以使用这种参考的实现形式，也可以自行思考传参的处理方法。

> 在 step9 之后，C++ 框架中出现了新的三地址码指令（PARAM、CALL等），因此你需要参考 `tac/dataflow.cpp` 文件开始的注释修改相应指令的数据流信息，具体的修改方式取决于你定义的三地址码指令的输入和输出特点。
>

## 目标代码生成

```assembly
    .text
    .global main

func:
    # start of prologue
    addi sp, sp, -56
    # end of prologue

    # start of body
    sw a0, 0(sp)
    sw a1, 4(sp)
    lw t0, 0(sp)
    lw t1, 4(sp)
    add t2, t0, t1
    mv t0, t2
    mv a0, t0
    j func_exit
    # end of body

func_exit:
    # start of epilogue
    addi sp, sp, 56
    # end of epilogue

    ret

main:
    # start of prologue
    addi sp, sp, -56
    sw ra, 52(sp)
    # end of prologue

    # start of body
    li t0, 1
    li t1, 2
    mv a0, t0
    mv a1, t1
    call func
    mv t0, a0
    mv a0, t0
    j main_exit
    # end of body

main_exit:
    # start of epilogue
    lw ra, 52(sp)
    addi sp, sp, 56
    # end of epilogue

    ret
```

首先你需要参考之前步骤中实现的方法，**翻译本步骤中新增的中间代码指令**。

接下来详细介绍函数调用的步骤和约定，以及函数调用及返回过程中栈帧的变化。

### 函数调用

程序代码里的一个函数调用，包含了下面一系列的操作：

1. 准备参数，完成传参。
2. （汇编）保存 caller-saved 寄存器。
3. 执行汇编中的函数调用指令，开始执行子函数直至其返回。
4. （汇编）恢复 caller-saved 寄存器。
5. 拿到函数调用的返回值，作为函数调用表达式的值。

上述步骤 1-5 称为调用序列（calling sequence）。然而，调用序列中有一些问题需要解决：如何进行参数传递？如何获取函数返回值？调用者（caller）和被调用者（callee）需要保存哪些寄存器，如何保存？调用者和被调用者通常对以上问题约定解决方式，并同时遵守这些约定。这些调用者与被调用者共同遵守的约定称为**调用约定**（calling convention）。调用约定通常在汇编层级使用，汇编语言课上也有涉及。因为汇编语言是低级语言，缺乏对函数的语言特性支持，只有标号、地址、寄存器，所以需要调用约定，规定如何用汇编的语言机制模拟函数调用。

### 调用约定

实验测例中有与 gcc 编译的文件相互调用的要求，因此，大家需要实现标准调用约定。

#### RISC-V 的标准调用约定（gcc 使用的、和 MiniDecaf 相关的）

1. caller-saved 和 callee-saved 寄存器

   ![](./pics/reg.png)

   上表给出 RISC-V 中 32 个整数寄存器的分类。所谓 caller-saved 寄存器（又名易失性寄存器），是指不需要在各个调用之间保存的寄存器，如果调用者认为在被调用函数执行结束后仍然需要用到这些寄存器中的值，则需要自行保存。所谓 callee-saved 寄存器（又名非易失性寄存器），指这些寄存器需要在各个调用之间保存，调用者可以期望在被调用函数执行结束后，这些寄存器仍保持原来的值。这要求被调用者，如果使用这些寄存器，需要先进行保存，并在调用返回之前恢复这些 callee-saved 寄存器的值。

   具体的保存方法并不限制，但一般都使用栈来保存。

2. 函数参数以及返回值的传递

   函数参数（32 位 int）从左到右存放在 a0 - a7 寄存器中，如果还有其他参数，则以从右向左的顺序压栈，第 9 个参数在栈顶位置。同学们可以使用编写一个带有多个参数的函数并进行调用，然后用 gcc 编译程序进行验证。

   返回值（32 位 int）放在 a0 寄存器中。

### 提示
关于测试样例：
我们的测试脚本会将你的编译器生成的汇编代码与我们提供的运行时框架一起通过 gcc 链接得到可执行文件，检查运行结果。你可以查看测试文件夹中的 `runtime.c`,`runtime.h`,`runtime.s` 来查看我们预定义的函数。

C++框架中：

1. 框架中会在生成的汇编中在函数名前面加上下划线 `_`，如果链接时出现问题请检查是不是下划线导致的。

2. 由于调用时涉及将参数放到寄存器中，如果原来的寄存器中已经分配给了其他虚拟寄存器，那么你需要将寄存器先保存（spill）到栈上，但是这个过程你需要小心地处理Liveout集合，以下面三地址码为例:
    ```assembly
    func:
        _T2 = ADD _T0, _T1
        return _T2        # 参数 x 和 y 分别对应 _T0, _T1
    main:
        _T0 = 1
        PARAM _T0         # 将 _T0 的值作为参数 x 放入a0寄存器
        _T1 = 2
        PARAM _T1         # 将 _T1 的值作为参数 y 放入a1寄存器
        _T3 = CALL func   # 调用函数
        return _T3
    ```
    在PARAM _T0这一行，我们要将虚拟寄存器T0作为参数x放入物理寄存器a0，假设此时T0在栈中，并且物理寄存器a0中存放了另一个虚拟寄存器T2，那么要先将T2 spill到栈中。
    即此时需要：
    1. 将T2放入栈中（即：spill T2）
    2. 从栈中将T0取出放入a0寄存器中

    但是我们的框架在spill一个寄存器时会考虑当前位置的liveout集合，假设T0在此后不再被用到，那么T0就不在当前位置的liveout集合中，也就是说在spill寄存器时T0可以被覆盖掉，这可能导致T2被spill到了T0所在的位置，覆盖了T0。
    ```c++
    void RiscvDesc::spillReg(int i, LiveSet *live) {
        std::ostringstream oss;
        Temp v = _reg[i]->var;
        if ((NULL != v) && _reg[i]->dirty && live->contains(v)) {
            RiscvReg *base = _reg[RiscvReg::FP];
            if (!v->is_offset_fixed) {
                _frame->getSlotToWrite(v, live);   // 此处选择了一个栈上的位置用于保存寄存器
            }
            ... ...
        }
        ... ...
    }
    ```
    因此如果你遇到需要将参数放到某个物理寄存器中并且原来物理寄存器中含有其他虚拟寄存器，那么你可以按照下面的方式做：
    ```c++
    void RiscvDesc::setRegParam(Tac *t, int cnt) {
        // 此处助教使用Tac的op0来存放需要当作参数的虚拟寄存器
        // 先将op0加入当前的LiveOut集合，这可以保证spillReg时候不会将op0覆盖
        t->LiveOut->add(t->op0.var);
        spillReg(RiscvReg::A0 + cnt, t->LiveOut);
        int i = lookupReg(t->op0.var);
        if(i < 0) {
            // 处理在栈上的情况
        } else {
            // 处理在其他寄存器中的情况
        }
    }
    ```


# 思考题
1. MiniDecaf 的函数调用时参数求值的顺序是未定义行为。试写出一段 MiniDecaf 代码，使得不同的参数求值顺序会导致不同的返回结果。
2. 为何 RISC-V 标准调用约定中要引入 callee-saved 和 caller-saved 两类寄存器，而不是要求所有寄存器完全由 caller/callee 中的一方保存？为何保存返回地址的 ra 寄存器是 caller-saved 寄存器？
