# 常见问题

## Invalid ELF image for this architecture
```
$ qemu-riscv32 a.out
a.out: Invalid ELF image for this architecture
```

解决方法：

> 注意编译时 gcc 要用 `riscv64-unknown-elf-gcc`，并且加上 `-march=rv32im -mabi=ilp32`。

## command not found
```
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O3 -S input.c
riscv64-unknown-elf-gcc: command not found
```
或者运行 `qemu-riscv32` 时提示上面的错误。

解决方法：

> 你是否按照[环境配置](./env.md)中指南配好环境？如果你没有安装到系统目录，是否设置 PATH，并且把 `export PATH...` 命令放到 `~/.bashrc`？

## Spike pk 卡死

执行 `spike pk` 直接卡死，需要按多次 Ctrl-C 后才能退出。

解决方法：

> 可能是忘加了 `--isa=RV32G` 选项，在用 64 位的 Spike 跑 32 位 pk。
>
> 如果你加了该选项也有这个问题，可能是你安装了 64 位的 pk 然后在用 32 位的 Spike 跑，请使用我们预编译的 32 位 pk。

## Spike 运行报错：could not open pk

```
$ spike --isa=RV32G pk
libc++abi.dylib: terminating with uncaught exception of type std::runtime_error: could not open pk (did you misspell it? If VCS, did you forget +permissive/+permissive-off?)
```

解决方法：

> Spike 找不到 pk，请输入 pk 的完整路径。

## Spike 运行报错：assertion failed: IS_ELF32(eh)

```
$ spike --isa=RV32G pk a.out
bbl loader
../pk/elf.c:42: assertion failed: IS_ELF32(eh)
Power off
```

解决方法：

> 你可能编译出了 64 位的 `a.out`，注意编译时 gcc 要用 `riscv64-unknown-elf-gcc`，并且加上 `-march=rv32im -mabi=ilp32`。

## Spike 运行报错：Child dtb process failed

```
$ spike --isa=RV32G /usr/local/bin/pk a.out
Failed to run dtc: No such file or directory
Child dtb process failed
```

解决方法：

> 使用 Homebrew 安装 device tree compiler：
>
> ```
> $ brew install dtc
> ```

## macOS 下找不到 realpath 命令

macOS 下运行 minidecaf-tests 里的 check.sh 报错：

```
./check.sh: line 25: realpath: command not found
./check.sh: line 26: realpath: command not found
./check.sh: line 30: $asmfile: ambiguous redirect
......
```

解决方法：

> 使用 Homebrew 安装 coreutils：
>
> ```
> $ brew install coreutils
> ```
