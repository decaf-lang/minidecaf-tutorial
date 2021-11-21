# 勘误表

在这里我们会列出与实验相关的**勘误**，它会和[问答墙](https://docs.qq.com/doc/DY1hZWFV0T0N0VWph)上的勘误部分保持一致。同学们遇到问题时，请先在勘误表中查找查看是否已有解答。

&nbsp;

Q：C++ 框架生成 RISC-V 汇编时有一些注释没法正常输出？

A：怀疑与平台相关，同学们可以做如下修改：

src/tac/tac.cpp 中，将 void Tac::dump 函数中输出每个 Tac 的四个空格修改为九个空格，如：

```C++
  case ASSIGN:
	os << "    " << op0.var << " <- " << op1.var;
	break;
修改为：
  case ASSIGN:
	os << "         " << op0.var << " <- " << op1.var;
	break;
```
**其余 Tac 类似。**

&nbsp;

Q：C++ 框架的 Variable 类实现有误？

A：`symb/symbol.hpp` 里面 Variable 类的 isLocalVar 函数是一段死代码。如果使用，请根据情况重写。

&nbsp;

Q: C++ 框架使用的第三方库 3rdparty/set.hpp 实现有误？（可能导致liveness分析出错）

A: 修改contains()的实现如下，判断集合是否为空。（之前有可能在集合空的情况下返回true)

```c++
bool contains(const _T e) const {
    const _T* p = std::lower_bound(begin(), end(), e);
	return (p!=end() && (*p == e);
}
```

并修改remove()的实现如下：

```c++
void remove(const _T e) {
    _T* p = std::lower_bound(begin(), end(), e);
    if (p!=end() && *p == e) {
        std::copy(p+1, end(), p);
        --_size;
    }
}
```

&nbsp;


Q：使用 `pip install -r ./requirements.txt` 命令无法正确安装依赖？

A：如果你安装了多版本的 python，使用 pip 命令未必会对应 3.9 版本的包管理器。请尝试使用 `python3.9 -m pip install -r ./requirements.txt` 安装依赖。

&nbsp;

Q：Python 框架无法正确输出三地址码？

A：非常抱歉，框架中输出时有一个小错误。在 `main.py` 中，输出三地址码时，请使用 `prog.printTo()` 语句；此外，想要输出带有缩进格式的抽象语法树，请使用如下语句：
```python
printer = TreePrinter(indentLen=<缩进空格数>)
printer.work(prog)
```

&nbsp;

Q： Python框架 step7 中，由 multi_nesting.c 生成的以下中间代码无法成功生成目标代码。

经过使用 print 法调试，发现是 `_T1` 所对应的寄存器在 `return _T1` 前就被释放了，后端会尝试到栈中寻找 `_T1` 并且不会找到，出现报错：
`utils.error.IllegalArgumentException: error: encounter a non-returned basic block`

请问是后端实现上有问题，还是这一部分本来就需要我们自己修改呢？

A：Python 框架的后端除了要修改指令选择部分之外，还需要修改基本块 CFG，可以参见 BruteRegAlloc 的注释里给出的提示。

&nbsp;

Q：我怎样才能知道我的提交通过了所有测试用例？

A：在 **2021.10.5 更新评测脚本**之后，现在通过 CI 结果可以直接判断是否通过了本阶段测例（不过你需要确保你的提交在对应的 branch 上，如 stage1 对应 stage-1 分支）。本地测试不受此次更新影响，因此更新本地的测试仓库 submodule 不是必须的。

&nbsp;

Q：实验指导书中step4的目标代码生成部分，给出的IR对应汇编指令不正确，修改了原有寄存器的值？

A：原先的汇编指令确实有问题，我们已经修正。感谢彭晋钧和郭昊同学！

&nbsp;

Q：如何提交课程报告？

A：

1. 请将实验报告以 pdf 格式提交到 git.tsinghua 自己的仓库中，放在仓库根目录下的 `reports/<branch-name>.pdf`，比如 stage 1 的实验报告需要放在 stage-1 这个 branch 下的 `reports/stage-1.pdf`。

2. 最新的 CI 会检查是否通过所有测例及是否有提交报告，只有通过所有测例且正确地提交报告，才会算作 pass。

3. 此前提到的 OJ 由于开发进度迟缓，我们本学期不会使用它作为作业评分的标准平台。

4. 如果关于报告提交有任何问题，请及时联系助教。

&nbsp;

Q：Python 框架寄存器分配中 allocRegFor 函数实现有错误？

A：请修改 bruteregalloc.py 中第 119 行处随机数生成的范围，将上界改为 `len(...) - 1`，避免溢出。感谢孟本源同学！

```python
reg = self.emitter.allocatableRegs[
    random.randint(0, len(self.emitter.allocatableRegs) - 1)
]
```

Q: Parser Stage中的`test-parser-stage.sh`无法正常使用?

A: 发布作业时打包有失误，请使用原有的`minidecaf-tests`中的`check.sh`测试脚本，将parser-stage的前端接入到原先的中后端来进行测试。