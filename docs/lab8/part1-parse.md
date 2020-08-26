# 词法语法解析

### `while` 语句

为 `<statement>` 新增如下产生式：

```
<statement> ::= ...  // 已有的其他产生式
              | "while" "(" <exp> ")" <statement>
```

其中 `"while"` 是新的标记，应在词法分析器中实现。

新增如下 AST 结点：

```
statement = ...  // 已有的其他结点
          | While(expression, statement)
```

其中 `expression` 和 `statement` 分别为循环条件和循环体。

### `do while` 语句

为 `<statement>` 新增如下产生式：

```
<statement> ::= ...  // 已有的其他产生式
              | "do" <statement> "while" "(" <exp> ")" ";"
```

其中 `"do"` 是新的标记，应在词法分析器中实现。

新增如下 AST 结点：

```
statement = ...  // 已有的其他结点
          | Do(statement, expression)
```

其中 `expression` 和 `statement` 分别为循环条件和循环体。

###  `for` 语句

相对于 `while` 语句和 `do while` 语句，`for` 语句较为复杂。`for` 语句可能有如下变种：

- `for` 的第一个分号前，可能是语句，也可能是循环变量的定义；
- `for` 的初始化语句、循环条件和自增语句均可以为空。

为此，我们按如下方式设计文法：

```
<statement> ::= ...  // 已有的其他产生式
              | "for" "(" <exp-option-semicolon> <exp-option-semicolon> <exp-option-close-paren> <statement>
              | "for" "(" <declaration> <exp-option-semicolon> <exp-option-close-paren> <statement>
<exp-option-semicolon> ::= <exp> ";" | ";"
<exp-option-close-paren> ::= <exp> ")" | ")"
```

其中 `"for"` 是新的标记，应在词法分析器中实现。

当然，这只是能解析 `for` 语句的其中一种文法。你也可以设计一个标记表示“表达式或空”，以替换 `<exp-option-semicolon>` 和 `<exp-option-close-paren>`，或是按你喜欢的其他方式设计。

解析器应生成如下  AST 结点：

```
statement = ...  // 已有的其他结点
          | For(exp option, exp option, exp option, statement)
          | ForDecl(declaration, exp option, exp option, statement)
```

其中 `For` 和 `ForDecl` 分别表示在 `for` 语句中使用初始化语句和定义循环变量的两种情况。AST 结点的各个参数分别表示初始化语句/循环变量定义、循环条件、自增语句和循环体。如果你在第6步选择将 `Declaration` 作为一种 `statment`，那么只需添加 `For` 结点即可，而不必添加 `ForDecl` 结点。按这种方式，你可能需要在后续步骤中区分这两种 `for` 语句。

带 `option` 标记的表示该项是可选的。你也可以选择不在 AST 结点中设计可选参数，而是构造一个常量 `1` 结点代替空的循环条件、构造一个空语句块结点代替空的初始化或自增语句。

### 空语句

在本步骤中，我们还要引入空语句。你可以利用上述 `for` 语句产生式中的 `<exp-option-semicolon>`，例如：

```
<statement> ::= ...  // 已有的其他产生式
              | <exp-option-semicolon> // null statement
```

也可以设计单独的空语句产生式。

对于 AST，你既可以使用空的语句块结点表示空语句，也可以加入专门表示空语句的结点，还可以干脆不用任何结点表示空语句。

### `break` 和 `continue` 语句

为 `<statement>` 新增如下产生式：

```
<statement> ::= ...  // 已有的其他产生式
              | "break" ";"
              | "continue" ";"
```

其中 `"break"` 和 `"continue"` 均是新的标记，应在词法分析器中实现。

新增如下 AST 结点：

```
statement = ...  // 已有的其他结点
          | Break
          | Continue
```

值得注意的是，如果程序中存在位于循环体外部的 `break` 或 `continue`，上述文法并不会报错。你需要在后续步骤中进行验证，也可以改进文法，在语法解析阶段就识别此类错误。