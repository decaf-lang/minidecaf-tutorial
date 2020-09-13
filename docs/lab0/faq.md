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

## 安装 ANTLR 提示 Permission denied
```
$ wget https://www.antlr.org/download/antlr-4.8-complete.jar
--2020-09-13 16:33:34--  https://www.antlr.org/download/antlr-4.8-complete.jar
Resolving www.antlr.org (www.antlr.org)... 185.199.111.153, 185.199.109.153, 185.199.108.153, ...
Connecting to www.antlr.org (www.antlr.org)|185.199.111.153|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2089101 (2.0M) [application/java-archive]
antlr-4.8-complete.jar: Permission denied

Cannot write to ‘antlr-4.8-complete.jar’ (Success).
```

运行 `sudo wget https://www.antlr.org/download/antlr-4.8-complete.jar`。
