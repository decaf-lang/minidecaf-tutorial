# 实验指导 parser-stage：自顶向下语法分析器

在 Stage1-2 中，实验框架使用了 bison（C++ 框架）或 ply（Python 框架）作为语法分析器，解析 MiniDecaf 程序并生成 AST。

在 parser-stage 中，我们将结合课堂上学习的 LL(1) 分析方法，完成一个**手工实现的递归下降**语法分析器。为了降低难度和工作量，将提供分析器的基本框架和部分实现，同学们只需要补全代码片段即可。所实现的手工语法分析器，只需要支持 [**Step1-6 的语法**](spec.md)。

## 准备工作

parser-stage 不涉及中端、后端部分，所以请同学们将 stage2 中完成的中后端代码合并到 parser-stage 的实验框架上。具体的操作可以参考如下步骤，本步骤所需要的额外文件请在[此处链接](https://cloud.tsinghua.edu.cn/d/9b34fdf53a3c48b8bc52/)获取，C++ 的文件在 cpp/ 下，Python 的文件在 python/ 下：

```bash
$ git switch parser-stage
$ git merge stage-2
```

**对于 C++ 框架**，在切换到 `parser-stage` 分支之后进行如下操作：

1. 将[上述链接](https://cloud.tsinghua.edu.cn/d/9b34fdf53a3c48b8bc52/)中的 `my_parser.hpp` 及 `my_parser.cpp` 放入 `src/frontend/` 中。
2. 使用上述链接中的 `scanner.l` 覆盖原有的 `scanner.l`。
3. 对于 `src/Makefile` 和 `src/compiler.hpp` 的修改分为以下两种情况：
   1. 如果你没有修改过 `Makefile` 和 `compiler.hpp` ，直接使用上述链接中的同名文件覆盖即可。
   2. 如果你修改过，请按照下述方法在文件中添加相关内容：

**对于 Python 框架**，只需要将我们下发的 parser-stage 文件覆盖在 stage2 上即可。

**需要注意的是**，parser-stage 的实验相对于其他 stage 是独立的，因此你在开始做 stage3 实验时，应从 stage2 中完成的代码开始（而不是 parser-stage）：

```bash
$ git switch stage-3
# 注意不要从parser-stage merge
$ git merge stage-2
```

## 背景知识

如果你已经很熟悉自顶向下语法分析、自底向上语法分析的原理，可以跳过这部分。这里我们只对两种语法分析方法进行简单介绍，**详细原理请参考课件**。

bison/ply 自动生成的语法分析器，属于 LALR(1) 语法分析，是**自底向上**的语法分析方法。
     
具体来说，维护一个符号栈，每一步进行移进（shift）将新的 token 加入栈顶，或规约（reduce）将栈顶的一些符号组成产生式，从语法树的最底层开始向上构建节点，最终获得一棵 AST。
     
如对于算术表达式 `a + b + c * (d + e)`，

使用的语法为：
```
    Expr -> Expr '+' Expr | Expr '*' Expr | '(' Expr ')'
    Expr -> 'a' | 'b' | 'c' | 'd' | 'e'
```

自底向上语法分析的过程是: 

1. 不断移进直到符号栈内包含 `'a' '+' 'b'`，检查下一个符号为 `'+'`，进行一次规约，获得 `a + b` 组成的 Expr 节点，并压栈。
2. 继续移进直到栈内包含 `Expr '+' 'c' '*' '('  'd' + 'e'`，检测到下一个符号为 `')'`，进行一次规约, 获得 `d + e` 对应的 Expr 节点，并压栈。
3. `Expr '+' 'c' '*' '('  Expr ')'`，继续规约，依次规约括号表达式、乘法表达式、加法表达式，获得最终的语法树根节点 Expr。

而**自顶向下**语法分析的过程是:

1. 从解析根节点 Expr 开始，从左向右读取 `'a' '+'` 后，判定使用产生式 `Expr -> Expr + Expr`，来推导根节点，将 `'a'` 对应为加号左侧的 Expr，将剩余的 `b + c * (d + e)` 对应为加号右侧的 Expr，递归解析，用递归解析返回的结果来构造根节点。

2. 在递归解析 `b + c * (d + e)` 的过程中，读取到 `'b' '+'`，就判定使用 `Expr -> Expr + Expr` 来进行下一步推导。然后分别递归解析 `'b'` 和 `c * (d + e)`。

3. 接下来读取到 `c *` 的时候，再次决定递归，分别推导 `'c'` 和 `(d+e)`。

注意到，尽管这里从根节点开始选择产生式，是自顶向下的，但对语法树节点的构造，仍需要在递归函数退出、返回下层语法树节点之后，自底向上地进行构造。

## 任务描述

你需要：
1. 使用提供的 parser-stage 框架替换你的编译器中的 parser 部分，完善框架中的实现，**通过 Step1-6 的测试**。
2. 本步骤你需要修改的代码均有 `TODO` 标出，并有相关的引导注释。其中 C++ 框架需要修改的文件为 `src/frontend/my_parser.cpp`，Python 框架需要修改的文件为 `frontend/parser/my_parser.py`。
3. 完成实验报告（具体要求请看实验指导书的首页）。