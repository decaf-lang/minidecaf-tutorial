# lab3：二元运算符


本次lab将添加二元运算来支持基本的算术运算。我们将弄清楚如何正确处理运算符的优先性和关联性。我们将增加几个二元运算（取两个值的运算符）：

- 加：Addition  `+`
- 减：Subtraction `-`
- 乘：Multiplication `*`
- 除：Division `/`
- 取模：Mod `%`

像往常一样，我们会更新编译器的每个阶段来支持这些操作。

## 词法分析

除了`减`二元运算符，上面的每一个运算符都需要一个新的标记（我们已经有一个`-`标记）。不管是减运算符还是否定运算符，它的标记化方式都是一样的；我们将在语法解析阶段弄清楚如何解释它。算术表达式也可以包含圆括号，但我们已经有了圆括号的标记，所以我们根本不需要改变我们的词法分析器来处理它们。

下面是我们需要支持的全部标记列表。前几此lab用到的标记在顶部，新的标记在底部加粗。

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
- **Addition `+`**
- **Multiplication `*`**
- **Division `/`**
- **Mod `%`**

#### ☑任务

更新*lex*函数以处理新的标记。它应该适用于测试集中所有`step[123]`中的例子。

## 解析

本周我们需要给我们的AST添加另一个表达式类型：二元操作（binary operations）。下面是我们AST节点的最新定义集合；只有`exp`的定义发生了变化。

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

请注意，我们现在在AST定义中区分了二元和一元运算符。例如，取负一元运算符的`-`和减二元运算符的`-`在我们的AST中是不同的类型（type）。下面是我们如何构建`2 - (-3)`的AST：

```
two = Const(2)
three = Const(3)
neg_three = UnOp(NEG, three)
exp = BinOp(MINUS, two, neg_three)
```

我们还需要改变语法中`<exp>`的定义。最明显的定义是这样的：

```
<exp> ::= <exp> <binary_op> <exp> | <unary_op> <exp> | "(" <exp> ")" | <int>
```

但这种语法有几个相关问题。

1. **它没有处理运算符的优先性**。考虑表达式`2 + 3 * 4`。使用上面的语法，你可以构建两种可能的解析树。

   ![Parse tree for expression interpreted as (2 + 3) * 4, outline below.](./lab3-pics/exp1.svg)

   Tree #1

   ![Parse tree for expression interpreted as 2 + (3 * 4), outline below.](./lab3-pics/exp2.svg)

   Tree #2

   使用第一棵解析树，这个表达式评价为`(2 + 3) * 4 = 24`。使用第二棵树，则是`2 + (3 * 4) = 14`。根据C语言标准和数学惯例，`*`比`+`具有更高的先验性，所以第二棵解析树是正确的。我们的语法必须以某种方式对这种优先级（precedence）进行编码。

   这也是我们的一元运算的一个问题--根据这个语法，`~2 + 3`可以被解析为`~(2 + 3)`，这当然是错误的。


2. **它不处理结合性（associativity）**。同一优先级的操作应从左到右进行评估（evaluate）。例如`1 - 2 - 3`应该解析为`(1 - 2) - 3`。但是，根据上面的语法，解析为`1 - (2 - 3)`也是有效的。

3. **它是左递归（left-recursive）**。在上面的语法中，`<exp>`的一个产生式是：

```
  <exp> ::=  <exp> <binary_op> <exp>
```

   在这个生产式中，最左边（即第一个）的符号也是`<exp>`--这就是左递归的意思。左递归语法并非不正确，但递归下降（Recursive Descent，简称RD）语法解析器无法处理它们。我们将在后面的文章中讨论为什么这是一个问题。

让我们从问题1开始考虑解决方案。我们先处理一元运算符--它们的优先级总是比二元运算符高。只有在以下情况下，才应该将一元运算符应用于整个表达式。

- 表达式是单个整数 (例如 `~4`)
- 表达式被括号包围住(例如`~(1+1)`)
- 表达式本身就是一个一元运算（例如`~！8`，`-~(2+2)`）

为了表达这一点，我们需要在我们的语法中使用另一个符号来指代 "一个用一元运算符的表达式"。我们称它为因子（`factor`）。我们将这样重写我们的语法：

```
<exp> ::= <exp> <binary_op> <exp> | <factor>
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
```

我们现在已经创建了两个优先级：一个用于二元操作，一个用于一元操作。我们还通过将表达式放在括号内强制执行更高的优先级，来正确地处理括号。

