
# lab4：更多二元操作符


本次试验将添加一些布尔运算符（`&&`，`||`）和一大堆关系运算符（`<`，`==`，等）。由于我们已经知道如何处理二元运算符，所以本次试验将非常简单。我们将增加8个新的操作符：

- 逻辑与：Logical AND `&&`
- 逻辑或：Logical OR `||`
- 等于：Equal to `==`
- 不等于：Not equal to `!=`
- 小于：Less than `<`
- 小于或等于：Less than or equal to `<=`
- 大于：Greater than `>`
- 大于或等于：Greater than or equal to `>=`

像往常一样，我们将更新我们的词法分析、解析解析和代码生成过程来支持这些操作。

## 词法分析

每一个新的操作符都对应一个新的标记。下面是我们需要支持的全部标记列表，旧的标记在顶部，新的标记在底部用粗体表示。

- Open brace `{`
- Close brace `}`
- Open parenthesis `(`
- Close parenthesis `)`
- Semicolon `;`
- Int keyword `int`
- Return keyword `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`
- Minus `-`
- Bitwise complement `~`
- Logical negation `!`
- Addition `+`
- Multiplication `*`
- Division `/`
- **AND `&&`**
- **OR `||`**
- **Equal `==`**
- **Not Equal `!=`**
- **Less than `<`**
- **Less than or equal `<=`**
- **Greater than `>`**
- **Greater than or equal `>=`**

#### ☑任务

更新*lex*函数以处理新的标记。应该通过测试集中所有step[1-4]的测试例子。

## 语法解析

在上个试验的语法中，每一个操作符的优先级都需要一个生产式。本次试验有了更多的优先级，这意味着我们的语法会增加一些。然而，我们的解析策略并没有任何改变；我们将以与旧的`exp`和`term`规则完全相同的方式处理新的生产式。这可能有些重复或乏味，但通过练习，希望能帮助同学巩固所有关于语法解析的方法。

下面是我们所有的二进制运算符，从最高到最低的优先级：

- Multiplication & division (`*`, `/`)
- Addition & subtraction (`+`,`-`)
- Relational less than/greater than/less than or equal/greater than or equal (`<`, `>`,`<=`,`>=`)
- Relational equal/not equal (`==`, `!=`)
- Logical AND (`&&`)
- Logical OR (`||`)

我们上周处理了前两个要点，最后四个要点是新的。我们将为最后四个要点各增加一条生产规则。新的语法如下，修改/增加的规则用黑体表示。

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
<logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
<equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
<relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
<additive-exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
<unary_op> ::= "!" | "~" | "-"
```

`<additive-exp>`与上周的`<exp>`相同。我们必须重新命名，因为`<exp>`现在指的是`逻辑或`表达式，现在它的优先级最低。

上次试验写了`parse_exp`和`parse_term`函数；本次实验需要实现`parse_relational_exp`、`parse_equality_exp`等函数。除了处理不同的运算符外，这些函数的处理过程都大致相同。

为了完整起见，这里给出是语法解析的AST定义：

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = BinOp(binary_operator, exp, exp) 
    | UnOp(unary_operator, exp) 
    | Constant(int)
```

这与上次lab的AST定义相同，只是我们增加了更多可能的`binary_operator`值。

#### ☑ 任务

更新表达式解析（expression-parsing）代码以处理本周新的二元运算符。它应该成功解析测试集中所有step[1-4]的例子。测试套件不会直接验证你的程序是否生成了正确的AST，所以你需要手动检查每个例子的AST以确保它是正确的。

## 代码生成

我们对处理二进制运算的代码生成的一般方法与上个实验相同：

1. 计算 `e1`的值
2. 把值推到（push）堆栈上
3. 计算`e2`的值
4. 将 `e1 `的值从堆栈中弹回（pop）到某寄存器中
5. 对`e1`和`e2`进行二元操作

所有新的值将在步骤5中出现。

### 关系运算符

