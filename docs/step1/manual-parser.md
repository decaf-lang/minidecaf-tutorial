## 手写 parser 简单实例

该文档简单展示使用 c 风格代码手写 parser 的过程。

### 0. 定义

我们的最终目标是这样一个函数，接受 token list 作为输入，输出一个代表整个程序结构的 AST。

```
parse(token_list) -> Prog
```

但是在 lab9 之前我们都只有一个 main 函数，所以这里的 `Prog` 可以暂时简化为 `Function`。

首先我们先定义 token 和 AST node

```c++
enum TokenKind {
    TK_RESERVED, // 保留字，包含关键字和各种符号
    TK_IDENT,    // 标识符，如变量名、函数名
    TK_NUM,      // 数字字面量，如 1, 0
};

struct Token {
    TokenKind kind;
    char* str;			//对应的字符串
    // int raw, col;	//如果你想得到报错位置，需要在这里记录行号与列号信息
};
```

```c++
struct Prog {
    Function* func;
}

struct Func {
   	list<Node*> stmts;
}

enum NodeKind{
    ND_RETURN,      // return 语句
    ND_NUM,         // 数值字面量
};

struct Node {
    NodeKind kind;
    int val;		// 用于储存 ND_NUM 类型节点的数值
    Node* expr;		// 用来储存 ND_RETURN 类型节点返回的表达式节点
};
```

statement 和 expression 两类节点有较大的区别，推荐区分为不同的两类 `Node`，这里未作区分，也不会有什么问题。

推荐使用 unique pointer 和 shared pointer 来构建 AST 树。

### 1. 访问 Token

在 lex 阶段，我们的到了一个 token list，在 parse 阶段，我们需要访问这个 list 构建 AST ，我们需要一套访问接口来方便操作。

```c++
// 获得当前正在处理的 token，处理完毕返回 NULL
Token* take_token();
// 进入下一个 token 的处理
void next_token();
```

这一步实现简单，甚至不一定要抽象为一个函数，请大家自行实现。

### 2. 框架

解析的过程是对产生式的还原。

```
program
    : function

function
    : type Identifier '(' ')' '{' statement '}'

type
    : 'int'

statement
    : 'return' expression ';'

expression
    : Integer
```

最上层函数为解析一个 `Prog`，目前相当与解析一个函数。

```c++
Program* parse() {
    Program* prog = new Program();
    Function *fn = function();
    prog->func = fn;
    return prog;
}
```

###　非终结符解析函数

`parse()`中，`function()`函数代表解析一个非终结符 function，即：从当前的 token 开始，消耗若干个 token，直到解析完成一个function（一个非终极符）。该函数没有输入，返回一个 AST 结点，过程中消耗了 token。接下来本文中类似函数（名称与产生式中非终结符一致）都是类似的含义。

按照生成式，解析一个 `function` 需要依次解析 `type` `Identifier` `(` `）` `{` `statement` `}`，如下：

```c++
Function *function() {
    parse_reserved("int"); 	// 应该为 type(), 这里做了简化
    char *name;
    parse_ident(name);
    Function *fn = new Function(name);
    parse_reserved("(");
    parse_reserved(")");
    parse_reserved("{");
    while (!parse_reserved("}")) {
        fn->nodes.push_back(stmt());
    }
    return fn;
}
```

其中 `parser_xxx()`代表解析一个终结符。为直接访问 token 的函数，仅仅处理一个 token，与 token 类别一一对应。正如上方的说明，`stmt()` 表示，消耗一系列 token，解析出一条语句。

对非终极符的解析函数是由其他的非终结符函数、终结符函数和处理AST节点的语句构成，如果你同时完成了名称解析或者类型检查等，你还需要其他功能语句。

#### 终结符解析函数：parser_xxx()

```c++
// 解析成功返回 true, 否则为 false
bool parse_int_literal(int &val); 		// 解析一个数字字面量，结果通过 val 返回
bool parse_reserved(const char* str);   // 解析一个保留字 str
bool parse_ident(char* &ident);			// 解析一个标识符，结果通过 ident 返回
```

这些底层的解析函数会处理当前的 token（通过 `take_token()`）拿到，如果成功会跳过当前 token（也就是调用 `next_token()`）。

如 `parse_reserved()` 会检查当前 token 的类型是否为 `TK_RESERVED`，如果是，检查其字符串是否与给出的一致,如果是，返回 true。以上任意一步失败，返回 false。

如果你想要自己的编译器在发生错误时停止，可以这样。

````c++
Function *function() {
    assert(parse_reserved("int"));
    // ...
}
````

当然，也可以输出一些错误信息。如果你想得到报错位置，可以令 `parse_xxx()`返回 token 位置信息。

##### stmt()

类似 `function()`的思路，对语句的解析也可以按照生成式进行，目前仅需要解析 return 一种类型的语句。

```c++
Node* stmt() {
    Node* node = NULL;
    if (parse_reserved("return")) {   
        node = new Node(ND_RETURN);
        node->expr = expr();
        assert(parse_reserved(";"));
        return node;
    }
    return node;
}
```

其中, `expr()`为解析一个表达式的函数，因为目前的 `expr()`仅仅需要解析一个数字，可以通过调用 `parse_int_lliteral()`轻松实现。返回一个类型为 `ND_NUM`的`Node`就好了。

### 总结

第一个 lab 的工作看似很简单，但是我们需要搭建一个比较完整的框架来便于后续工作，其实工作量较大。接下来工作会比较轻松。



  

