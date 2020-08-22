# 运行测试样例
测试相关的文件在 [minidecaf-tests](https://github.com/decaf-lang/minidecaf-tests) 里面，其中 `examples/` 是各个步骤的输入输出，测试脚本是 `check.sh`。

**测试的运行步骤** 如下
1. 用 `git clone` 把 minidecaf-tests 和一个参考实现克隆到同一个目录下面。
2. 进入 minidecaf-tests/，修改 `check.sh` 的 `gen_asm`，根据你选择的参考代码反注释某条命令
3. [可选] `sudo apt install parallel` 安装 parallel 以便并行测试，测试时间可缩短百分之七八十
4. [可选] 修改 `check.sh` 里面的 `JOBS`，控制要运行哪些测试点
5. 运行 `./check.sh` 即可。

测试运行的 **输出结果** 如下，OK 表示通过，FAIL 表示输出不对，ERR 表示编译错误。

```bash
$ ./check.sh
gcc found
qemu found
parallel found
OK testcases/step1/multi_digit.c
OK testcases/step1/newlines.c
...... 其他测试点，太长省略
OK testcases/step12/matmul.c
OK testcases/step12/quicksort.c
```

