### 实验指导 step14：静态单赋值

本节实验指导使用的例子为：

```C
int main() {
  int x = 1;
  int cond = 1;
  if (cond > 0) {
    x = 1;
  } else {
    x = -1;
  }
  return x;
}
```

#### 词法语法分析

mem2reg 属于在中间代码基础上的优化，因此词法语法分析部分没有额外增加的内容。

#### 语义分析

mem2reg 属于在中间代码基础上的优化，因此语义分析部分没有额外增加的内容。

#### 中间代码生成

mem2reg 使得我们可以在生成中间代码时，使用 Alloc、Load 和 Store 的组合针对局部变量生成符合 SSA 要求的代码。

对于本节实验用例，一种可能的中间代码表示为：

```assembly
main:
  _T0 = ALLOC 4
  _T1 = ALLOC 4
  STORE _T0, 1
  LOAD _T2, _T0
  _T4 = GT _T2, 0
  BEQZ _T4, _L2
  STORE _T2, 1
_L1:
  LOAD _T5, _T2
  return _T5
_L2:
  _T6 = SUB 0, 1
  STORE _T2, _T6
  JUMP _L1
```

在此基础上，进行 mem2reg 转化：

```assembly
main:
  _T0 = GT 1, 0
  BEGZ _T0, _L2
_L1:
  _T2 = phi [1, main], [_T3, _L2]
  return _T2
_L2:
  _T3 = SUB 0, 1
  JUMP _L1
```

需要注意的是，所有的 Phi 指令应当在基本块的开头同时支持并行执行（即 Phi 指令的执行顺序对结果没有影响）。

在实现 mem2reg 时，我们需要首先对代码进行数据流分析，计算控制流图中的支配关系和每个基本块的支配边界。

> 相关的解释和详细说明可以参考：
> 如何构建 SSA 形式的 CFG：https://szp15.com/post/how-to-construct-ssa/

随后，我们需要实现 SSA 构造算法。一种常用的算法是将整个过程分为：插入 phi 函数和变量重命名，两个阶段。

在第一阶段，记录每个局部变量相关的 Alloc 和 Store 指令，并由此在基本块的开头插入 Phi 指令。

在第二阶段，遍历所有基本块，对其中局部变量相关的 Alloc，Load 和 Store 指令进行改写，以保证程序语义的正确性。在遍历一个基本块的所有指令后，维护该基本块的所有后继基本块中的 Phi 指令。

> 相关的解释和详细说明可以参考：
>
> Static Single Assignment Book 的 Chapter3：https://pfalcon.github.io/ssabook/latest/

#### 目标代码生成

将 Phi 指令翻译为目标代码的过程相对复杂，本节实验不对这部分做要求。