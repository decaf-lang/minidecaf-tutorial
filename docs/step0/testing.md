## 推荐：运行实验框架
配好环境以后，我们强烈推荐你构建运行我们提供的实验框架初始代码。
> 接下来我们会用到 git。
> git 的安装和使用会在软件工程课上讲述，同学们也自行查阅相关资料，也可以参考[这里](https://www.liaoxuefeng.com/wiki/896043488029600) 。

1. 通过 `git clone` 把[测例](https://github.com/decaf-lang/minidecaf-tests)和实验框架实现克隆到同一个目录下面。

    > TODO：框架上传之后更新链接。

    C++ 和 Python 框架在同一个仓库的不同分支里面。

2. 按照参考实现的 README 配置好它的环境。

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

