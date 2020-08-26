# 词法语法解析

## 词法解析

在本实验中，将添加一些布尔运算符（`&&`，`||`）和一大堆关系运算符（`<`，`==`，等）。由于我们已经知道如何处理二元运算符，所以本次试验将非常简单。我们将增加8个新的操作符：

- 逻辑与：Logical AND `&&`
- 逻辑或：Logical OR `||`
- 等于：Equal to `==`
- 不等于：Not equal to `!=`
- 小于：Less than `<`
- 小于或等于：Less than or equal to `<=`
- 大于：Greater than `>`
- 大于或等于：Greater than or equal to `>=`
  
我们修改标记列表以支持新的运算符，新的标记列表如下所示:

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

## 语法解析

在上个实验的语法中，每一个操作符的优先级都需要一个产生式。

下面是我们所有的二进制运算符，从最高到最低的优先级：

- Multiplication & division (`*`, `/`)
- Addition & subtraction (`+`,`-`)
- Relational less than/greater than/less than or equal/greater than or equal (`<`, `>`,`<=`,`>=`)
- Relational equal/not equal (`==`, `!=`)
- Logical AND (`&&`)
- Logical OR (`||`)

我们在上个实验中处理了前两个优先级，最后四个优先级是新的。我们将为最后四个优先级各增加一条产生规则。新的语法如下，修改/增加的规则用黑体表示。

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

这里给出语法解析的AST定义：

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = BinOp(binary_operator, exp, exp) 
    | UnOp(unary_operator, exp) 
    | Constant(int)
```

这与上次lab的AST定义相同，只是我们增加了更多可能的`binary_operator`值。
