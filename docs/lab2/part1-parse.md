# 词法语法解析

## 词法解析

在本实验中，我们将增加三个一元运算符（unary operators，即只对一个值操作的运算符）：**取负(`-`)**：**按位取反(`~`)**、**逻辑否（`！`）**。我们只需要将这些操作符分别添加到我们的标记列表中。添加后的标记列表如下所示：

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

## 语法解析

现在，一个表达式可以有两种形式之一。它可以是一个常量，或者是一个一元运算。一元运算由运算符（如`~`）和操作数组成，操作数本身就是一个表达式。例如，以下是我们如何构造表达式`~3`。

```
c = Const(3)
exp = UnOp(COMPLEMENT, c)
```

我们对表达式的定义是递归的，表达式可以包含其他的表达式。因此，我们的语法需要更新。

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <unary_op> <exp> | <int>      // <- 看这里
<unary_op> ::= "!" | "~" | "-"          // <- 看这里
```

在AST中，我们将增加另一种类型的表达式，一元运算（unary operations）。下面是对AST节点的定义，只有`exp`的定义有变化。

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = UnOp(operator, exp) | Constant(int)       // <- 看这里
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

