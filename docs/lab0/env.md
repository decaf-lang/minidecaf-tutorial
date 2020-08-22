# 环境配置

## 必做：RISC-V 的 gcc 和 qemu
我们的编译器只生成 RISC-V 汇编，但是提供预编译的 gcc 和 qemu 模拟器。
gcc 用来把 C 编译到汇编、以及把汇编变成 RISC-V 可执行文件；qemu 用来运行 RISC-V 可执行文件。
不过我们提供的 gcc 和 qemu 只能在 Linux/Mac 下运行，**Windows 的同学** 可以使用 WSL，或者运行一个虚拟机。
关于 WSL / 虚拟机使用，以及 Linux 基础操作，大家可以自己在网上查找资料。

```
                  你的编译器                gcc               qemu
MiniDecaf 源文件 ------------> RISC-V 汇编 -----> 可执行文件 --------> 输出
```

这一步的环境配置指南
1. (Windows 同学）配置好 WSL / 虚拟机

2. 从网络学堂下载 riscv-prebuilt.tar.gz 压缩包并解压（命令是 `tar xzf riscv-prebuilt.tar.gz`）

3. 安装工具链 `cp riscv-prebuilt/* /usr/ -r`

> 在第 3. 步，你可以选择不安装到系统目录下。相应的，你需要设置环境变量：
> `export PATH=$PATH:/path/to/riscv-prebuilt/bin`，把 `/path/to` 替换为你的解压目录

执行下面命令测试你 gcc 和 qemu 是否成功安装 [^1]
1. 创建 `test.c` 文件，其中写入如下内容
```c
#include <stdio.h>
int main() { printf("Hello world!\n"); }
```

2. 编译 `test.c` 文件，`gcc` 应该输出一个可执行文件 `a.out`。但 `a.out` 是 RISC-V 可执行文件，所以我们的 X86 计算机无法运行。
```bash
$ riscv64-unknown-elf-gcc test.c
$ ls a.out
a.out
$ ./a.out
bash: ./a.out: cannot execute binary file: Exec format error
```

3. 使用 qemu 执行 `a.out`
```bash
$ qemu-riscv64 a.out
Hello world!
```


## 推荐：参考实现的环境
我们强烈推荐你选择一个参考实现，并且先测试运行（见下一节）一下，为此你需要配置参考实现的环境。
现在已有如下的参考实现，请根据自己的喜好选择一个，`git clone` 到本地，然后按照它的 README 配置好它的环境。

### Python-ANTLR
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-dzy
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-dzy`

### Rust-lalr1
* 地址 https://github.com/decaf-lang/minidecaf/tree/mashplant
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b mashplant`

### Rust-manual
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-cy
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-cy`

### Java-ANTLR
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-xxy
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-xxy`

### C++-ANTLR
有两个，第一个：
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-tsz
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-tsz`

第二个：
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-zj
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-zj`

### C++-manual
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-zyr
* clone 命令：`git clone git@github.com:decaf-lang/minidecaf.git -b md-zyr`


# 备注
[^1]: 开头的 `$ ` 表示接下来是一条命令，记得运行的时候去掉 `$ `。例如，让你运行 `$ echo x`，那你最终敲到终端里的是 `echo x`（然后回车）。如果开头没有 `$ `，那么这一行是上一条命令的输出（除非我们特别说明，这一行是你要输入的内容）。
