# parser-stage 框架介绍

下面我们介绍 parser-stage 实验框架中的一些函数，来帮助大家更好地理解实验框架。

注意**我们的框架并不完全是课堂讲授的基于 LL(1) 文法的递归下降分析方法**，在有些地方会通过 while 循环来解析多个连续的、左结合的表达式，对应于等价的拓展巴克斯范式（EBNF）文法。详见下文关于 `p_multiplicative` 函数的介绍。

## 框架接口

### lookahead 函数

C++ 框架：`Token lookahead(TokenType t)` 

Python 框架：`def lookahead(self, type: Optional[str] = None) -> Any`

词法分析器 lex 将程序字符串转换为一串 token，C++ 框架用 `yylex()` 获取词法分析器提供的下一个 token，python 框架用 `next(lexer)` 获取词法分析器提供的下一个 token。

为了实现递归下降语法分析中的 "lookahead" 机制，我们需要**看下一个 token 是什么，但却不能消耗这个 token**，为此我们用一个变量 `next_token` （C++ 框架：全局变量 next_token，python 框架：Parser.next_token）暂存将要被解析的下一个 token。通过判断 `next_token` 的类型，来判断将要使用哪一条产生式。

而 `lookahead()` 函数有两个重载的版本。一个版本不带参数，直接读取一个 token；
另一个版本传入了一个 token 类型做参数，表示希望读取一个特定类型的 token，如果类型不符则报错。每次执行 `lookahead()` 函数，都会**消耗**当前的 `next_token` 并从词法分析器获得新的 token 赋值给 `next_token` 变量。

注意直接访问 `next_token` 变量和执行 `lookahead()` 函数的区别在于：是否消耗一个 token 并向词法分析器请求下一个 token。`next_token` 变量不会消耗，而 `lookahead()` 函数则会消耗一个 token。

### First/Follow

某个产生式的 First 集合，包括可能在该产生式右端第一个出现的所有 token。如果该产生式可以产生空串，则该 First 集合也包含空串。

某个非终结符的 Follow 集合，包括可能紧跟出现在该非终结符之后 token。

在我们的框架里，因为语法非常简单，所以没有进一步计算 PS 预测集合，而是直接用 if 语句结合 First/Follow 集合直接进行判断（用 if 语句枚举判断输入的 token 是否属于集合中的元素）。

C++ 框架里定义的 isFirst 数组和 isFollow 数组，表示的是左端为某个非终结符的所有产生式的 First 集合的总和。例如，`isFirst[SymbolType::Binary][TokenType::IDENTIFIER]` 表示的是左侧为 `Binary` （产生式左端的非终结符）对应的所有产生式中，能否产生第一个 token 为 `IDENTIFIER` 的 token 序列。如果能，`isFirst` 数组对应元素的值则为 true，否则为 false。如果同学们在实现中需要用到 isFirst 数组和 isFollow 数组，需要自行补充完整数组的内容。

Python 框架中通过**装饰器模式**（decorator pattern）定义了每个产生式左端非终结符的 First 集合，例如 `p_declaration` 函数开头的 `@first("Int")` 表示 `declaration` 的 First 集只包含 token `'Int'`。Python 框架里没有显式定义 Follow 集合。事实上，需要同学们完善的部分里并不需要用到 First/Follow 集合，直接使用 if 语句判断即可。

### p_Multiplicative

我们使用 C++ 框架的 `p_Multiplicative()` 函数和 Python 框架中的 `p_multiplicative()` 函数介绍框架里是如何使用与语法规范等价的 EBNF 文法及其解析方法。这两个函数都希望从当前的 token 流中，解析出一个 `multiplicative` 表达式，并返回其语法树结点。

`multiplicative` 对应的语法为：

```
multiplicative : multiplicative '*' unary
                   | multiplicative '/' unary
                   | multiplicative '%' unary
                   | unary  
```

容易发现，这个产生式是左递归的，不适合基于 LL(1) 的递归下降 分析器直接处理。我们将其转换为 EBNF 的形式进行程序解析：`multiplicative : unary { '*' unary | '/' unary | '%' unary }` 其中，EBNF 中的大括号表示重复零次或任意多次。

注意到产生式的开头总有一个 `Unary` 非终结符，所以我们递归调用 `p_Unary()` 函数解析对应的 `Unary` 非终结符，如果通过 `next_token` 检查到后续符号不属于 `*`、`/` 或 `%`，就可以直接返回创建并返回 `Unary` AST结点。否则，通过 `lookahead()` 读取掉运算符 `(* / %)`，并按照左结合的方法，循环解析更多的 `Unary` 非终结符。最终完成 Multiplicative 对应 AST 结点的构建。

例如，让我们考虑这个函数如何处理连乘积 `1*2*3*(4+5)*x`：

递归解析出 `1` 对应的 `Unary` AST 结点，然后进入 `while` 循环：

while 循环第一轮: `lookahead` 消耗掉 `*`，递归解析出 `2` 对应的 AST 结点，然后构建 `1*2` 这个乘法表达式对应的 AST 结点；

while 循环第二轮: `lookahead` 消耗掉 `*`，递归解析出 `3` 对应的 AST 结点，然后构建 `1*2*3` 这个乘法表达式对应的 AST 结点；

……（以此类推）

直到处理完 `x` 后，发现下一个 token 不是 `*`，那么当前 `multiplicative` 非终结符对应的文法 parse 结束，并返回 AST 结点。

最后得到的 AST 为：
```
binary(*) [
    binary(*) [
        binary(*) [
            binary(*) [
                int(1)
                int(2)
            ]
            int(3)
        ]
        binary(+) [
            int(4)
            int(5)
        ]
    ]
    identifier(x)
]
```


### 需要填写的函数

实验框架中标记有 `TODO` 的函数需要我们填写。填写正确后，合并 stage2 的中端、后端，要求**通过 step1-6 的测例**。

C++ 框架需要完成的函数：
```
p_Type p_StmtList p_Statement p_VarDecl p_Return p_If
p_Expression  p_Assignment p_LogicalAnd p_Relational
```

Python 框架需要完成的函数：
```
p_relational p_logical_and p_assignment p_expression p_statement
p_declaration p_block p_if p_return p_type 
```


# 思考题

1. 在框架里我们使用 EBNF 处理了 `additive` 的产生式。请使用课上学习的消除左递归、消除左公因子的方法，将其转换为不含左递归的 LL(1) 文法。（不考虑后续 multiplicative 的产生式）
```
additive : additive '+' multiplicative
             | additive '-' multiplicative
             | multiplicative  
```

2. 对于我们的程序框架，在自顶向下语法分析的过程中，如果出现一个语法错误，可以进行**错误恢复**以继续解析，从而继续解析程序中后续的语法单元。
请尝试举出一个出错程序的例子，结合我们的程序框架，描述你心目中的错误恢复机制对这个例子，怎样越过出错的位置继续解析。（注意目前框架里是没有错误恢复机制的。）

3. （选做，不计分）指出你认为的本阶段的实验框架/实验设计的可取之处、不足之处、或可改进的地方。
