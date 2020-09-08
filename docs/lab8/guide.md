# step8 实验指导

## 词法语法分析
如果你使用工具完成词法语法分析，修改你的语法规范以满足要求，自行修改词法规范，剩下的交给工具即可。

值得一提的是，四种循环大同小异，都可以写成 `Loop(pre, cond, body, post)`，AST 中可以用一个统一的节点表示。
> `Loop(pre, cond, body, post)` AST 结点表示如下的一个循环
> ```c
> { // pre 里面可能有声明，所以需要这个作用域
>     pre;                // 可能是空、也可能是一个 declaration 或者 expression
>     while (cond) {      // 可能是空、也可能是一个 expression
>         body;
>         // body 里的 continue 会跳转到这里
>         post;           // 是一个 expression
>     }
>     // break 跳转到这里
> }
> ```

如果你是手写分析，TODO

## 名称解析
变量名相关的解析不变，但注意按照语义规范 8.2，for 要自带一个作用域。

另外，我们需要确定：每个 break 和 continue 跳转到的标号是哪个。
实现很容易，类似符号表栈维护 break 标号栈和 continue 标号栈。
1. 遇到 `Loop(...)` 就（一）创建这个循环的 break 标号和 continue 标号（以及起始标号）；
    （二）把两个标号压入各自栈里；
    （三）离开 `Loop` 的时候弹栈。
> 和 step6 一样，各个循环的标号需要唯一，简单地后缀一个计数器即可。
2. 每次遇到 break 语句，其跳转目标就是 break 标号栈的栈顶，如果栈为空就报错。continue 语句类似。

## IR 生成
无新增 IR。

这一阶段 Visitor 遍历 AST 时，遇到 `Loop(pre, cond, body, post)`，生成的 IR 如
1. `pre 的 IR`
2. `label BEGINLOOP_LABEL`：开始下一轮迭代
3. `cond 的 IR`
4. `beqz BREAK_LABEL`：条件不满足就终止循环
5. `body 的 IR`
6. `label CONTINUE_LABEL`：continue 跳到这
7. `post 的 IR`
8. `br BEGINLOOP_LABEL`：本轮迭代完成
9. `label BREAK_LABEL`：条件不满足，或者 break 语句都会跳到这儿

> 其中 `XXX_LABEL` 要和上一步名称解析生成的标号名一样。

遇到 break 语句的 AST 结点时，生成一条 `br BREAK_LABEL`，其中 `BREAK_LABEL` 是名称解析确定的标号。

## 汇编生成
不变。

# 任务
1. 改进你的编译器，支持本节引入的新特性，通过相关测试。
2. 实验报告中回答思考题。

# 总结
step8 相对容易。

