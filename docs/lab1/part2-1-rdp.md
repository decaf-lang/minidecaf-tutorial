### 递归下降解析

为了将一个标记列表转化为AST，我们将使用一种叫做递归下降解析的技术。我们将定义一个函数来解析语法中的每个非终结符，并返回一个相应的AST节点。解析符号*S*的函数应该从列表的开头删除标记，直到它到达*S*的有效派生。如果在它完成解析之前，碰到了一个不在*S*的产生式中的标记，它应该失败。如果 *S* 的产生式规则包含其他非终结符，它应该调用其他函数来解析它们。

下面是解析语句的伪代码。

```
def parse_statement(tokens):
    tok = tokens.next()
    if tok.type != "RETURN_KEYWORD":
        fail()
    tok = tokens.next()
    if tok.type != "INT"
        fail()
    exp = parse_exp(tokens) //parse_exp will pop off more tokens
    statement = Return(exp)

    tok = tokens.next()
    if tok.type != "SEMICOLON":
        fail()

    return statement
```

后面可以发现，产生式是递归的（例如一个算术表达式可以包含其他表达式），这意味着解析函数也将是递归的--因此这种技术被称为递归下降解析。