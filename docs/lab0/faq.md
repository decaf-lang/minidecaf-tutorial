# 常见问题

## Invalid ELF image for this architecture
```
$ qemu-riscv32 a.out
a.out: Invalid ELF image for this architecture
```

注意编译时 gcc 要用 `riscv64-unknown-elf-gcc`、并且加上 `-march=rv32im -mabi=ilp32`。

## command not found
```
$ riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O3 -S input.c
riscv64-unknown-elf-gcc: command not found
```
或者运行 `qemu-riscv32` 时提示上面的错误。

你是否按照[环境配置](./env.md)中指南配好环境？
如果你没有安装到系统目录，是否设置 PATH，并且把 `export PATH...` 命令放到 `~/.bashrc`？
