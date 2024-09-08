# 勘误表

在这里我们会列出与实验相关的**勘误**，它会和[问答墙](https://docs.qq.com/doc/DY1hZWFV0T0N0VWph)上的勘误部分保持一致。同学们遇到问题时，请先在勘误表中查找查看是否已有解答。

&nbsp;

Q：使用 `pip install -r ./requirements.txt` 命令无法正确安装依赖？

A：如果你安装了多版本的 python，使用 pip 命令未必会对应 3.9 版本的包管理器。请尝试使用 `python3.9 -m pip install -r ./requirements.txt` 安装依赖。

&nbsp;

Q： 代码框架 step7 中，由 multi_nesting.c 生成的以下中间代码无法成功生成目标代码。

经过使用 print 法调试，发现是 `_T1` 所对应的寄存器在 `return _T1` 前就被释放了，后端会尝试到栈中寻找 `_T1` 并且不会找到，出现报错：
`utils.error.IllegalArgumentException: error: encounter a non-returned basic block`

请问是后端实现上有问题，还是这一部分本来就需要我们自己修改呢？

A：代码框架的后端除了要修改指令选择部分之外，还需要修改基本块 CFG，可以参见 BruteRegAlloc 的注释里给出的提示。

&nbsp;

Q：我怎样才能知道我的提交通过了所有测试用例？

A：可以通过本地测试或者通过 CI 结果可以判断是否通过了本阶段测例（不过你需要确保你的提交在对应的 branch 上，如 stage1 对应 stage-1 分支）。

&nbsp;

Q：如何提交课程报告？

A：

1. 请将实验报告以 pdf 格式提交到 git.tsinghua 自己的仓库中，放在仓库根目录下的 `reports/<branch-name>.pdf`，比如 stage 1 的实验报告需要放在 stage-1 这个 branch 下的 `reports/stage-1.pdf`。

2. 最新的 CI 会检查是否通过所有测例及是否有提交报告，只有通过所有测例且正确地提交报告，才会算作 pass。

3. 如果关于报告提交有任何问题，请及时联系助教。
