#### ☑任务：

写一个*generate*函数，接受一个AST并生成汇编。它可以以字符串的形式在屏幕上显示汇编代码，也可以直接把汇编代码写到文件中。它应该为所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)生成正确的汇编码。


#### ☑ 任务：写一个*pretty-print* funcion，它接收一个AST并以可读的方式打印出来。

写一个*pretty-print*的函数，接受一个AST并以可读的方式打印出来。

####  (可选) 漂亮的打印

你可能需要一个实用函数来打印出你的AST，以帮助调试。你可以现在就写，或者等到你需要的时候再写。下面是对return_2.c的AST输出例子：

```
FUN INT main:
    params: ()
    body:
        RETURN Int<2>
```

这个例子包含了一些AST不需要的信息，比如返回类型和函数参数列表。


#### ☑任务：

编写一个接受C源文件并输出可执行文件的程序（可以是一个包含调用你写的编译器和GCC的shell脚本）。该程序应该

1. 读取minidecaf源文件

2. 进行词法分析

3. 进行语法解析

4. 生成汇编码

5. 把汇编码写入到一个文件

6. 调用GCC命令，将生成的汇编码转换为可执行文件。在下面命令中，"assembly.s "是汇编文件的名称，"out "是你想生成的可执行文件的名称。

```
   riscv64-unknown-elf-gcc assembly.s -o out
```

7. (可选) 删除汇编文件。