我们可以做类似的改变，使得`*`和`/`比`+`和`-`具有更高的优先级。我们之前添加了一个`<factor>`符号，代表一元运算的操作数。现在我们将添加一个`<term>`符号，代表乘法和除法的操作数：

```
<exp> ::= <exp> ("+" | "-") <exp> | <term>
<term> ::= <term> ("*" | "/") <term> | <factor>
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
```

这个语法正确地编码了运算符的优先级。现在`2 + 3 * 4`只有一个可能的解析树。

![Parse tree according to new grammar for 2 + (3 * 4), outline below](./lab3-pics/exp_fixed.svg)



这就是问题1解决了。问题2是这个语法没有处理结合性。如果你没有使用递归下降语法解析器，一般来说，你对左结合操作使用左递归生产式，对右结合操作使用右递归产生式。在这种情况下，我们可以这样重写`<exp>`的产生式：

```
<exp> ::= <exp> ("+" | "-") <term> | <term>
```

这将使得加法和减法成为左递归；你不能把`1 - 2 - 3`解析为`1 - (2 - 3)`，因为`2 - 3`不是一个项（`term`）。

但是我们使用的是递归下降语法解析器，所以我们不能处理这个左递归规则。为了理解为什么这行不通，我们试着写一个函数来根据这个规则解析表达式。

```
def parse_expression(tokens):
    //determine which of two production rules applies:
    //  * <exp> ("+" | "-") <term>
    //  * <term>
    if is_term(tokens): //how do we figure this out???
        return parse_term(tokens)
    else:
        //recursively call parse_expression to handle it
        e1 = parse_expression(tokens) //recurse forever ☠️
```

要想知道使用哪条生产规则，我们不能只看第一个标记--我们需要知道这个表达式中是否有`+`或`-`操作。如果我们确定这个表达式是一个求和（sum）或求差（difference），我们就会永远递归地调用`parse_expression`函数。为了不这样做，我们需要找到表达式末尾的最后一个`<term>`，解析并删除它，然后再回过头来解析剩下的内容。这两个问题（找出使用哪条生产式，以及解析最后一个`term`）都需要我们向前看一个任意数量的标记，直到找到表达式的结尾。你也许能让这种方法发挥作用--如果有类似的现有解析算法--它应该也会很复杂低效，而且不会是一个递归下降解析器。所以我们不打算这么做。

另一方面，如果我们只是把`<term>`和`<exp>`调换一下以避免左递归，我们就会有这样的规则。

```
<exp> ::= <term> ("+" | "-") <exp> | <term>
```

这很容易解析，但却是错误的--它是*右结合*。使用这个语法，你会将`1 - 2 - 3`解析为`1 - (2 - 3)`。

所以我们的选择似乎是一个不可解析的左递归语法，或者是一个不正确的右递归语法。幸运的是，还有另一种解决方案。我们将在我们的语法中引入重复（repetition），所以我们可以将一个表达式定义为一个`term`，可能加或减一个`term`，可能加或减另一个`term`......永远如此。在EBNF符号中，用大括号(`{}`)包住某个东西意味着它可以重复零次或多次。这是我们本此实验将用于表达式的**最终**语法。

```
<exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
```

这个语法正确地处理了优先级，它不是左递归，也不是右结合。然而，它也不是真正的左结合。以前，一个`<exp>`是一个有两个项的二元操作--现在它有任意数量的项。如果你有一堆操作在同一优先级（比如`1 - 2 - 3`），这个语法并没有提供任何方法将它们归为子表达式。

不过这也没关系，我们的语法不需要与我们的AST完全对应。我们仍然可以用左结合的方式来构建我们的AST。我们将解析第一个`term`，然后，如果有更多的`term`，我们将以循环的方式处理它们，在每次迭代时构建一个新的BinOp节点。下面是这个处理过程的伪代码：

```
def parse_expression(toks):
    term = parse_term(toks) //pops off some tokens
    next = toks.peek() //check the next token, but don't pop it off the list yet
    while next == PLUS or next == MINUS: //there's another term!
        op = convert_to_op(toks.next())
        next_term = parse_term(toks) //pops off some more tokens
        term = BinOp(op, term, next_term)
        next = toks.peek()

    return t1
```

我们可以在`parse_term`中使用完全相同的方法。

`parse_factor`的实现很直接，因为它不需要处理结合性。我们将查看第一个标记，以确定要使用哪个生产式；弹出（pop off ）常量，并确保它们具有我们期望的值；并调用其他函数来处理非终结符：

