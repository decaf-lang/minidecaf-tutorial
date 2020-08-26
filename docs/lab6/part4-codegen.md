## 代码生成

### 基础

不妨先看看跳转语句的 c 汇编代码：

```c
int main() {
    int a = 0;
    if(a) {
        a = 2;
    } else {
        a = 3;
    }
    return a;
}
```

```
	.globl	main
main:
	addi	sp,sp,-32
	sd	s0,24(sp)               #这里的 s0 是 fp 的别称
	addi	s0,sp,32            #函数前序，由于只有一个函数，未保存 ra
	sw	zero,-20(s0)            #变量初始化 
	lw	a5,-20(s0)
	sext.w	a5,a5               #这两句计算了 if 条件
	beqz	a5,.L2
	li	a5,2                    #then 分支
	sw	a5,-20(s0)
	j	.L3
.L2:                            #els分支
	li	a5,3
	sw	a5,-20(s0)
.L3:
	lw	a5,-20(s0)
	mv	a0,a5                   #返回变量 a 的值
	ld	s0,24(sp)
	addi	sp,sp,32
	jr	ra                      #函数收尾
```
#### 跳转语句

跳转语句是分支的基础，跳转分无条件跳转和条件跳转

```asm
j label                 #jump;无条件跳转到label, pc <- label
beqz t0, label          #branch equal to zero; pc = (t0 == 0)? label : pc + 1;
```

#### 标识

标识(label)可以方便我们进行跳转，为了保证跳转的正确我们需要合适的方式生成 label。最简单的，我们可以用一个累加的数字来区分 label(比如上面的汇编例子)，但好的 label 生成方便我们后续实现 break, continue 等指令。目前，我们可以用一个累增数字和一个后缀(`.then`、`.else`、`.exit`)来生成标识。

### 生成

为了生成 IF 语句和条件表达式的汇编代码，我们将需要有条件和无条件的跳转，以条件表达式为例。遵循递归的思路，我们可以这样 IF 语句:

```
生成IF语句：
    计算条件;
    生成跳转语句; 
    生成标识(then);
    生成then分支代码;
    生成标识(els);
    生成els分支代码;
```

条件表达式与之类似，以下给出条件表达式伪代码。

```
visitTern(IR tern) {
    visit(tern.cond);
    #Label then = new Label("then");            #在这里，then分支是用不到的，可以删掉，但在后续的循环中会用到
    Label els = new Label("els");               #得到一个新的 else label
    Label exit = new Label("exit");             #得到一个新的 exit label
    emitBeqz(els);                              #消耗 tern.cond 的结果，如为 false 则跳转到 els 分支
    then.emit();                                #emit then label, 接下来的代码会 push then 分支的结果并跳转到 exit
    emitJ(exit);                                #then分支结束后，直接跳转到 exit label
    els.emit();                                 #emit els label, 接下来的代码会 push els 分支的结果并跳转到 exit
    visit(tern.els);
    exit.emit();
}
```

IF 语句与条件表达式很类似，请同学们自行完成。
