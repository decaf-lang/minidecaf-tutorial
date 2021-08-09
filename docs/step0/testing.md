## 推荐：运行一个参考实现
配好环境以后，我们强烈推荐你选择一个[参考实现](../ref/intro.md)先测试运行一下（见下一节）。
> 接下来我们会用到 git。
> git 的安装和使用会在今年软件工程课上讲述，同学们也自行查阅相关资料，也可以参考[这里](https://www.liaoxuefeng.com/wiki/896043488029600) 。
> 每一个参考实现都是一个 git 分支，且都以 commit 的形式提供了每一个 step 的参考实现。
> 同学们可以通过 `git log` 查看提交历史，通过 `git checkout` 查看每一个 step 的参考实现，或者通过 `git diff` 对比两个 step 之间的差异。

1. 通过 `git clone` 把[测例](https://github.com/decaf-lang/minidecaf-tests)和某个参考实现克隆到同一个目录下面。
    > git.tsinghua 上有[镜像](https://git.tsinghua.edu.cn/decaf-lang/minidecaf-tests)，每 5 分钟更新一次
2. 按照参考实现的 README 配置好它的环境。
3. 按照[测例](https://github.com/decaf-lang/minidecaf-tests)的 README 运行测试

测试运行的 **输出结果** 大致如下。

```bash
$ ./check.sh
gcc found
qemu found
parallel found
OK testcases/step1/multi_digit.c
OK testcases/step1/newlines.c
...... 其他测试点，太长省略
```

