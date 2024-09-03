# RISC-V相关内容补充

## RISC-V官方资料

不建议阅读，太过冗长，这对于编译知识提升非常有限。

[RISC-V 官方](https://riscv.org/technical/specifications/)
请下载ISA Specifications (Ratified)中的Volume 1, Unprivileged Specification。

如果你时间充足，你可以阅读：

Chapter 24 RV32/64G Instruction Set Listings

Chapter 25 RISC-V Assembly Programmer’s Handbook

## 如何快速查询RISC-V指令

### 在线编译器

你可以使用[Compiler Explorer (godbolt.org)](https://godbolt.org/)来快速获得一个riscv指令的实现

在左边输入以下例子

```c++
int mod(int x, int y) {
    // 注意：此处不要直接写一个可以计算得到结果的式子
    // 比如5 % 8会被编译器优化为5
    return x % y;
}
```

把右边的编译器选为RISC-V(32-bits)中的任何一个，在编译选项中写上-O2（减少不必要的指令生成），翻译一条指令看看效果。


### 本地编译器

你可以通过 gcc 编译如下程序来了解如何翻译逻辑非运算符到 RISC-V 汇编 riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 foo.c -S -O3 -o foo.s（**记得加 -O3 或者 -O2 选项**）：
```c++
int foo(int x) {
    return !x;
}
```

不出意外你会获得如下结果：
```
foo:
    seqz    a0,a0
    ret
```