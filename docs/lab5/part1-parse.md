# 词法语法解析

### 支持多条语句

从本步骤开始，函数中可能具有多条语句，而不再只有一个返回语句。相关符号的定义变更为：

```
<function> ::= "int" "main" "(" ")" "{" { <statement> } "}"
<statement> ::= "return" <exp> ";"
              | <exp> ";"
```

文法中的 `{ <statement> }` 记号表示 `<statement>` 可重复 0 至任意多次。在语法解析器的实际实现中，也可将上述文法写作：

```
<function> ::= "int" "main" "(" ")" "{" <statements> "}"
<statements> ::= /* empty */
               | <statements> <statement>
```

如果你选择自己亲自实现一个语法解析器，建议使用后一种文法以简化实现。如果你使用了 antlr 等解析器生成工具，可以尝试直接编写前一种文法，但并不一定比后一种文法更方便。请根据实际情况做出选择。

### 标识符

在之前的步骤中，唯一的标识符——主函数名 `main` 是固定的。为了简洁起见，我们将 `main` 视为一个关键字，硬编码在词法和语法解析器中。但从本步骤开始，局部变量的名称将是不定的，故需要引入一个专门表示标识符的标记 `Identifier`，定义如下：

```
Identifier [a-zA-Z_][a-zA-Z0-9_]*
```

而函数符号的定义则进一步变更为：

```
<function> ::= "int" Identifier "(" ")" "{" { <statement> } "}"
```

### 局部变量的定义

语句符号的定义做如下进一步修改，将支持局部变量的定义和初始化视作一种语句：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "int" Identifier [ "=" <exp>] ";"  // <- 看这里
```

其中 `[ = <exp>]` 表示初始化表达式是可选的。根据你实现解析器的方式，也可以将上述文法改写成：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "int" Identifier ";"
              | "int" Identifier "=" <exp> ";"
```

解析器应生成相应的 AST 结点：

```
statement = Return(exp)
          | Declare(string, exp option)  // <- 看这里
          | Exp(exp)
```

其中 `string` 表示变量名，而 `exp` 是一个可选参数，表示变量的初始化表达式。

### 局部变量的访问和赋值

表达式符号做如下修改：

```
<exp> ::= Identifier "=" <exp> | <logical-or-exp>  // <- 看这里
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
<logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
<equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
<relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
<additive-exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | Integer | Identifier  // <- 看这里
<unary_op> ::= "!" | "~" | "-"
```

当 `<factor>` 是一个 `Identifier` 时，表示访问一个变量。当 `<exp>` 是 `Identifier "=" <exp>` 时，表示对变量赋值。

最后，解析器应生成相应的 AST 结点：

```
exp = Assign(string, exp)  // <- 看这里
    | Var(string)  // <- 看这里
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

其中 `string` 表示变量名。
