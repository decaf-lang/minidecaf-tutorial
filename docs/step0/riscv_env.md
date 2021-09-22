# RISC-V 环境配置

## 必做：RISC-V 的 gcc 和 qemu

我们的编译器只生成 RISC-V 汇编，然后再使用 gcc 把 RISC-V 汇编变成 RISC-V 可执行文件，最后用 qemu/spike 等模拟器来运行 RISC-V 可执行文件。
> 注意这里的 gcc 和常说的 gcc 不一样。
> 常说的 gcc 运行在我们的 x86 机器上、把 C 编译到 x86 可执行文件；
> 而这里的 gcc 虽然也运行在我们的 x86 机器上，却要编译到 RISC-V 可执行文件。
> 这种“gcc 跑在 x86 却编译出 RISC-V 代码”的操作被称为交叉编译（cross compilation）。
>
> 因此我们不能直接使用有些系统自带的 gcc，这种 gcc 生成的可执行程序只能在你本机（x86）上运行。
> 我们需要下载安装 riscv64-unknown-elf-gcc，用来生成 RISC-V 可执行程序。

> 建议各位同学使用我们提供的 RISC-V 工具链，由 SiFive 预编译的较新版本的工具链对 32 位的支持存在问题。

我们提供了预编译的 riscv64-unknown-elf-gcc 和 qemu/spike 模拟器，不过只能在 Linux/Mac 下运行（qemu 对应 Linux，spike 对应 Mac），Windows 的同学可以使用 WSL，或者运行一个虚拟机。
命令行基础操作我们就不赘述了，大家可以自己在网上查找资料。
下面是环境配置指南，请阅读自己的系统的那一小节。

```
                  你的编译器                gcc            qemu/spike
MiniDecaf 源文件 ------------> RISC-V 汇编 -----> 可执行文件 --------> 输出
```

### Windows 用户环境配置指南
下面描述了 WSL 的一种参考方法。
你还可以开一个 Linux 虚拟机，使用 Virtualbox 或 VMWare 等，然后参考下面 Linux 配置。

Win10 设置
1. 参考 https://blog.csdn.net/daybreak222/article/details/87968078 ，设置“开发者模式”以及“启用子系统功能”。

2. 打开Microsoft Store，搜索Ubuntu，选择ubuntu20.04.

3. 按照下面的 Linux 用户环境配置指南安装 riscv 工具链。

### Ubuntu 用户环境配置指南

1. 建议使用 Ubuntu 20.04 及更高的版本，你可以直接使用 apt 来安装用户态的 qemu，即 `apt install qemu-user`。

对于低版本的 Ubuntu，你需要自己编译出可用的用户态 QEMU。
```bash
git clone https://git.qemu.org/git/qemu.git # 这里可能下载速度过慢，需要科学上网
cd qemu && ./configure --target-list=riscv32-linux-user
make
make install
qemu-riscv32 --version # 检查是否安装成功
```

2. 从[这里](https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.08/riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14.tar.gz)下载预编译好的 RISC-V 工具链并解压。

3. 安装工具链 `cp riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14/* /usr/ -r`

> 在第 2. 步，你可以选择不安装到系统目录下。相应的，你需要设置环境变量：
> `export PATH=$PATH:/path/to/riscv-prebuilt/bin`，把 `/path/to` 替换为你的解压目录。
> 把上面这条命令加到你的 `~/.bashrc` 文件中，这样不用每次打开终端都要重新设置。
> 每次改完 `~/.bashrc` 你都需要重启终端，以便改动生效。
> （如果你不用系统自带的 bash 而是用 zsh 之类的 shell，那加到 `~/.zshrc` 等 shell 配置文件里）

### macOS 用户环境配置指南

1. 从[这里](https://static.dev.sifive.com/dev-tools/riscv64-unknown-elf-gcc-8.3.0-2020.04.0-x86_64-apple-darwin.tar.gz)下载预编译好的 RISC-V 工具链并解压到你喜欢的目录。
2. 由于 macOS 不支持 QEMU 的用户态模式，我们使用 [Spike](https://github.com/riscv/riscv-isa-sim) 模拟器和一个简易内核 [riscv-pk](https://github.com/riscv/riscv-pk) 提供用户态程序的运行环境。你可以选择下面两种安装方法中的任意一种：

  1. 从[这里](https://cloud.tsinghua.edu.cn/f/6246e90c407b4a508816/)下载我们预编译的二进制程序包 spike-pk-prebuilt-x86_64-apple-darwin.tar.gz，不过还需要通过 [Homebrew](https://brew.sh/) 安装依赖 device tree compiler：

    ```bash
    $ brew install dtc
    ```

  2. 通过 [Homebrew](https://brew.sh/) 安装 Spike（会自动安装 dtc）：

    ```bash
    $ brew tap riscv/riscv
    $ brew install riscv-isa-sim
    ```

    然后从[这里](https://cloud.tsinghua.edu.cn/f/6246e90c407b4a508816/)上下载我们预编译的二进制程序包 spike-pk-prebuilt-x86_64-apple-darwin.tar.gz，只用里面的 `pk`。

    > Homebrew 也提供了 riscv-pk，不过那是 64 位的，而我们需要 32 位的，请使用我们预编译的 riscv-pk 或自行编译。

3. （可选）设置环境变量，方法与 Linux 一样，见上一节。如果不设置每次使用 gcc 和 spike 时都要输入完整路径。不过对于 `pk` 设置环境变量不管用，要么把它放到系统目录 `/usr/local/bin/pk`，要么每次都用完整路径。
4. 测试你 GCC 和 Spike 是否成功安装，详见[RISC-V 的工具链使用](./riscv.md)。


## 必做：测试你是否正确配置好了环境
1. 创建 `test.c` 文件，其中写入如下内容
```c
#include <stdio.h>
int main() { printf("Hello world!\n"); }
```

2. 编译 `test.c` 文件，`gcc` 应该输出一个可执行文件 `a.out`。但 `a.out` 是 RISC-V 可执行文件，所以我们的 X86 计算机无法运行。
```bash
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O3 test.c
$ ls a.out
a.out
$ ./a.out
bash: ./a.out: cannot execute binary file: Exec format error
```

后面[RISC-V 的工具链使用](./riscv.md)总结了 gcc 和 qemu 在编译实验中可能需要的用法。

3. 使用 qemu 执行 `a.out`
```bash
# Linux用户
$ qemu-riscv32 a.out
Hello world!
# Mac OS用户，假设你已经将spike加入环境变量，将pk加入系统目录
$ spike --isa=RV32G pk a.out
bbl loader
Hello world!
```

# 备注
[^1]: 开头的 `$ ` 表示接下来是一条命令，记得运行的时候去掉 `$ `。例如，让你运行 `$ echo x`，那你最终敲到终端里的是 `echo x`（然后回车）。如果开头没有 `$ `，那么这一行是上一条命令的输出（除非我们特别说明，这一行是你要输入的内容）。
