## ☑任务：

更新汇编代码生成过程，以正确处理函数定义与调用。并通过 step[1-9] 的测试用例。

## ☑任务（可选）：

利用 `riscv64-unknown-elf-gcc`，通过对一些小例子生成汇编代码，了解 GCC 的调用约定，包括函数序言、函数尾声、函数调用部分，并改进你的 minidecaf 编译器，使其符合 GCC 的调用约定，并让 minidecaf 程序能够正确调用由 GCC 编译的函数。

下面是一个测试程序，使用你的编译器编译并运行后，应该能正确输出 `Hello, World!`。

```c
int putchar(int c);

int main() {
    putchar(72);
    putchar(101);
    putchar(108);
    putchar(108);
    putchar(111);
    putchar(44);
    putchar(32);
    putchar(87);
    putchar(111);
    putchar(114);
    putchar(108);
    putchar(100);
    putchar(33);
    putchar(10);
}
```

> 提示：使用 a0-a7 寄存器传递前 8 个参数，超过 8 个的部分再使用栈传递，并注意传参寄存器的保存。
