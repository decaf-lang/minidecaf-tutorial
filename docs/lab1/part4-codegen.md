## 汇编代码生成

我们选择的目标平台是RISC-V 32，我们可以先看看常见的编译器生成的汇编代码是什么样的：

```bash
$ riscv32-linux-gnu-gcc return2.c -S -O3
$ cat return2.s
    .file   "return2.c"
    .option nopic
    .text
    .section        .text.startup,"ax",@progbits
    .align  1
    .globl  main
    .type   main, @function
main:
    li      a0,2
    ret
    .size   main, .-main
    .ident  "GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
```

其实这里有很多多余的信息，你可以自己尝试一下，只留下最关键的一些表示main函数的信息就可以经由汇编器和链接器生成正确的程序：

```nasm
    .globl  main
main:
    li      a0,2
    ret
```

这里做的事情倒是很直接，就是直接return一个常数了，不过跟我们上面描述的两条指令做到事情还是不太一样。为了能够模拟我们描述的PUSH和RET的操作，还是有必要了解一下RISC-V指令集和相关的调用约定的知识，不过为了减小大家的工作量，这个阶段我们不要求你们去自行查阅，而是把必要的知识都列出来：

1. 我们假定整数都是32位的，因此运算栈中的一个元素占据4字节
2. 我们可以用sp寄存器来表示栈，sp的值就是栈顶，但是这个栈是向地址低的地方生长的，所以如果sp的值减少4，就意味着栈增长了一个元素
3. 我们可以用t开头的寄存器来进行一些临时的数据存储和运算
4. 最终函数的返回值需要保存到a0寄存器中

### 基础指令

li指令用来加载一个常数到寄存器中
```asm
li t0, 3            #t0 = 3
```
sw指令用来把一个寄存器中的值保存到一个内存地址
```asm
sw t0, 4(sp)        #地址 sp+4 对应的内存 = t0, 长度为 4 字节
```
lw指令用来把一个内存地址中的值读入到一个寄存器
```asm
lw t0, 4(sp)        #t0 = 地址 sp+4 对应的内存, 长度为 4 字节
```
ret用来执行函数返回
```asm
ret                 #pc <- ra
```

### 代码生成

代码生成部分的工作是：输入一个 AST，输出汇编代码。我们主要通过遍历 AST 来完成汇编生成，在此过程中，我们可以定义一些 IR 来是的代码生成更加清晰，方便理解。当然你也可以直接生成汇编。因此接下来我们要做的是：AST (--> IR) --> asmmebly。

目前的 AST 中，需要处理的只有 return 语句和数字常量。函数结构的其他部分你可以使用 hard code 去生成，后续涉及到函数等更加复杂的结构我们回去修改。

硬编码模板：
```
    .globl
<函数名>:
```

#### 代码框架

我们通过遍历 AST 来进行 IR 生成或者直接生成汇编代码，接下来的伪代码中 `visit(Node node)` 代表递归进行该 AST 节点的代码生成，可以使用类似如下的框架进行 AST 遍历。

```
visit(Node node) {
    switch(node.node_type) {
        case RETURN:
            visitRet(node);
            break;
        ....
    }
}
```
或者如果你使用的语言有继承系统：
```
visit(RET_STMT ret) {
    visitRet(ret);
}
```
遍历 AST 只需 `visit(root)`

#### 递归解析

对 AST 的解析是一个递归的过程，以 return 语句为例，我们需要先生成计算汇编返回值的代码，然后再生成 `ret`。就像这样:

```
visitRet(Node ret_stmt) {
    visit(ret_stmt.expr);            //先计算返回值的值（也就是生成计算操作数的代码）          
    emitReturn();                    //生成返回语句汇编代码 
}

visitConst(Node const) {
    emitConst(const.val);            //生成产生一个常量的汇编代码
}
```

在当前阶段，我们总是只涉及一个操作数，因此可以可以固定一个寄存器来储存每一步的计算结果。

emitConst(int val) 可以生成这样的代码 (固定将结果储存在 t0 寄存器中)：

```asm
li t0, {val}          #t0 = val
```

但是这样的设计可拓展性很差，在碰到多个操作数的时候会变得复杂（在lab3我们就会碰到这样的例子）。在栈式机上，每一个操作总是在栈上取出操作数，计算结束后将结果储存回栈中，这样我们所用的寄存器的数量会很少。

emitConst(int val) 在栈式机上，应该生成这样的代码：

```
PUSHI(val);
```
这是一个IR，其中，PUSHI(val) 代表将一个常量压栈，对应汇编：

```asm
li t0, {val}
addi sp, sp, -4
sw t0, 0(sp)
```
emitReturn() 的作用是：取出栈顶的值（必须保证此时栈顶的值就是想 return 的），返回它。对应 IR：

```asm
RETURN
```

对应汇编：

```asm
lw a0, 0(sp)    # 从栈顶读出值到表示返回值的寄存器
add sp, sp, 4   # 栈减小一个元素，这一条和上面一条合起来就是弹出一个元素，并把值赋给a0
ret             # 函数返回
```

最终你为`return2.c`生成的整个汇编程序可以是这个样子的：

```asm
    .globl  main
main:
    li t0, 2
    sw t0, -4(sp)
    add sp, sp, -4
    lw a0, 0(sp)
    add sp, sp, 4
    ret
```

注意，该汇编代码显然是可以优化的，但是不在实验要求之内。