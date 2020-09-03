# step5 实验指导

## 词法语法分析
如果你使用工具完成词法语法分析，修改你的语法规范以满足要求，自行修改词法规范，剩下的交给工具即可。

语义检查部分，我们需要检查是否（一）使用了未声明的变量、（二）重复声明变量。
为此，我们在生成 IR 的 Visitor 遍历 AST 时，维护当前已经声明了哪些变量。
遇到变量声明（`declaration`）和使用（`primary` 和 `assignment`）时检查即可。

如果你是手写分析，TODO

## IR 生成
为了完成 step5 的 IR 生成，我们需要确定 IR 的栈帧布局，请看 [这里](./stackframe.md)。

局部变量被放在栈上，但我们不能直接弹栈访问它们。
因此我们需要加入访问栈内部的 `load`/`store`，以及生成栈上地址的 `frameaddr` 指令。
并且我们再加入一个 `pop` 指令。

| 指令 | 参数 | 含义 | IR 栈大小变化 |
| --- | --- | --- | --- |
| `frameaddr` | 一个非负整数常数 `k` | 把当前栈帧底下开始第 `k` 个元素的地址压入栈中 | 增加 1 |
| `load` | 无参数 | 将栈顶弹出，作为地址 [^1] 然后加载该地址的元素（`int`），把加载到的值压入栈中 | 不变 |
| `store` | 无参数 | 弹出栈顶作为地址，读取新栈顶作为值，将值写入地址开始的 `int` | 减少 1 |
| `pop` | 无参数 | 弹出栈顶，忽略得到的值 | 减少 1 |

IR 生成还是 Visitor 遍历，并且
* 遇到读取变量 `primary: Identifier` 的时候，查符号表确定变量是第几个，然后生成 `frameaddr` 和 `load`。
* 遇到变量赋值的时候，先生成等号右手边的 IR，同上对等号左手边查符号表，生成 `frameaddr` 和 `store`。
> 注意赋值表达式是有值的，执行完它的 IR 后栈顶还保留着赋值表达式的值。这就是为什么 `store` 只弹栈一次。
* 遇到表达式语句时，生成完表达式的 IR 以后记得再生成一个 `pop`，保证栈帧要满足的第 1. 条性质（[这里](./stackframe.md)有说）
* 遇到声明时，除了记录新变量，还要初始化变量。
> 为了计算 prologue 中分配栈帧的大小，IR 除了一个指令列表，还要包含一个信息：局部变量的个数。
* `main` 有多条语句了，所以它的 IR 是其中语句的 IR 顺序拼接。

> 例如 `int main(){int a=2; a=a+3; return a;}`，显然 `a` 是第 0 个变量。
> 那它的 IR 指令序列是（每行对应一条语句）：
```
frameaddr 0 ; push 2 ; store ; pop ;
frameaddr 0 ; load ; push 3 ; add ; frameaddr 0 ; store ; pop ;
frameaddr 0 ; load ; ret ;
```

## 汇编生成
IR 指令到汇编的对应仍然很简单，如下表。

| IR       | 汇编                                                |
| ---      | ---                                                 |
| `frameaddr k` | `addi sp, sp, -4  ;  addi t1, fp, -12-4*k  ;  sw t1, 0(sp)` |
| `load`    | `lw t1, 0(sp)  ;  lw t1, 0(t1)  ;  sw t1, 0(sp)` |
| `store` | `lw t1, 4(sp)  ;  lw t2, 0(sp)  ;  addi sp, sp, 4  ;  sw t1, 0(t2)` |
| `pop` | `addi sp, sp, 4` |

但除了把 IR 一条一条替换成汇编，step5 还需要生成 prologue 和 epilogue，并且 `ret` 也要修改了，
参见[栈帧文档](./stackframe.md)。

| IR       | 汇编                                                |
| ---      | ---                                                 |
| `ret` | `lw a0, 0(sp)  ;  addi sp, sp, 4  ;  j FUNCNAME_epilogue` |

# 备注
[^1]: 我们规定 `load` 的地址必须对齐到 4 字节，生成 IR 时需要保证。`store` 也是。
