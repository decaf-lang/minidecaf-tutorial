## 推荐：运行实验框架
配好环境以后，我们强烈推荐你构建运行我们提供的实验框架初始代码。
> 接下来我们会用到 git。
> git 的安装和使用会在软件工程课上讲述，同学们也自行查阅相关资料，也可以参考[这里](https://www.liaoxuefeng.com/wiki/896043488029600) 。

1. 按照本文档的前几节（[RISCV 环境配置](./riscv_env.md)和[实验框架环境配置](./env.md)配置好实验环境。

2. 助教已经为每位同学在 git.tsinghua.edu.cn 创建了一个仓库，其中 minidecaf 的[测例仓库](https://git.tsinghua.edu.cn/compiler-21/minidecaf-tests)为其中的一个子模块，你可以通过以下指令来在克隆主仓库的同时克隆子模块 `git clone --recursive <repository>`。
由于测例仓库会有所更新，在克隆之后你需要在主仓库目录下使用 `git submodule update --remote --merge` 来手动更新。

3. 按照[测例](https://github.com/decaf-lang/minidecaf-tests)的 README 运行测试 step1，实验框架给出的初始代码可以通过 step1 的所有测例。

测试运行的 **输出结果** 大致如下。

```bash
$ STEP_UNTIL=1 ./check.sh
gcc found
qemu found
parallel found
OK testcases/step1/multi_digit.c
OK testcases/step1/newlines.c
...... 其他测试点，太长省略
```

