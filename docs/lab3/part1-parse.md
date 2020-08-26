# 词法语法解析

## 词法解析

在本实验中，我们需要添加二元运算来支持基本的算术运算。我们将弄清楚如何正确处理运算符的优先性和关联性。需要支持的二元运算包括：

- 加：Addition  `+`
- 减：Subtraction `-`
- 乘：Multiplication `*`
- 除：Division `/`
- 取模：Mod `%`

除了`减`二元运算符，上面的每一个运算符都需要一个新的标记（我们已经有一个`-`标记）。不管是减运算符还是否定运算符，它的标记化方式都是一样的；我们将在语法解析阶段弄清楚如何解释它。算术表达式也可以包含圆括号，但我们已经有了圆括号的标记，所以我们不需要改变我们的词法分析器来处理它们。我们修改标记列表以支持新的运算符，新的标记列表如下所示：

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

## 语法解析

在本次实验中，我们需要给我们的AST添加另一个表达式类型：二元操作（binary operations）。

### 直接定义的问题

首先是对语法的定义，以使解析器可以进行解析。最明显的定义是这样的：

```
<exp> ::= <exp> <binary_op> <exp> | <unary_op> <exp> | "(" <exp> ")" | <int>
```

但这种语法有几个相关问题。

1. **它没有处理运算符的优先性**。考虑表达式`2 + 3 * 4`。使用上面的语法，你可以构建两种可能的解析树。`(2 + 3) * 4 = 24`或`2 + (3 * 4) = 14`。根据C语言标准和数学惯例，`*`比`+`具有更高的先验性，所以第二棵解析树是正确的。我们的语法必须以某种方式对这种优先级（precedence）进行编码。这也是我们的一元运算的一个问题--根据这个语法，`~2 + 3`可以被解析为`~(2 + 3)`，这当然是错误的。

2. **它不处理结合性（associativity）**。同一优先级的操作应从左到右进行评估（evaluate）。例如`1 - 2 - 3`应该解析为`(1 - 2) - 3`。但是，根据上面的语法，解析为`1 - (2 - 3)`也是有效的。

3. **它是左递归（left-recursive）**。在上面的语法中，`<exp>`的一个产生式是：

```
  <exp> ::=  <exp> <binary_op> <exp>
```

在这个生产式中，最左边（即第一个）的符号也是`<exp>`，这就是左递归的意思。左递归语法并非不正确，但递归下降（Recursive Descent，简称RD）语法解析器无法处理它们。我们将在后面的文章中讨论为什么这是一个问题。

### 处理优先级

让我们从问题1开始考虑解决方案。我们先处理一元运算符，因为它们的优先级总是比二元运算符高。只有在以下情况下，才应该将一元运算符应用于整个表达式。

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

### 处理结合性

问题2是这个语法没有处理结合性。如果你没有使用递归下降语法解析器，一般来说，你对左结合操作使用左递归生产式，对右结合操作使用右递归产生式。在这种情况下，我们可以这样重写`<exp>`的产生式：

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

要想知道使用哪条产生规则，我们不能只看第一个标记，而需要知道这个表达式中是否有`+`或`-`操作。如果我们确定这个表达式是一个求和（sum）或求差（difference），我们就会永远递归地调用`parse_expression`函数。为了不这样做，我们需要找到表达式末尾的最后一个`<term>`，解析并删除它，然后再回过头来解析剩下的内容。这两个问题（找出使用哪条生产式，以及解析最后一个`term`）都需要我们向前看一个任意数量的标记，直到找到表达式的结尾。你也许能让这种方法发挥作用--如果有类似的现有解析算法--它应该也会很复杂低效，而且不会是一个递归下降解析器。所以我们不打算这么做。

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

### 递归下降解析


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

### 语法定义

这里是本次lab的完整语法，包括上面的新东西（表达式--expressions、项--terms、因子--factors）和从上次lab开始没变的东西（函数--functions、语句--statements等）：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int>
```

### AST节点定义

下面是我们AST节点的最新定义集合；只有`exp`的定义发生了变化。

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

请注意，我们现在在AST定义中区分了二元和一元运算符。例如，取负一元运算符的`-`和减二元运算符的`-`在我们的AST中是不同的类型（type）。
