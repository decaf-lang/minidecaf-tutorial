# step8 实验指导

本实验指导使用的例子为：

```C
for (int i = 0; i < 5; i = i + 1)
    break;
// 后续语句 ...
```

## 词法语法分析

针对循环语句和 break/continue 语句，我们需要设计 AST 节点来表示它，给出的参考定义如下：

| 节点 | 成员 | 含义 |
| --- | --- | --- |
| `While` | 循环条件 `cond`，循环体 `body` | while 循环语句 |
| `For` | 初始语句 `init`，循环条件 `cond`，更新语句 `update`，循环体 `body` | for 循环语句 |
| `Break` | 无 | break 语句 |
| `Continue` | 无 | continue 语句 |

其中，while 和 break 语句的实现已经在框架中给出，同学们可以参考并实现 for 和 continue 语句。

## 语义分析

本步骤语义分析阶段的处理方式和 Step7 中的 if 语句相类似，但是请额外注意以下两点：

1. for 循环要自带一个作用域。在示例里，`for (int i = 0; i < 5; i = i + 1)` 语句里定义的循环变量处于一个独自的作用域里。这也就是说，我们可以在循环体内部定义同名变量。如果我们把示例修改为：`for (int i = 0; i < 5; i = i + 1) { int i = 0; }` 这也是合法的 MiniDecaf 程序。因此，在符号表构建阶段，扫描到 for 结点时，不要忘记开启一个局部作用域。

2. break 和 continue 语句必须位于循环体内部才合法。因此，在扫描过程中，需要记录当前结点位于多少重循环内。扫描到 break 和 continue 结点时，若当前不处于任何循环内，则报错。

## 中间代码生成

本步骤中没有需要新增的 TAC 指令。不过为了实现循环语句，需要仔细地考虑如何将 MiniDecaf 循环语句翻译成 TAC 的分支跳转指令。由于 while 循环可以看作 for 循环的特例，我们选择了 for 循环作为示例。
让我们先来看看示例对应的 TAC 代码：

```assembly
    _T1 = 0
    _T0 = _T1                 # int i = 0;
_L1:                          # begin label
    _T2 = 5
    _T3 = LT _T0, _T2
    BEQZ _T3, _L3              # i < 5;
_L2:                          # loop label
    _T4 = 1
    _T5 = ADD _T0, _T4
    _T0 = _T5                 # i = i + 1;
    JUMP _L1
_L3:                          # break label
    # 后续指令 ...
```

为了实现所有可能的跳转，对每个 for 循环我们都需要定义三个跳转标签：begin, loop 和 break。它们的作用如下：

1. begin 标签（示例中的 _L1）是循环体的开始位置。初次进入循环时，从这个标签的位置开始执行，并判断循环条件是否满足，若不满足，则跳转到 break 标签（示例中的 _L3）处。

2. loop 标签（示例中的 _L2）是执行 continue 语句时应当跳转到的位置。

3. break 标签是整个循环结束后的位置。如果循环条件不满足，或者执行了 break 语句，那么应当跳转到此处，执行循环之后的指令。

请注意，示例给出的只是一种循环语句**参考实现**，同学们也可以设计自己的实现方法。

由于循环语句可以嵌套，所以 TAC 语句生成过程中需要动态维护 loop 标签和 break 标签，这样才能确定每一条 break 和 continue 语句跳转到何处。因此，在 TAC 生成时，需要使用栈结构维护从内到外所有的 loop 标签和 break 标签。

`utils/tacgen/tacgen.py` 里的 `TACFuncEmitter` 类里实现了维护 TAC 生成时需要的上下文信息的功能。同学们可以在这个类中增加对循环所需的 break/continue 标签的维护。

## 目标代码生成

由于不需要增加新的中间代码指令，本步骤中目标代码生成模块没有新的内容。除非之前步骤的实现有误，否则这个步骤应该不会出现错误。

# 思考题

1. 将循环语句翻译成 IR 有许多可行的翻译方法，例如 while 循环可以有以下两种翻译方式：

    第一种（即实验指导中的翻译方式）：
    
    + `label BEGINLOOP_LABEL`：开始下一轮迭代
    + `cond 的 IR`
    + `beqz BREAK_LABEL`：条件不满足就终止循环
    + `body 的 IR`
    + `label CONTINUE_LABEL`：continue 跳到这
    + `br BEGINLOOP_LABEL`：本轮迭代完成
    + `label BREAK_LABEL`：条件不满足，或者 break 语句都会跳到这儿
    
    第二种：
    
    + `cond 的 IR`
    + `beqz BREAK_LABEL`：条件不满足就终止循环
    + `label BEGINLOOP_LABEL`：开始下一轮迭代
    + `body 的 IR`
    + `label CONTINUE_LABEL`：continue 跳到这
    + `cond 的 IR`
    + `bnez BEGINLOOP_LABEL`：本轮迭代完成，条件满足时进行下一次迭代
    + `label BREAK_LABEL`：条件不满足，或者 break 语句都会跳到这儿
    
    从执行的指令的条数这个角度（`label` 不算做指令，假设循环体至少执行了一次），请评价这两种翻译方式哪一种更好？

2. 我们目前的 TAC IR 中条件分支指令采用了单分支目标（标签）的设计，即该指令的操作数中只有一个是标签；如果相应的分支条件不满足，则执行流会继续向下执行。在其它 IR 中存在双目标分支（标签）的条件分支指令，其形式如下：
    
    ```assembly
    br cond, false_target, true_target
    ```
    
    其中`cond`是一个临时变量，`false_target`和`true_target`是标签。其语义为：如果`cond`的值为0（假），则跳转到`false_target`处；若`cond`非0（真），则跳转到`true_target`处。它与我们的条件分支指令的区别在于执行流总是会跳转到两个标签中的一个。
    
    你认为中间表示的哪种条件分支指令设计（单目标 vs 双目标）更合理？为什么？（言之有理即可）
