## 汇编代码生成

### 基础

首先介绍本阶段需要用到的汇编指令。

取负（`-`）和按位非（`~`）是超级简单的，每一个都可以用一条汇编指令来完成。

`neg`取负操作数的值。下面是一个例子。

```
    neg rd, rs          #rd = -rs
```

`not`用它的按位取反来替换一个值。我们可以用和`neg`完全一样的方式来使用它。

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

取反操作伪代码如下：

```
void visitNeg(IR neg) {
    visit(neg.operator);        #先计算操作数的值（也就是生成计算操作数的代码）
    emitNeg();
}
```

在当前阶段，我们总是只涉及一个操作数，因此可以可以固定一个寄存器来储存每一步的计算结果。

emitNeg() 可以生成这样的代码 (固定将结果储存在 t0 寄存器中)：

```asm
neg t0, t0          #执行取反计算，结果储存在 t0 中
```

但是这样的设计可拓展性很差，在碰到多个操作数的时候会变得复杂（在lab3我们就会碰到这样的例子）。

/\*介绍栈式机？\*/

在栈式机上，每一个操作总是在栈上取出操作数，计算结束后将结果储存回栈中，这样我们所用的寄存器的数量会很少。

```
void visitNeg(IR neg) {
    visit(neg.operator);        #先计算操作数的值，计算完成后，结果应该在栈顶
    emitNeg();              #取出栈顶操作数，执行计算，将结果储存回栈
}
```

emitNeg() 可以生成这样的代码：

```asm
ld t0, 0(sp) 
add sp, sp, 8       #前两条语句将操作数取出，并置于 t0 寄存器中，类似与 pop
neg t0, t0          #执行取反计算，结果储存在 t0 中
sd t0, -8(sp) 
add sp, sp, -8      #这两条语句完成计算结果的压栈储存，类似于 push
```

不难发现对 sp 的移动是多余的，可以简化如下：

```asm
ld t0, 0(sp) 
neg t0, t0
sd t0, 0(sp) 
```

其他两个操作与 neg 几乎完全一致，最后我们可以得到如下代码：

```
void visitUnary(IR unary) {
    visit(unary.operator);
    switch(unary.op) {
        case NEG:           // '-'
            emitNeg();
            return;         // '~'
        case BITNOT:
            emitBitNot();
            return;
        case NOT:           // '!'
            emitLogNot();
            return;
    }
}
```

