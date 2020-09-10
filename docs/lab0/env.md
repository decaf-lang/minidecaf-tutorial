# 环境配置

## 必做：RISC-V 的 gcc 和 qemu

我们的编译器只生成 RISC-V 汇编，但是提供预编译的 gcc 和 qemu 模拟器。
gcc 用来把 C 编译到汇编、以及把汇编变成 RISC-V 可执行文件；qemu 用来运行 RISC-V 可执行文件。
不过我们提供的 gcc 和 qemu 只能在 Linux/Mac 下运行，Windows 的同学可以使用 WSL，或者运行一个虚拟机。
命令行基础操作我们就不赘述了，大家可以自己在网上查找资料。

```
                  你的编译器                gcc               qemu
MiniDecaf 源文件 ------------> RISC-V 汇编 -----> 可执行文件 --------> 输出
```

### Windows 用户

Win10 设置
1. 参考https://blog.csdn.net/daybreak222/article/details/87968078， 设置“开发者模式”以及“启用子系统功能”。

2. 打开Microsoft Store，搜索Ubuntu，选择ubuntu20.04.

3. 更新源：
 sudo vi /etc/apt/sources.list  ,并在文件最前面加入
 ```
 # 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
 deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
 # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
 deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
 # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
 deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
 # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
 deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
 # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse

 # 预发布软件源，不建议启用
 # deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
 # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
 ```

 然后执行命令：

 sudo apt-get update
 sudo apt-get upgrade

4. 安装qemu，执行命令： sudo apt-get install qemu-user

5. 安装riscv64-gcc：
 下载已编译的安装包 https://static.dev.sifive.com/dev-tools/riscv64-unknown-elf-gcc-8.3.0-2020.04.0-x86_64-linux-ubuntu14.tar.gz
 把安装包解压，根据解压路径把riscv64-unknown-elf-gcc-8.3.0-2020.04.0-x86_64-linux-ubuntu14\bin 加入PATH环境变量
配置结束

### Linux 用户

1. 从网络学堂下载 riscv-prebuilt.tar.gz 压缩包并解压（命令是 `tar xzf riscv-prebuilt.tar.gz`）

2. 安装工具链 `cp riscv-prebuilt/* /usr/ -r`

> 在第 2. 步，你可以选择不安装到系统目录下。相应的，你需要设置环境变量：
> `export PATH=$PATH:/path/to/riscv-prebuilt/bin`，把 `/path/to` 替换为你的解压目录

执行下面命令测试你 gcc 和 qemu 是否成功安装 [^1]：
1. 创建 `test.c` 文件，其中写入如下内容
```c
#include <stdio.h>
int main() { printf("Hello world!\n"); }
```

2. 编译 `test.c` 文件，`gcc` 应该输出一个可执行文件 `a.out`。但 `a.out` 是 RISC-V 可执行文件，所以我们的 X86 计算机无法运行。
```bash
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O3 -S test.c
$ ls a.out
a.out
$ ./a.out
bash: ./a.out: cannot execute binary file: Exec format error
```

3. 使用 qemu 执行 `a.out`
```bash
$ qemu-riscv32 a.out
Hello world!
```

### macOS 用户

1. 从[这里](https://static.dev.sifive.com/dev-tools/riscv64-unknown-elf-gcc-8.3.0-2020.04.0-x86_64-apple-darwin.tar.gz)下载预编译好的 RISC-V 工具链并解压。
2. 由于 macOS 不支持 QEMU 的用户态模式，我们使用 [Spike](https://github.com/riscv/riscv-isa-sim) 模拟器和一个简易内核 [riscv-pk](https://github.com/riscv/riscv-pk) 提供用户态程序的运行环境。网络学堂上提供了我们预编译的二进制程序包 spike-pk-prebuilt-x86_64-apple-darwin.tar.gz。你也可以使用 [Homebrew](https://brew.sh/) 安装 Spike [^2]：
```bash
$ brew tap riscv/riscv
$ brew install riscv-isa-sim
```

3. （可选）设置环境变量，以便每次使用时不需要输入完整路径。
4. 测试你 GCC 和 Spike 是否成功安装，详见[RISC-V 的工具链使用](./riscv.md)。

## 推荐：参考实现的环境

我们强烈推荐你选择一个[参考实现](../ref/intro.md)，并且先测试运行一下（见下一节），为此你需要配置参考实现的环境。
请根据自己的喜好选择一个，`git clone` 到本地，然后按照它的 README 配置好它的环境。

对于 git 的安装和使用请同学们自行查阅相关资料，也可以参考[这里](https://www.liaoxuefeng.com/wiki/896043488029600) 。每一个参考实现都是一个 git 分支，且都以 commit 的形式提供了每一个 step 的参考实现。同学们可以通过 `git log` 查看提交历史，通过 `git checkout` 查看每一个 step 的参考实现，或者通过 `git diff` 对比两个 step 之间的差异。

# 备注
[^1]: 开头的 `$ ` 表示接下来是一条命令，记得运行的时候去掉 `$ `。例如，让你运行 `$ echo x`，那你最终敲到终端里的是 `echo x`（然后回车）。如果开头没有 `$ `，那么这一行是上一条命令的输出（除非我们特别说明，这一行是你要输入的内容）。

[^2]: Homebrew 也提供了 riscv-pk，不过那是 64 位的，而我们预编译的是 32 位的。
