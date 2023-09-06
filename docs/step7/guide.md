# step6 实验指导

## 词法语法分析
如果你使用工具完成词法语法分析，修改你的语法规范以满足要求，自行修改词法规范，剩下的交给工具即可。

语义检查无需修改。

如果你是手写分析，参见[这里](./manual-parser.md)。

注意 step6 引入 `block_item` 后，`declaration` 不再是语句，所以 `if (a) int b;` 不是的合法代码。
这和 C 标准是一致的（不过在C++中这样的代码是合法的，也许这更加符合你的常识）。

## 悬吊 else 问题
这一节引入的 if 语句既可以带 else 子句也可以不带，但这会导致语法二义性：`else` 到底和哪一个 `if` 结合？
例如 `if(a) if(b) c=0; else d=0;`，到底是 `if(a) {if(b) c=0; else d=0;}` 还是  `if(a) {if(b) c=0;} else d=0;`（其中有大括号，step7中会支持，不过意思不难理解）？
这个问题被称为 **悬吊 else（dangling else）** 问题。

如果程序员没有加大括号，那么我们需要通过一个规定来解决歧义。
我们人为规定：`else` 和最近的 `if` 结合，也就是说上面两种理解中只有前者合法。
为了让 parser 能遵守这个规定，一种方法是设置产生式的优先级，优先选择没有 else 的 if。
按照这个规定，parser 看到 `if(a) if(b) c=0; else d=0;` 中第一个 if 时，选择没有 else 的 if；
而看到第二个时只能选择有 else 的 if [^1]，也就使得 `else d=0;` 被绑定到 `if(b)` 而不是 `if(a)` 了。

## IR 生成
显然，我们需要跳转指令以实现 if，同时还需要作为跳转目的地的标号（label）。
我们的跳转指令和汇编中的类似，不限制跳转方向，往前往后都允许。

| 指令 | 参数 | 含义 | IR 栈大小变化 |
| --- | --- | --- | --- |
| `label` | 一个字符串 | 什么也不做，仅标记一个跳转目的地，用参数字符串标识 | 不变 |
| `beqz` | 同上 | 弹出栈顶元素，如果它等于零，那么跳转到参数标识的 `label` 开始执行 | 减少 1 |
| `bnez` | 同上 | 弹出栈顶元素，如果它不等于零，那么跳转到参数标识的 `label` 开始执行 | 减少 1 |
| `br` | 同上 | 无条件跳转到参数标识的 `label` 开始执行 | 不变 |

注意一个程序中的标号，也就是 `label` 的参数，必须唯一，否则跳转目的地就不唯一了。
简单地维护一个计数器即可，例如 `label l1`, `label l2`, `label l3` ...

Visitor 遍历 AST 遇到一个有 else 的 if 语句，为了生成其 IR，要生成的是
1. 首先是 `条件表达式的 IR`：计算条件表达式。
2. `beqz ELSE_LABEL`：判断条件，若条件不成立则执行 else 子句
3. 跳转没有执行，说明条件成立，所以之后是 `then 子句的 IR`
4. `br END_LABEL`：条件成立，执行完 then 以后就结束了
5. `label ELSE_LABEL`，然后是 `else 子句的 IR`
6. `label END_LABEL`：if 语句结束。

> 例子：`if (a) return 2; else a=2+3;` 的 IR 是
> 1. `frameaddr k ; load`，其中 `k` 是 `a` 的 frameaddr
> 2. `beqz else_label1`，数字后缀是避免标号重复的
> 3. `push 2 ; ret`
> 4. `br end_label1`
> 5. `label else_label1`，然后是 `push 2 ; push 3 ; add ; frameaddr k ; store ; pop`
> 6. `label end_label1`

仿照上面，容易写出条件表达式的 IR 应该如何生成，并且同时也能保证满足语义规范
> **6.4** 和 3.2 不同，条件表达式规定了子表达式的求值顺序。
>     首先对条件求值。如果条件值为真，然后仅对 `?` 和 `:` 之间的子表达式求值，作为条件表达式的值，
>     不得对 `:` 之后的子表达式求值。
>     如果条件为假，类似地，仅对 `:` 之后的子表达式求值。

类似，无 else 的 if 语句的 IR 包含
1. `条件表达式的 IR`
2. `beqz END_LABEL`
3. `then 子句的 IR`
4. `label END_LABEL`

## 汇编生成
如下表：

| IR       | 汇编                                                |
| ---      | ---                                                 |
| `label LABEL_STR` | `LABEL_STR:` |
| `br LABEL_STR` | `j LABEL_STR`[^2] |
| `beqz LABEL_STR` | `lw t1, 0(sp)  ;  addi sp, sp, 4  ;  beqz t1, LABEL_STR` |
| `bnez LABEL_STR` | `lw t1, 0(sp)  ;  addi sp, sp, 4  ;  bnez t1, LABEL_STR` |

# 思考题

1. Rust 和 Go 语言中的 if-else 语法与 C 语言中略有不同，它们都要求两个分支必须用大括号包裹起来，而且条件表达式不需要用括号包裹起来：

```Rust
if 条件表达式 {
  // 在条件为 true 时执行
} else {
  // 在条件为 false 时执行
}
```

请问相比 C 的语法，这两种语言的语法有什么优点？

# 总结
本节主要就是引入了跳转，后面 step8 循环语句还会使用。

# 备注
[^1]: 见思考题
[^2]: 如果 `LABEL_STR` 在当前函数内，`j LABEL_STR` 就等于 `beqz x0, LABEL_STR`
