
# 静态单赋值

> 静态单赋值这一小节参考并改编自北航的编译课程实验文档：
> https://buaa-se-compiling.github.io/miniSysY-tutorial/challenge/mem2reg/help.html
> 在此表示感谢！

静态单赋值（Static Single Assignment, SSA）是编译器中间表示（IR）阶段的一个重要概念，它要求程序中每个变量在使用之前只被赋值一次。

例如，考虑使用 IR 编写程序计算 1 + 2 + 3 的值，一种可能的写法为：

```assembly
_T0 = 1
_T1 = 2
_T2 = 3
_T3 = _T0 + _T1
_T3 = _T3 + _T2
ret _T3
```
很遗憾，上述程序并不符合 SSA 的要求，因为其中变量 _T3 被赋值了两次。正确的写法应该为：
```assembly
_T0 = 1
_T1 = 2
_T2 = 3
_T3 = _T0 + _T1
_T4 = _T3 + _T2
ret _T4
```
#### 我们为什么要这样做呢？

因为 SSA 可以简化每个变量的属性，进而简化编译器的优化过程。

例如，考虑下面这段伪代码：

```assembly
y = 1
y = 2
x = y
```
很显然，其中变量 y 的第一次赋值是不必须的，因为变量 y 被使用前，经历了第二次赋值。对于编译器而言，确定这一关系并不容易，需要经过定义分析（Reaching Definition Analysis）的过程。在很多控制流复杂的情况下，上述过程将变得更加困难。

但如果将上述代码变为 SSA 形式：

```assembly
y1 = 1
y2 = 2
x1 = y2
```
上述关系变得更加显而易见，由于每一个变量只被赋值一次，编译器可以轻松地得到 x1 的值来自于 y2 这一信息。

正因如此，许多编译器优化算法都建立在 SSA 的基础之上，例如：死代码消除（dead code elimination）、常量传播（constant propagation）、值域传播（value range propagation）等。

#### 我们如何实现 SSA 呢？

例如，考虑使用 IR 编写程序使用循环计算 5 的阶乘。

按照 C 语言的思路，我们可能给出如下写法：

```assembly
_L0:
  _T0 = 0
  _T1 = 1
  _T2 = 2
  _T3 = _T0 + _T1  # int temp = 1
  _T4 = _T0 + _T2  # int i = 2
  _T5 = 5
_L1:
  _T6 = _T4 < _T5   # i < 5
  beqz _T6, _L3
_L2:                  # loop label
  _T3 = _T3 * _T4  # temp = temp * i
  _T4 = _T4 + _T1  # i = i + 1
  jump _L1
_L3:                  # break label
  ret _T3
```
我们注意到，变量 _T3 和 _T4 由于循环体的存在可能被赋值多次，因此上述写法并不符合 SSA 的要求。

一种可能的方案是使用 Phi 指令。Phi 指令的语法是 `<result> = PHI [<val0>, <label0>], [<val1>, <label1>] ...` 。它使得我们可以根据进入当前基本块之前执行的是哪一个基本块的代码来选择一个变量的值。

由此，我们的程序可以改写为：

```assembly
_L0:
  _T0 = 2
  _T1 = 1
_L1:
  _T2 = PHI [_T0, _L0], [_T6, _L2]  # int i = 2
  _T3 = PHI [_T1, _L0], [_T7, _L2]  # int temp = 1
  _T4 = 5
  _T5 = _T2 < _T4                   # i < 5
  beqz _T5, _L3
_L2:                                # loop label
  _T7 = _T3 * _T2                   # temp = temp * i
  _T6 = _T2 + _T1                   # i = i + 1
  jump _L1
_L3:                                # break label
  ret _T3
```
由此，上述程序中每一个变量只被赋值了一次，满足了 SSA 的要求。（注意，SSA 仅要求变量在静态阶段被单一赋值，而不是在运行时仅被赋值一次）

另一种可能的方案是使用 Alloca、Load 和 Store 的组合。SSA 要求中间表示阶段虚拟寄存器满足单一赋值要求，但并不要求内存地址如此。因此，我们可以在前端生成中间代码时，将每一个变量都按照栈的方式使用 Alloca 指令分配到内存中，之后每次访问变量都通过 Load 或 Store 指令显式地读写内存。使用上述方案编写的程序满足 SSA 的要求，且避免了繁琐地构造 Phi 指令，但频繁地访问内存将导致严重的性能问题。

#### 有没有更好的解决方案呢？

有，我们可以将两种方案结合起来。

在前端生成中间代码时，首先使用第二种方案利用 Alloca、Load、Store 指令快速地构建满足 SSA 要求的代码。
随后，在上述代码的基础上， 将其中分配的内存变量转化为虚拟寄存器，并在合适的地方插入 Phi 指令。
这一解决方案也被称为 mem2reg 技术。

mem2reg 使得我们可以在生成中间代码时，使用 Alloc、Load 和 Store 的组合针对局部变量生成符合 SSA 要求的代码。

举个例子，一种可能的中间代码表示为：

```assembly
main:
  _T0 = alloc 4
  _T1 = alloc 4
  store _T0, 1
  load _T2, _T0
  _T4 = _T2 > 0
  beqz _T4, _L2
  store _T2, 1
_L1:
  load _T5, _T2
  ret _T5
_L2:
  _T6 = 0 - 1
  store _T2, _T6
  jump _L1
```

在此基础上，进行 mem2reg 转化：

```assembly
main:
  _T0 = 1 > 0
  beqz _T0, _L2
_L1:
  _T2 = phi [1, main], [_T3, _L2]
  ret _T2
_L2:
  _T3 = 0 - 1
  jump _L1
```

需要注意的是，所有的 Phi 指令应当在基本块的开头同时支持并行执行（即在同一个基本块内的 Phi 指令的顺序对结果没有影响）。

在实现 mem2reg 时，我们需要首先对代码进行数据流分析，计算控制流图中的支配关系和每个基本块的支配边界。

> 相关的解释和详细说明可以参考：
> 如何构建 SSA 形式的 CFG：https://szp15.com/post/how-to-construct-ssa/

随后，我们需要实现 SSA 构造算法。一种常用的算法是将整个过程分为：插入 phi 函数和变量重命名，两个阶段。

在第一阶段，记录每个局部变量相关的 Alloc 和 Store 指令，并由此在基本块的开头插入 Phi 指令。

在第二阶段，遍历所有基本块，对其中局部变量相关的 Alloc，Load 和 Store 指令进行改写，以保证程序语义的正确性。在遍历一个基本块的所有指令后，维护该基本块的所有后继基本块中的 Phi 指令。

> 相关的解释和详细说明可以参考：
>
> Static Single Assignment Book 的 Chapter3：https://pfalcon.github.io/ssabook/latest/
