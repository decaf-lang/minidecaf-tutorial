# step10 实验指导

## 词法语法分析
如果你使用工具完成词法语法分析，修改你的语法规范以满足要求，自行修改词法规范，剩下的交给工具即可。

如果你是手写分析，参见[这里](./manual-parser.md)。

## 名称解析
和局部变量一样，全局变量要放进符号表里，名称解析才能解析到它们。
和 step7 一样，符号表是一个栈，其中每个元素对应一个作用域。
全局变量就放在栈底，它们位于全局作用域；名称分析遍历 AST 过程中，栈底元素一直都在，不会被弹出。

全局变量相关的语义检查有：
1. 初始值只能是整数字面量。
    > 有以下几种可行的实现方法：
		>
		> 1. 直接取得初始值对应源代码的字符串，按整数解析（`int(text)` 或 `Integer.parse(text)`）即可。
    > 2. 修改语法，全局变量是一个新的 `global_declaration : type Identifier ('=' Integer)? ';'`。
		> 3. 判断这个expr节点的具体类型，要求它必须是整数常量，并且获取常量值。各种语言中都有相应的机制，只是语法不太一样。
2. 不能重复声明：step7 已经要求同一作用域中不能重复声明变量了。

## IR 生成
局部变量需要通过 `frameaddr` 访问，但全局变量不行，所以我们引入新的 IR 指令用于加载全局变量的地址

| 指令 | 参数 | 含义 | IR 栈大小变化 |
| --- | --- | --- | --- |
| `globaladdr` | 一个字符串，表示符号名 | 取得符号名对应的全局变量的地址，压入栈中 | 增加 1 |

> 例如 `int a=2; int main(){return a;}` 中 `main` 的 IR 是
> `globaladdr a  ;  load  ;  ret`。

并且现在，一个 MiniDecaf 程序的 IR 除了一系列 **IR 函数**，还要包含一系列 **IR 全局变量** 了，每个需要记录的信息类似：
1. 大小有多少字节
2. 是否有初始值，初始值是多少

## 汇编生成
汇编可以直接用 `la` 加载全局变量地址

| IR       | 汇编                                                |
| ---      | ---                                                 |
| `globaladdr SYMBOL` | `addi sp, sp, -4  ;  la t1, SYMBOL  ;  sw t1, 0(sp)` |

每个全局变量还对应一段汇编，不过这段汇编基本就是一个模板替换，我们直接给出结果。

例如 `int compiler = 2020;` 放到 .data，其汇编如下，`compiler` 和 `2020` 可替换成其他变量名和初始值：
```
	.data
	.globl compiler
	.align 4
	.size compiler, 4
compiler:
	.word 2020
```
> 汇编命令（assembler directive）的标准文档在 [这里](https://sourceware.org/binutils/docs-2.32/as/Pseudo-Ops.html#Pseudo-Ops)。
> 不用深入学习汇编命令，它们不是课程内容。
>
> 简要解释一下：`.data` 表示输出到 `data` 段；`.globl a` 定义一个全局符号；`.word` 后是一个四字节整数，是 `a` 符号所在内存的初始值。

而 `int tsinghua;` 放到 .bss 的汇编如下，第一个 4 表示大小，第二个 4 表示对齐要求
```
	.comm	tsinghua,4,4
```

# 思考题
1. 写出 `la v0, a` 这一 RiscV 伪指令可能会被转换成哪些 RiscV 指令的组合（说出两种可能即可）。

参考的 RiscV 指令链接：https://github.com/TheThirdOne/rars/wiki/Supported-Instructions

# 总结
我们实验中，全局变量相对简单。
但其实全局变量可以展开讲到 linker 和 loader，可惜我们课容量有限不能讨论。
