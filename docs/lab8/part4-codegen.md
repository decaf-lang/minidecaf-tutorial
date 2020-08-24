## 汇编代码生成

### 空语句

对于空语句的代码生成过程很简单，即不要为空语句生成任何汇编。

### `while` 循环

给定一个 `while` 循环：

```c
while (<condition>)
    <statement>
```

我们可以这样描述它的代码生成流程：

1. 生成计算 `<condition>` 的代码
2. 如果结果是假的，跳到步骤 5
3. 生成 `<statement>` 的代码
4. 跳到步骤 1
5. 完成

在这里就不展示需要生成的具体汇编了，参考 RISC-V 指令集选取合适的指令（条件跳转和无条件跳转）。最主要的是给步骤 1 和步骤 5 打上标签（label），这样当我们需要跳转指令时，就有地方可以跳转了。

### `do` 循环

对于一个 `do` 循环：

```c
do
    <statement>
while (<condition>);
```

和 `while` 循环不同，`do` 循环会先执行循环体 `<statement>`，再计算 `<condition>` 的值，如果结果为真，才跳转到循环体头部，否则不跳转而结束循环。请参考 `while` 循环实现 `do` 循环的代码生成。

### `for` 循环

给出这样一个 `for` 循环：

```c
for (<init>; <condition>; <post-expression>)
    <statement>
```

可以转换成如下的 `while` 循环：

```c
<init>
while (<condition>) {
    <statement>
    <post-expression>
}
```

类似地，`for` 循环也可转换为一个 `do` 循环，不过需要增加 `<init>` 后直接跳转到计算 `<condition>` 这一步。因此，你可以直接复用 `while` 循环或 `do` 循环的代码生成过程，为 `for` 循环生成代码。

需要注意的是，`<init>` 和 `<post-expression>` 都有可能是空的，在这种情况下，我们只是不生成任何汇编。对于 `<condition>` 为空的情况，还需修改相应的条件跳转语句。

<!--
TODO：语义检查
此外，整个 `for` 循环（包括 `init` 这些控制表达式）是一个有自己作用域（scope）的块（block），而 `for` 循环的*体（body）*也是一个块（block）。这意味着你可以有这样的代码：

```c
int i = 100; // scope 1
for (int i = 0; i < 10; i = i + 1) { // scope 2 - variable i shadows previous i
    int i; //scope 3 - this variable i shadows BOTH previous i's
}
```

这里的主要问题是，当你退出代码块时，你需要把在 `init` 中声明的变量从堆栈中弹出，就像你在上一篇文章中需要处理释放其他变量一样。 -->

### `break` 和 `continue` 语句

我们可以用一条直接跳转指令实现这两条语句，关键是找出跳转到哪里：

* `break`：跳转到“循环结束”标签；
* `continue`：
    + 对于 `while` 循环：跳转到计算 `<condition>` 前面；
    + 对于 `do` 循环：跳转到生成 `<statement>` 前面；
    + 对于 `for` 循环：跳转到生成 `<post-expression>` 前面；

<!--
TODO：语义检查
另外需要注意，如果你不在一个循环里面，就不能使用 `break` 或 `continue` 语句，此时应该有适当的错误提示。
-->