我们先来处理关系运算符。与第2周的逻辑NOT运算符（`！`）一样，这些运算符对真结果返回1，对假结果返回0。这些运算符与`！`几乎相同，只是它们将两个表达式相互比较。

下面是我们在lab2为`！`生成的汇编：

```
    <CODE FOR exp GOES HERE>
    cmpl   $0, %eax    ;set ZF on if exp == 0, set it off otherwise
    movl   $0, %eax    ;zero out EAX (doesn't change FLAGS)
    sete   %al         ;set AL register (the lower byte of EAX) to 1 iff ZF is 1
```

我们可以稍微修改一下，实现`==`：

```
    <CODE FOR e1 GOES HERE>
    push   %eax          ; save value of e1 on the stack
    <CODE FOR e2 GOES HERE>
    pop    %ecx          ; pop e1 from the stack into ecx - e2 is already in eax
    cmpl   %eax, %ecx    ;set ZF on if e1 == e2, set it off otherwise
    movl   $0, %eax      ;zero out EAX (doesn't change FLAGS)
    sete   %al           ;set AL register (the lower byte of EAX) to 1 iff ZF is on
```

`sete`指令只是一系列条件集指令中的一种。还有`setne`(如果不等于则置`1`)，`setge`(如果大于或等于则置`1`)，等等。要实现`<`、`>`和其他关系运算符，我们可以生成与上面`==`完全相同的汇编，只是用适当的条件汇编指令替换`sete`。很简单!

在lab2中，我们谈到了用零标志(ZF)来测试相等。但是我们不能用ZF来确定哪个操作数更大。为此，我们需要符号标志(SF)，如果一个操作的结果是负数，就会设置这个标志，就像这样：

```
    movl $0, %eax ;zero out EAX
    movl $2, %ecx ;ECX = 2
    cmpl $3, %ecx ;compute 2 - 3, set flags
    setl %al      ;set AL if 2 < 3, i.e. if 2 - 3 is negative
```

现在我们来谈谈`&&`和`||`。
> 后续会分别用`&`和`|`来表示位与（`bitwise AND`）和位或（`bitwise  OR`）。

### （可选）短路逻辑评估

C11标准保证了对`&&`和`||`的逻辑评估会短路（short-circuit）：如果我们在评估第一个子句（clause）后知道了结果，就不会评估第二个子句。例如，考虑下面这行代码。

```
return 0 && foo();
```

因为第一个子句结果是假，我们就不需要知道`foo`的返回值，所以我们根本不会调用`foo`。是否调用`foo`不会改变这一行的返回值，但它可能会执行I/O，更新全局变量，或者产生其他重要的副作用。所以确保`&&`和`||`短路不仅仅是一种性能优化，它是一些程序正确执行所必需的。

###逻辑或 OR

为了保证逻辑或短路（short-circuit），我们需要在子句1为真时跳过子句2。我们将按照以下步骤来计算`e1 || e2`。

1. 计算`e1`
2. 如果结果为0，则跳到步骤4
3. 将EAX设为1，并跳到最后
4. 计算`e2`
5. 如果结果为0，则将EAX设为0，否则将EAX设为1

步骤2将需要一种新的指令类型，称为**条件跳转**。这些指令类似于我们已经使用过的条件集指令，如`sete`和`setne`。唯一不同的是，它们不是将一个字节设置为1，而是跳转到汇编代码中的一个特定点，我们用一个标签（label）来指定。下面是 "je "的一个例子，"如果相等则跳转 "指令的操作。

```
    cmpl $0, %eax ; set ZF if EAX == 0
    je _there    ; if ZF is set, go to _there
    movl $1, %eax
    ret
_there:
    movl $2, %eax
    ret
```

如果在这段代码开始时`EAX`为0，它将返回2；否则将返回1。让我们看看在每种情况下到底会执行什么指令。

首先考虑在开始时EAX为零的情况：

