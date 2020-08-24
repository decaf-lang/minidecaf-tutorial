# 词法语法解析

### 分支语句

本步骤对语句的定义做如下修改：

```
<function> ::= "int" Identifier "(" ")" "{" { <block-item> } "}"
<block-item> ::= <statement> | <declaration>
<declaration> ::= "int" Identifier [ "=" <exp> ] ";"
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]
```

最主要的变更是引入了分支语句作为一种 `<statement>`，其中的 `"if"` 和 `"else"` 是新的关键字，应在词法分析器中实现。

值得注意的是：上一步骤中的 `<statement>` 被拆分成了 `<statement>` 和 `<declaration>` 两个符号，局部变量的定义不再是一种 `<statement>` 了。而 `<statement>` 和 `<declaration>` 都是 `<block-item>`。考虑如下例子，你就能明白这一变动的原因。

```c
if (1)
    x = x + 1;
```

这是合法的，`x = x + 1` 是一个  `<statement>`。

```c
if (1)
    int x;
```

这是不合法的，`int x` 是一个 `<declaration>`。

语法解析器应生成相应的 AST 结点：

```
statement = ...  // 已有的其他结点
          | Conditional(exp, statement, statement option)
```

其中 `Conditional` 结点表示分支语句，其三个参数分别为分支条件、then 语句和 else 语句，其中 else 语句是可选的。

根据你的喜好，你也可以选择不在 `Conditional` 结点里实现可选的 `else` 参数，而是构造一个表示空语句的结点（或者使用下一步要引入的空语句块）来表示缺少 `else` 分支的情况。

你可以让 `Declaration` 结点不再属于一种 `statement`，以和文法保持一致，也可以不做此项修改。

### 分支表达式

本步骤对表达式的定义做如下修改：

```
<exp> ::= Identifier "=" <exp> | <conditional-exp>
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]  // <- 看这里
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
<logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
<equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
<relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
<additive-exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | Integer | Identifier
<unary_op> ::= "!" | "~" | "-"
```

此处 `<conditional-exp>` 表示 `?:` 表达式。语法解析器应生成相应的 AST 结点：

```
exp = Assign(string, exp)
    | Var(string)
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
    | CondExp(exp, exp, exp)  // <- 看这里
```

其中 `CondExp` 表示 `?:` 表达式，其三个参数分别为条件、条件成立时的值，和条件不成立时的值。