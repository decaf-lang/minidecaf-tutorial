## 汇编代码生成

### 基础

首先介绍本阶段需要用到的汇编指令。

取负（`-`）和按位非（`~`）是超级简单的，都可以用一条汇编指令来完成。

`neg`将操作数取负的值。下面是一个例子。

```
    neg rd, rs          #rd = -rs
```

`not`将操作数按位取反。我们可以用和`neg`完全一样的方式来使用它。

```
    not rd, rs          #rd = ~rs
```

逻辑非（`!`）是比较复杂的。记住，`return !exp`相当于：

```
if (exp == 0) {
    return 1;
} else {
    return 0;
}
```

但在 riscv 下有一个非常方便的指令，我们可以使用`seqz`(set equal to zero)来实现它。

```
    seqz rd, rs         #rd = (rs == 0) ? 1 : 0;
```

### 生成

对于类似 `!!~-3` 这样一连串的操作，我们总是要先得到操作数，然后才能进行操作，这个式子的计算次序为：取负，按位取反,逻辑取反，逻辑取反。在代码实现上，这是一个递归的过程。

实现取反操作伪代码如下：

```
void visitNeg(Node neg) {
    visit(neg.operator);        #先计算操作数的值，计算完成后，结果应该在栈顶
    emitNeg();                  #取出栈顶操作数，执行计算，将结果储存回栈
}
```

emitNeg() 可以生成这样的代码：

```asm
lw t0, 0(sp) 
add sp, sp, 4       #前两条语句将操作数取出，并置于 t0 寄存器中，类似与 pop
neg t0, t0          #执行取反计算，结果储存在 t0 中
sw t0, -4(sp) 
add sp, sp, -4      #这两条语句完成计算结果的压栈储存，类似于 push
```

不难发现对 sp 的移动是多余的，可以简化如下：

```asm
lw t0, 0(sp) 
neg t0, t0
sw t0, 0(sp) 
```

其他两个操作与 neg 几乎完全一致，最后我们可以得到如下代码：

```
void visitUnary(Node unary) {
    visit(unary.operator);
    switch(unary.op) {
        case NEG:           // '-'
            emitNeg();
            return;         
        case BITNOT:
            emitBitNot();
            return;
        case NOT:           // '!'
            emitLogNot();
            return;
    }
}
```