1. `cmpl $0, %eax` 因为EAX是0，所以将把零标志（ZF）设置为真
2. `je _there`因为ZF为真，所以会跳转
3. `movl $2, %eax` 这是接下来执行的，因为它是`_there`之后的第一条指令。它将EAX设为2
4. `ret` 返回值将是2

现在考虑EAX不为零的情况：

1. `cmpl $0, %eax` 因为EAX不是0，所以将ZF设置为false
2. `je _there`因为ZF是假的，所以不会跳转，所以这条指令不执行
3. `movl $1, %eax` 因为没有跳转，所以CPU控制照常传递到下一条指令。它将EAX设为1
4. `ret`返回值将是1

我们还需要`jmp`指令，它执行无条件跳转。下面是一个`jmp`操作的例子：

```
    movl $0, %eax ; zero out EAX
    jmp _there    ; go to _there label
    movl $5 %eax  ; this will never execute, we always jump over it
_there:
    ret           ; will always return zero
```

现在我们已经熟悉了`jmp`和`je`，下面是`e1 || e2`的汇编代码：

```
    <CODE FOR e1 GOES HERE>
    cmpl $0, %eax            ; check if e1 is true
    je _clause2              ; e1 is 0, so we need to evaluate clause 2
    movl $1, %eax            ; we didn't jump, so e1 is true and therefore result is 1
    jmp _end
_clause2:
    <CODE FOR e2 GOES HERE>
    cmpl $0, %eax            ; check if e2 is true
    movl $0, %eax            ; zero out EAX without changing ZF
    setne %al                ; set AL register (the low byte of EAX) to 1 iff e2 != 0
_end:
```

注意，标签（label）必须是唯一的。这意味着实际上不能使用`_clause2`或`_end`作为标签，因为如果程序中包含一个以上的逻辑OR，你会有重复的标签。也许应该写一个实用函数（label generator ，标签生成器）来生成唯一的标签。它不需要很花哨，标签生成器只是在每个标签中包含一个递增的计数器。

这里的"_end "标签可能看起来很奇怪，因为它看起来并没有给任何东西贴标签。事实上，它标记了这个表达式之后的任何内容；它只是给我们提供了一个目标位置来跳过`_clause2`。

### 逻辑与 AND

逻辑与的处理几乎与逻辑或相同，只是如果`e1`是`0`，我们就会短路。 我们使用`jne`(跳转如果不相等)指令。在这种情况下，我们不需要将任何东西移入EAX，因为0是我们想要的结果。下面是汇编代码：

```
    <CODE FOR e1 GOES HERE>
    cmpl $0, %eax            ; check if e1 is true
    jne _clause2             ; e1 isn't 0, so we need to evaluate clause 2
    jmp _end
_clause2:
    <CODE FOR e2 GOES HERE>
    cmpl $0, %eax            ; check if e2 is true
    movl $0, %eax            ; zero out EAX without changing ZF
    setne %al                ; set AL register (the low byte of EAX) to 1 iff e2 != 0
_end:
```

与逻辑或一样，我们需要确保标签（label）是唯一的。

#### ☑任务

更新你的代码生成通证，为`&&`, `||`, `==`, `!=`, `<`, `<=`, `>`, 和`>=`发出正确的代码。它应该在所有有效的例子上成功(除了`skip_on_failure_`的例子)，在第1-4阶段的所有无效例子上失败。

## （可选）其他二元操作符

我们还没有实现所有的二进制运算符！我们还不能实现赋值运算符（如`+=`和`-=`），因为我们不支持局部变量。我们还没有实现所有的二进制运算符！我们还不能实现赋值运算符（比如`+=`和`-=`），因为我们不支持局部变量。但是现在你应该可以自己实现其他的运算符。

- 位与：Bitwise AND `&`
- 位或：Bitwise OR `|`
- 位异或：Bitwise XOR `^`
- 位左移：Bitwise shift left `<<`
- 位右移：Bitwise shift right `>>`


## 下一步

下一个实验中，我们将增加局部变量。这意味着我们终于可以写出不只是返回语句的程序了。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)