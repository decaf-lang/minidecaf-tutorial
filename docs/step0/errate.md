# 勘误表

在这里我们会列出与实验相关的**勘误**，它会和[问答墙](https://docs.qq.com/doc/DY1hZWFV0T0N0VWph)上的勘误部分保持一致。同学们遇到问题时，请先在勘误表中查找查看是否已有解答。

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

A：原先的汇编指令确实有问题，我们已经修正。