```
def parse_factor(toks)
    next = toks.next()
    if next == OPEN_PAREN:
        //<factor> ::= "(" <exp> ")"
        exp = parse_exp(toks) //parse expression inside parens
        if toks.next() != CLOSE_PAREN: //make sure parens are balanced
            fail()
        return exp
    else if is_unop(next)
        //<factor> ::= <unary_op> <factor>
        op = convert_to_op(next)
        factor = parse_factor(toks)
        return UnOp(op, factor)
    else if next.type == "INT":
        //<factor> ::= <int>
        return Const(convert_to_int(next))
    else:
        fail()
```

这里是本次lab的完整语法，包括上面的新东西（表达式--expressions、项--terms、因子--factors）和从上次lab开始没变的东西（函数--functions、语句--statements等）：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
```

#### ☑ 任务：更新表达式解析代码，处理加减乘除

更新你的表达式解析代码，以处理加、减、乘、除、取模。它应该成功地解析测试用例中所有有效的step[1-3]的例子。手动检查每个例子的AST，以确保它正确处理结合性和运算符优先级。

## 代码生成

本周在代码生成阶段有一个新的挑战。要处理一个二元表达式，比如`e1+e2`，我们生成的汇编需要：

- 计算 "e1 "并将其保存在某处
- 计算`e2`
- 将`e1`加到`e2`，并将结果存储在EAX中

所以，我们需要一个地方来保存第一个操作数。把它保存在寄存器中会很复杂。因为第二个操作数本身可以包含子表达式，所以可能还需要把中间结果保存在寄存器中，这导致有可能覆盖`e1`。为了简单起见，我们可以把第一个操作数保存在栈（`stack`）中。

让我们简单地谈谈栈（`stack`）。计算机上的每个进程都有一些内存。这个内存被分为几段，其中一段就是**调用栈（call stack）**，或者说只是栈。栈顶的地址存储在ESP寄存器中，也就是栈指针。像大多数堆栈一样，你可以把东西推到（`push`）顶上，或者从顶上弹出（`pop`）东西；x86包括`push`和`pop`指令来做这些事情。关于堆栈的一个令人困惑的事情是，它向*低的*内存地址增长--当你把东西推到堆栈上时，你*减少了*ESP。处理器依靠ESP来计算栈顶在哪里。所以，`pushl val`做了以下事情：

- 把`val`写到栈的下一个空的位置(即ESP - 4)
- 将ESP减少4，所以它包含`val`的内存地址

![On the left, a diagram of the stack value a is on top at memory address 0xbffff980. Other values below a have higher memory addresses. The ESP register holds value 0xbffff980, the address of a. On the right, a diagram representing the stack after "val" is pushed onto it. Now "val" is on top of the stack at address 0xbffff97c, and ESP holds value 0xbffff97c. "a" is just below "val", at the same address as before.](./lab3-pics/push_val.svg)

同样，"popl dest "做了如下事情：

- 从堆栈顶部读取数值（即ESP中内存地址的数值）
- 将该值复制到`dest`中，这是一个寄存器或其他内存位置
- 将ESP增加4，所以它指向`val`下面的值

但现在，你真正需要知道的是，有一个栈，"push "把东西放在上面，"pop "把东西拿下来。所以，这里是我们的 "e1 + e2 "的汇编代码：

```
    <CODE FOR e1 GOES HERE>
    push %eax ; save value of e1 on the stack
    <CODE FOR e2 GOES HERE>
    pop %ecx ; pop e1 from the stack into ecx
    addl %ecx, %eax ; add e1 to e2, save results in eax
```

你可以用同样的方法处理`e1 * e2`，用`imul`代替`addl`。减法比较复杂，因为操作数的顺序很重要；`subl src, dst`计算`dst - src`，并将结果保存在`dst`中。你需要确保`e1`在`dst`中，`e2`在`src`中--当然，结果最终在EAX中。除法就更棘手了：`idivl dst`将EDX和EAX作为一个单一的64位寄存器，并计算`[EDX:EAX] / dst`。然后，它将商存储在EAX中，余数存储在EDX中。为了能正确工作，你需要先把`e1`移到EAX中，然后在发出`idivl`指令之前，用`cdq`指令把它有符号扩展到EDX中。

#### ☑任务：生成正确汇编代码

更新你的代码生成器，生成正确的加、减、除、乘、取模代码。它应该在step[123]中的所有例子上成功生成正确汇编代码。


## 接下来

下一个实验将增加更多的二元运算符来支持比较和布尔逻辑。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)