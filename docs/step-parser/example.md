# parser-stage 框架介绍

下面我们介绍 parser-stage 实验框架中的一些函数，来帮助大家更好地理解实验框架。

注意**我们的框架并不完全是 LL(1) 文法的下降分析**，在有些地方会通过 while 循环来解析多个连续的、左结合的表达式，相当于使用了等价的拓展巴克斯范式（EBNF）来解析。详见下文关于 `p_multiplicative` 函数的介绍。

## 框架接口

### lookahead 函数

C++ 框架：`Token lookahead(TokenType t)` 

Python 框架：`def lookahead(self, type: Optional[str] = None) -> Any`

词法分析器 lex 将程序字符串转换为一串 token，C++ 框架用 `yylex()` 获取词法分析器提供的下一个 token，python 框架用 `next(lexer)` 获取词法分析器提供的下一个 token。

为了实现递归下降语法分析中的 "lookahead" 机制，我们用一个变量 `next_token` （C++ 框架：全局变量 next_token，python 框架：Parser.next_token）暂存将要被解析的下一个 token。通过判断 `next_token` 的类型，来判断将要使用哪一条产生式。

而 `lookahead()` 函数，则表示希望读取一个特定类型的 token（如果传入了一个 token 类型做参数） / 希望读取一个 token（如果没有传入一个 token 类型作为参数）。每次执行这个函数，都会**消耗**当前的 `next_token` 并从词法分析器获得新的 token 赋值给 `next_token` 变量。

注意直接访问 `next_token` 变量和执行 `lookahead()` 函数的区别：在于是否消耗一个 token 并向词法分析器请求下一个 token。

### First/Follow

某个产生式的 First 集合，表示的是可能作为该产生式中第一个 token 出现的集合。

某个产生式的 Follow 集合，表示的是可能作为该产生式之后第一个 token 出现的集合。

在我们的框架里，因为语法非常简单，这两个集合用到的地方不多，更多的是直接用 if 语句来判断（相当于通过 if 语句把 First/Follow 集合直接写出来进行判断）。

C++ 框架里定义的 isFirst 数组和 isFollow 数组，表示的是左端为某个非终结符的所有产生式的 First 集合的总和。

例如，`isFirst[SymbolType::Binary][TokenType::IDENTIFIER]` 表示的是左侧为 `Binary` 的所有产生式中，能否产生第一个 token 为 `IDENTIFIER` 的 token 序列。如果能，`isFirst` 数组这个位置的数值就为 true。

Python 框架中通过装饰器模式（decorator pattern）定义了每个产生式的 First 集合，例如 `p_declaration` 函数开头的 `@first("Int")` 表示 `declaration` 的 First 集只包含 token `'Int'`。Python 框架里没有显式定义 Follow 集合。事实上，需要同学们完善的部分里并不需要用到 First/Follow 集合。

### p_Multiplicative

我们使用 C++ 框架的 `p_Multiplicative()` 函数和 Python 框架中的 `p_multiplicative()` 函数介绍框架里是如何使用与文法等价的 EBNF 进行解析的。这两个函数都希望从当前的 token 流中，解析出一个 `multiplicative` 表达式并返回其语法树节点。

`multiplicative` 对应的语法为：

```
multiplicative : multiplicative '*' unary
                   | multiplicative '/' unary
                   | multiplicative '%' unary
                   | unary  
```

容易发现，这个产生式是左递归的，不适合 LL(1) 分析器直接处理。我们将其转换为 EBNF 的形式便于编写程序解析：`multiplicative : unary { '*' unary | '/' unary | '%' unary }` 其中，EBNF 中的大括号表示重复零次或任意多次。

注意到产生式的开头总有一个 `Unary` 节点，所以我们先进行 `p_Unary()` 获取一个 `Unary` 节点，如果通过 `next_token` 检查到后续节点不属于 `*`、`/` 或 `%`，就可以直接返回这个 `Unary` 节点。否则，通过 `lookahead()` 读取掉运算符 `(* / %)`，并按照左结合的方法，循环解析更多的 `Unary` 节点，构建 Multiplicative 的 AST 节点。

例如，让我们考虑这个函数如何处理连乘积 `1*2*3*(4+5)*x`：

递归解析出 `1` 对应的 `Unary` 节点，然后进入 `while` 循环：

while 循环第一轮: `lookahead` 消耗掉 `*`，递归解析出 `2` 对应的节点，然后构建 `1*2` 这个乘法表达式节点；

while 循环第二轮: `lookahead` 消耗掉 `*`，递归解析出 `3` 对应的节点，然后构建 `1*2*3` 这个乘法表达式节点；

……（以此类推）

直到处理完 `x` 后，发现下一个 token 不是 `*`，那么当前 `multiplicative` 节点的文法 parse 结束，返回 AST 节点。


### 需要填写的函数

实验框架中标记有 `TODO` 的函数需要我们填写。填写正确后，合并 stage2 的中端、后端，应当**通过 step1-6 的测例**。

C++ 框架需要填写的函数：
```
p_Type  p_StmtList  p_Statement p_VarDecl  p_Return p_If
p_Expression  p_Assignment p_LogicalAnd p_Relational
```

Python 框架：
```
p_relational p_logical_and p_assignment p_expression p_statement
p_declaration p_block p_if p_return p_type 
```


# 思考题

1.```
additive : additive '+' multiplicative
                 | additive '-' multiplicative
                 | multiplicative  
```
在框架里我们使用 EBNF 处理了 `additive` 的产生式。请使用课上学习的方法，将其转换为不含左递归的 LL(1) 文法。（不考虑后续 multiplicative 的产生式）

2. 对于我们的程序框架，自顶向下语法分析的过程中，如果出现一个语法错误，可以进行**错误恢复**以继续解析，从而能够解析出一个程序中多个语法错误。
请尝试举出一个出错程序的例子，结合我们的程序框架，描述你心目中的错误恢复机制对这个例子，怎样越过出错的位置继续解析。（注意目前框架里是没有错误恢复机制的。）

3. （选做，不计分）指出你认为的本阶段的实验框架/实验设计的可取之处、不足之处、或可改进的地方。
