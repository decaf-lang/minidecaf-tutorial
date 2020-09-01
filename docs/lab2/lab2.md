
# lab2：一元运算符


在上一个实验中，我们学习了如何编译返回整数的程序。本次实验我们将对这些整数进行数学运算。你可以找到相应的[lab2测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step2)。

我们将增加三个一元运算符（unary operators，即只对一个值操作的运算符）。

**取负(`-`)**：

`-5 = 0 - 5`. 换句话说，这是一个普通的负数。

**按位取反(`~`)**：

这将翻转数字中的每一个位。例如，在二进制中，4被写成100。

- 4在二进制中被写成`100`
- `100的`按位取补是`011`
- `011`在十进制中是3
- 所以`~4=3`

**逻辑否（`！`）**：

布尔运算符 "not"。将`0`视为`"false"`，而将所有其他值视为 `"true"`。

- `!0 = 1`
- `(anything else) = 0`

在lab1中，我们创建了一个包含三个阶段的编译器：一个词法分析器、一个语法解析器和一个代码生成器。现在我们将更新每个阶段来处理这些新的运算符。

## 词法分析

我们只需要将这些操作符分别添加到我们的标记列表中。下面是标记列表：上周的标记在顶部，新的标记在底部加粗。

- Open brace `{`
- Close brace `}`
- Open parenthesis `\(`
- Close parenthesis `\)`
- Semicolon `;`
- Int keyword `int`
- Return keyword `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`
- **Negation `-`**
- **Bitwise complement `~`**
- **Logical negation `!`**

我们可以像处理其他单字符标记一样，以完全相同的方式处理这些新的标记，比如大括号和圆括号。

#### ☑任务

更新*lex*函数来处理新的标记。它应该适用于测试集中所有step1和step2的例子。

## 语法解析

上周我们定义了几个AST节点，包括表达式（expressions）。我们只定义了一种类型的表达式：常量（constants）。本周，我们将增加另一种类型的表达式，一元运算（unary operations）。最新的一组定义如下。只有`exp`的定义有变化。

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = UnOp(operator, exp) | Constant(int)
```

现在，一个表达式可以有两种形式之一--它可以是一个常量，或者是一个一元运算。一元运算由运算符（如`~`）和操作数组成，操作数本身就是一个表达式。例如，以下是我们如何构造表达式`~3`。

```
c = Const(3)
exp = UnOp(COMPLEMENT, c)
```

我们对表达式的定义是递归的--表达式可以包含其他的表达式!

这是一个表达式：`！3`。

这也是一个表达式：`!~-4`

这个也是：`!!!!!!!-~~-!3`

我们的语法也需要更新。

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <unary_op> <exp> | <int>
<unary_op> ::= "!" | "~" | "-"
```

因为表达式的定义是递归的，所以解析表达式的函数也应该是递归的。下面是解析一个表达式的伪代码：

```
def parse_expression(tokens):
    tok = tokens.next()
    if tok.type == "INT":
        //parse this the same way as before, return a Const node
    else:
        op = get_operator(tok) //convert token to unary_op AST element - fail if token isn't "!", "~" or "-"
        inner_exp  = parse_expression(tokens) //HOORAY, RECURSION - this will pop more tokens off the stack
        return UnOp(op, inner_exp)
```

#### ☑ 任务：更新你的表达式解析函数以处理一元运算

更新你的表达式解析（expression-parsing）函数，以处理一元运算。它应该成功解析测试集中所有有效的step1和step2的例子。

## 代码生成

取负和位补是超级简单的，每一个都可以用一条汇编指令来完成。

`neg`取负操作数的值。下面是一个例子。

```
    movl    $3, %eax    ;EAX register contains 3
    neg     %eax        ;now EAX register contains -3
```

当然，我们在对它取负之前需要计算一个值，所以我们需要递归生成内部表达式的代码，然后发出`neg`指令。

`not`用它的按位取反来替换一个值。我们可以用和`neg`完全一样的方式来使用它。

逻辑上的否定是比较复杂的。记住，`return !exp`相当于：

```
if (exp == 0) {
    return 1;
} else {
    return 0;
}
```

逻辑否操作与其他操作不同，其他操作都是直接的位操作，但逻辑否需要一些条件逻辑。我们可以使用`cmpl`[4](https://norasandler.com/2017/12/05/Write-a-Compiler-2.html#fn4)来实现它，它比较两个值和`sete`("set if equal")。`sete`如果上次比较的结果相等，则将其操作数设为1，否则为0。

像`cmpl`和`sete`这样的比较和条件指令有点奇怪；`cmpl`并没有明确地存储比较的结果，而`sete`并没有明确地提到这个结果，或者被比较的值。这两条指令--以及所有的比较和条件指令--都隐含地引用FLAGS寄存器。顾名思义，这个寄存器的内容被解释为一个一比特标志的数组，而不是一个单一的整数。这些标志在每次算术操作后都会自动设置。我们现在唯一关心的标志是零标志(ZF)，如果运算结果为0，它就会被设置为开启，否则就会被关闭。

`cmpl a，b`计算(b - a)，并相应设置flags。如果两个值相等，它们的差值为0，所以只有当`cmpl`的操作数相等时，ZF才会被置位。`sete`指令使用ZF来测试是否相等；如果ZF开启，则将其操作数设置为1，如果ZF关闭，则设置为0。事实上，`setz`("set if zero")是同一指令的另一个符号。

这里最后一个小窍门是，`sete`只能设置一个字节，而不是整个字。我们要让它设置AL寄存器，而AL寄存器只是EAX中最不重要的字节。我们只需要先将EAX清零；由于`！`的结果总是0或1，所以我们不想留下任何多余的高位设置。

虽然上面的解释很长，但实际上你只需要三行汇编就可以实现`！`。

```
    <CODE FOR exp GOES HERE>
    cmpl   $0, %eax    ;set ZF on if exp == 0, set it off otherwise
    movl   $0, %eax    ;zero out EAX (doesn't change FLAGS)
    sete   %al         ;set AL register (the lower byte of EAX) to 1 iff ZF is on
```

为了让自己相信这是正确的，我们用`！5`的表达方式来解决这个问题：

1. 首先我们把5移到EAX寄存器中
2. 我们将0和5进行比较，5 !=0，所以ZF标志被设置为0
3. EAX寄存器被清零，所以我们可以在下一步设置它
4. 我们有条件地设置AL；因为ZF为0，所以我们将AL设置为0.AL指的是EAX的下位字节；上位字节在第3步中也被清零，所以现在EAX包含0

#### ☑ 任务

更新你的代码生成（code-generation）阶段，为`！`、`~`和`-`操作生成正确的汇编代码。它应该为所有step1和step2示例生成正确的汇编。

## 下一步

下一个lab将增加一些二进制运算：加法、减法等，找出2+2是否真的等于4。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
