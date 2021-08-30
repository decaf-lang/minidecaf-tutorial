# RISC-V 的工具链使用

RISC-V 是一个很像 MIPS 的 RISC 指令集架构，编译实验要求你的编译器把 MiniDecaf 程序编译到 RISC-V 汇编。

指令集文档在[这里](https://riscv.org/technical/specifications/)，我们只需要其中的 "Unprivileged Spec"。

> 另外[这里](https://github.com/TheThirdOne/rars/wiki/Supported-Instructions)也有（非官方的）指令用法说明。 不过事实上，很多时候看 gcc 输出的汇编比看什么文档都有用。

## RISC-V 工具使用

我们提供预先编译好的 RISC-V 工具，在[环境配置](env.md)中已经叙述了安装和使用方法。 下面汇总一下。

> 注意，我们虽然是用的工具前缀是 `riscv64`， 但我们加上参数 `-march=rv32im -mabi=ilp32` 以后就能编译到 32 位汇编 。 使用时记得加这个参数，否则默认编译到 64 位汇编。

我们假设你已经正确设置好了环境变量，否则运行 `riscv64-unknown-elf-gcc` 或 `qemu-riscv32` 或 `spike` 时请用完整路径。

* gcc 编译 `input.c` 到汇编 `input.s`，最高优化等级（否则输出的汇编会很冗长）

```bash
# input.c 的内容
$ cat input.c
int main(){return 233;}

# 编译到 input.s
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O3 -S input.c

# gcc 的编译结果
$ cat input.s
    .file    "input.c"
    .option nopic
    .attribute arch, "rv32i2p0_m2p0"
    .attribute unaligned_access, 0
    .attribute stack_align, 16
    .text
    .section    .text.startup,"ax",@progbits
    .align    2
    .globl    main
    .type    main, @function
main:
    li    a0,233
    ret
    .size    main, .-main
    .ident    "GCC: (SiFive GCC 8.3.0-2020.04.0) 8.3.0"
```

* gcc 编译 `input.s` 到可执行文件 `a.out`

```bash
# input.s 的内容，就是上面汇编输出的简化版本
$ cat input.s
    .text
    .globl    main
main:
    li    a0,233
    ret

# 编译到 a.out
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 input.s

# 输出结果，能看到是 32 位的 RISC-V 可执行文件
$ file a.out
a.out: ELF 32-bit LSB executable, UCB RISC-V, version 1 (SYSV), statically linked, not stripped
```

* 【Linux 用户】qemu 运行 `a.out`，获取返回码

```bash
# 运行 a.out
$ qemu-riscv32 a.out

# $? 是 qemu 的返回码，也就是我们 main 所 return 的那个值
$ echo $?
233
```

* 【macOS 用户】Spike 模拟器运行 `a.out`，获取返回码

```bash
# 运行 a.out
# /usr/local/bin/pk 替换为你自己的 pk 路径
$ spike --isa=RV32G /usr/local/bin/pk a.out
bbl loader

# $? 是 spike 的返回码，也就是我们 main 所 return 的那个值
$ echo $?
233
```

