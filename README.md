# MiniDecaf 编译实验

## 实验概述
MiniDecaf [^1] 是一个 C 的子集，去掉了如 include/define/多文件/struct 等特性。
这学期的编译实验要求你从头开始实现一个编译器，把 MiniDecaf 代码编译到 RISC-V 汇编。

下面是 MiniDecaf 的快速排序，和 C 是一样的
```c
int qsort(int *a, int l, int r) {
    int i = l; int j = r; int p = *(a + (l+r)/2);
    while (i <= j) {
        while (*(a+i) < p) i = i + 1;
        while (*(a+j) > p) j = j - 1;
        if (i > j) break;
        int u = *(a+i); *(a+i) = *(a+j); *(a+j) = u;
        i = i + 1;
        j = j - 1;
    }
    if (i < r) qsort(a, i, r);
    if (j > l) qsort(a, l, j);
}
```

如目录所示，MiniDecaf 实验分为六大阶段，由十二个小步骤组成。
每个步骤，你的任务都是把 MiniDecaf 程序编译到 RISC-V 汇编。
**每步做完以后，你都有一个完整能运行的编译器。**
随着实验一步一步进行，MiniDecaf 语言会从简单变复杂，每步都会增加语言特性。

> * 我们提供一系列的参考实现，包含 Python/Rust/Java/C++ 的。遇到困难你可以参考他们做法、也可以复用他们的代码。
>
> * 编译器边边角角的情况很多，所以你的实现只要通过我们的测例就视为正确。


## 实验环境
我们只生成 RISC-V 汇编，但是提供预编译的 gcc 和 qemu 模拟器。
使用 gcc 你可以把汇编变成 RISC-V 可执行文件，使用 qemu 你可以运行 RISC-V 可执行文件。

```
                  你的编译器                gcc               qemu
MiniDecaf 源文件 ------------> RISC-V 汇编 -----> 可执行文件 --------> 输出
```

不过我们提供的 gcc 和 qemu 只能在 Linux/Mac 下运行，**Windows 的同学** 可以使用 WSL，或者运行一个虚拟机。
关于 WSL / 虚拟机使用，以及 Linux 基础操作，大家可以自己在网上查找资料。


## 实验提交
你需要使用 **git** 对你的实验做版本维护，然后提交到 **git.tsinghua.edu.cn**。
大家在网络学堂提交帐号名后，助教给每个人会建立一个私有的仓库，作业提交到那个仓库即可。
关于 git 使用，大家也可以在网上查找资料。

每次除了实验代码，你还需要提交 **实验报告**，其中包括
* 指导书里面思考题的回答
* 声明你参考以及复用了谁的代码

**晚交扣分规则** 是：
* 晚交 n 天，则扣除 n/15 的分数，扣完为止。例如，晚交三天，那你得分就要折算 80%。


## 备注
[^1]: 关于名字由来，往年实验叫 Decaf，所以今年就叫 MiniDecaf 了。不过事实上现在的 MiniDecaf 和原来的 Decaf 没有任何关系。
