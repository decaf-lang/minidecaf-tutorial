# 词法语法解析

本步骤对词法/语法解析的变更较为简单。语句块可以视为语句的一种，就像括号表达式可以视为表达式的一种一样。

据此，文法做如下修改：

```
<block-item> ::= <statement> | <declaration>
<declaration> ::= "int" Identifier [ "=" <exp> ] ";"
<statement> ::= ...  // 已有的其他产生式
              | "{" { <block-item> } "}  // <- 看这里
```

你可能需要加入其他标记与产生式以识别 `{ <block-item> }`。

要生成的 AST 做如下修改：

```
statement = ...  // 已有的其他结点
          | Compound(block_item list)
```

