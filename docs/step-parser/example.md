# parser stage 实验指导

下面我们介绍parser实验框架中的一些函数，来帮助大家更好地理解实验框架。

注意**我们的框架并不完全是LL(1)文法的下降分析**, 在有些地方会通过while循环来解析多个连续的、左结合的表达式, 相当于使用了等价的EBNF来解析。详见下文关于`p_multiplicative`函数的介绍。 

### 1. lookahead

C++中: `Token lookahead(TokenType t)` 

python中: `def lookahead(self, type: Optional[str] = None) -> Any:`

词法分析器lex将程序字符串转换为一串token, C++框架用`yylex()`获取词法分析器提供的下一个token, python框架用`next(self.lexer)`获取词法分析器提供的下一个token.

为了实现递归下降语法分析中的"lookahead"机制, 我们用一个变量`next_token`(C++: 全局变量next_token, python: Parser.next_token)暂存将要被解析的下一个Token: 通过判断`next_token`的类型, 来判断将要使用哪一条产生式。
而lookahead()函数，则表示希望读取一个特定类型的token(如果传入了一个token类型做参数) / 希望读取一个token(如果没有传入一个token类型作为参数)。每次执行这个函数，都会消耗当前的next_token并从词法分析器获得新的token赋值给next_token变量。

注意直接访问next_token变量和执行lookahead()函数的区别：在于是否消耗一个token并向词法分析器请求下一个token.

### 2. First/Follow

某个产生式的First集合，表示的是可能作为该产生式中第一个Token出现的Token集合。
某个产生式的Follow集合，表示的是可能作为该产生式之后第一个Token出现的Token集合。

在我们的框架里，因为语法非常简单，这两个集合用到的地方不多，更多的是直接用if语句来判断。(相当于通过if语句把First/Follow集合写出来了)

C++框架里定义的isFirst数组和isFollow数组, 表示的是左端为某个非终结符的所有产生式的First集合的总和。

例如, `isFirst[SymbolType::Binary][TokenType::IDENTIFIER]`表示的是左侧为`Binary`的所有产生式中，能否产生第一个Token为`IDENTIFIER`的token序列。如果能，`isFirst` 数组这个位置的数值就为true。

**TODO: python框架中的first follow集合**

### 3. p_Multiplicative

C++的 p_Multiplicative()函数 和 python中的 p_multiplicative()函数, 都希望从当前的token stream中, 解析出一个 `multiplicative`表达式并返回其语法树节点. 

`multiplicative`对应的语法为:

```
multiplicative : multiplicative '*' unary
                   | multiplicative '/' unary
                   | multiplicative '%' unary
                   | unary  
```

我们将其转换为EBNF的形式便于编写程序解析: `multiplicative : unary { '*' unary | '/' unary | '%' unary } `

注意到产生式的开头总有一个`Unary`节点, 所以我们先进行`p_Unary()`获取一个`Unary`节点, 如果通过`next_token`检查到后续节点不属于`+` `/` `%`, 就可以直接返回这个`Unary`节点。否则，通过lookahead()读取掉运算符(+ / %), 接下来按照左结合的方法，循环解析更多的`Unary`节点, 构建Multiplicative的语法树节点。

考虑这个函数如何处理连乘积1*2*3*(4+5)*x：

递归解析出 1 对应的Unary节点, 然后进入while循环，

while循环第一轮: lookahead消耗掉*, 递归解析出2对应的节点, 然后构建 1*2 这个乘法表达式节点.

while循环第二轮: lookahead消耗掉*, 递归解析出3对应的节点, 然后构建 (1*2) * 3 这个乘法表达式节点.

......(以此类推)


### 需要填写的函数

实验框架中标记有`TODO`的函数需要我们填写。填写正确后，合并stage2的中端、后端，应当通过step1-6的测例。

C++需要填写的函数:
p_Type  p_StmtList  p_Statement p_VarDecl  p_Return p_If  
p_Expression  p_Assignment p_LogicalAnd p_Relational

python:
**TODO: python需要填写的函数**

### 思考题

1.
```
additive : additive '+' multiplicative
                 | additive '-' multiplicative
                 | multiplicative  
```

将additive的这三条产生式转换为LL(1)语法。（不考虑后续multiplicative的产生式）

2. 对于我们的程序框架，自顶向下语法分析的过程中, 如果出现一个语法错误，可以进行"错误恢复"以继续解析，从而能够解析出一个程序中多个语法错误。
请尝试举出一个出错程序的例子，结合我们的程序框架，描述你心目中的"错误恢复机制"对这个例子，怎样越过出错的位置继续解析。
注意目前框架里是没有"错误恢复机制"的。

3(选做,不计分). 指出你认为的本阶段的实验框架/实验设计的可取之处、不足之处、或可改进的地方。