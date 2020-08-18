# 第一步 : 整数

本阶段我们将编译一个返回单个整数的minidecaf程序。我们还将建立编译器的三个基本阶段（pass）：词法、解析和代码生成。第一步将有比较大的工作量，即建立了一个编译器的框架，该框架将使以后添加更多语言特性变得容易，对后续实验步骤有较大的帮助，

下面是一个我们要编译的程序 return_2.c

```
int main() {
    return 2;
}
```

## 词法分析

词法分析器（也叫扫描器或标记器）是编译器的一个阶段，它将一个字符串（源代码）分解成一个标记（token）列表，类似于断句。一个 token 是语法解析器（parser）能够理解的最小单位，token 的本质是一个更小的字符串，但我们会在其中记录更多的信息，如标记类型、（如果是数值）对应的值。

下面是词法分析器（lexer）需要识别的所有标记，以及定义每个标记的正则表达式（regular expression）。

- Open brace `{`
- Close brace `}`
- Open parenthesis `(`
- Close parenthesis `)`
- Semicolon `;`
- Int keyword `int`
- Return keyword `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`

这些标记可以分为三类：

* 保留字： 符号和关键字，如 `{`、 `int`、 `return`
* 数值字面量：数字，如`2`
* 标识符：主要是函数名和变量名（虽然现在还用不到）， 如 `main`

#### ☑任务：

写一个*lex*函数，接受一个文件并返回一个标记列表。它应该适用于[minidecaf测试用例](https://github.com/decaf-lang/minidecaf-tests)中的所有[`step1`](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)中的示例。为了保持简单，我们只对十进制整数进行词法分析。如果你愿意尝试，你也可以扩展你的词法分析器来处理八进制和十六进制整数。

> 注意：我们不能对负整数进行词法分析。这并不是偶然的--C 语言没有负整数常量。它只是有一个负一元运算符，可以应用于正整数。我们将在下一步添加负一元运算。

#### 简单实现

词法分析可以通过自动机、正则匹配等方式进行实现，但对于简单的程序而言，实现并不需要那么复杂（可以认为是自动机或者正则匹配在简单情形下的退化）。

接下来展示`lex`函数的一种简单手工实现，首先需要确定词法分析的目标：`token`

考虑到你所使用的语言不一定可以使用 sum type，这里展示 C 风格的简单范例：

```C++
enum TokenKind {
    TK_RESERVED, // Keywords or punctuators
    TK_IDENT,    // Identifiers
    TK_NUM,      // Integer literals
};

struct Token {
	TokenKind kind,
    String str,  // Token string
	long val,    // Used for TK_NUM
};
```

`lex`函数的功能是解析输入程序字符串，得到相应的 token 列表（或者你喜欢的其他类型，如数组）。结合语法规则完成对子字符串的分类即可，核心代码简单范例（伪代码）如下。

```c++
List<Token> lex(String input_string) {
    List<Token> token_list;
    String str[] = input_string.split_at_white_space();
    for (s in str) {
        // 保留字
        if (s is a keyword or punctuator) {
            Token tok = {kind = TK_RESERVED, str = s};
            token_list.add(tok);
            continue;
        }
        // 标识符
        if (s starts with a letter) {
            Token tok = {kind = TK_IDNET, str = s};
            token_list.add(tok);
            continue;
        }
        // 数字字面量
        if (s starts with a number) {
            Token tok = {kind = TK_NUM, str = s, val = string_to_long(s)}
            token_list.add(tok);
            continue;
        }
    }
    return token_list;
}
```

当然，也可以直接对输入程序进行字符遍历，请结合所使用语言灵活实现。注意每次产生一个 token 便将该 token 加入 token 列表尾部。

## 语法解析

下一步是将我们的标记列表转化为抽象的语法树（Abstract  Syntax Tree，简称AST）。AST是表示程序结构的一种方式。在大多数编程语言中，像条件和函数声明这样的语言结构是由更简单的结构组成的，比如变量和常量。AST捕捉到了这种关系；AST的根将是整个程序，而每个节点将有子节点代表它的组成部分。让我们来看一个小例子。

```
if (a < b) {
    c = 2;
    return c;
} else {
    c = 3;
}
```

这段代码是一个if语句，所以我们将AST的根标记为 "if statement"。它有三个子节点：

- 表达式：condition (`a < b`)
- 语句列表：if body (`c = 2; return c;`)
- 语句列表：else body (`c = 3;`)

这些节点都可以进一步分解。例如，condition (`a < b`)表达式是一个有两个操作数（operand ）子节点的`"<"`二元操作的AST节点：

- first operand (variable `a`)
- second operand (variable `b`)

下面是我们对`return_2.c`给出的AST节点的定义：

```
program = Program(function_declaration)
function_declaration = Function(string, statement) // string is the function name
statement = Return(exp)
exp = Constant(int) 
```

这里是return_2.c的AST图。

- Program
  - Function (name: main)
    - body
      - return statement
        - constant (value: 2)

最后，我们需要一个形式化的语法，它定义了一系列标记如何组合成语言构造。我们将基于[Backus-Naur Form](https://en.wikipedia.org/wiki/Backus-Naur_form-Naur_form)来定义：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <int>
```

上面的每一行都是一个产生式（*production* ），定义了如何从一种形式语言（BNF）的构造和标记来建立另外一个语言（minidecaf）的构造。每一个出现在产生式左侧的符号（即`<program>`、`<function>`、`<statement>`）都是一个非终结符（non-terminal symbol）。个别标记（keywords、id、punctuation等）是终结符（terminal symbols）。这个语法告诉我们什么样的标记序列构成了一个有效的minidecaf程序。

### 递归下降解析

为了将一个标记列表转化为AST，我们将使用一种叫做递归下降解析的技术。我们将定义一个函数来解析语法中的每个非终结符，并返回一个相应的AST节点。解析符号`S`的函数应该从列表的开头删除标记，直到它到达*S*的有效派生。如果在它完成解析之前，碰到了一个不在*S*的产生式中的标记，它应该失败。如果 `S` 的产生式规则包含其他非终结符，它应该调用其他函数来解析它们。

可以发现，产生式是递归的（例如一个算术表达式可以包含其他表达式），这意味着解析函数也将是递归的--因此这种技术被称为递归下降解析。

#### ☑任务：

编写一个*parse*函数，接受一个标记列表，并返回一个AST，根节点（root node）是Program节点。该函数应该为所有有效的[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)建立正确的AST。如果你愿意，你也可以让你的解析器在遇到超过INT_MAX（整数最大值）的整数常量时优雅地失败并指出解析失败的原因。

有很多方法可以在代码中表示AST--每种类型的节点可以是它自己的类或它自己的数据类型，这取决于你用什么语言来编写编译器。例如，以下是你如何将AST节点定义为OCaml数据类型：

```
type exp = Const(int)
type statement = Return(exp)
type fun_decl = Fun(string, statement)
type prog = Prog(fun_decl)
```

#### 简单实现

接下来展示语法解析的一种C风格的简单范例。首先，需要定义解析的目标：AST 节点。

```c++
enum NodeKind{
    ND_FUNC,	   // Function
    ND_RET,        // Return statement
    ND_NUM,		   // Integer literal
};

struct Node {
    // Node kind
    NodeKind kind; 
 	// Used for ND_NUM
    long val; 
    // Used for ND_FUNC
    String name;
    List<Node> body;
    // Used for ND_RET
    Node ret_val;
};
```

目前，我们不需要考虑诸如函数返回值类型，函数参数等内容。由于目前 program 和 function 完全等价，暂时不设置 program 节点。

递归下降解析是一个自顶向下的过程，伪代码范例如下：

```c++
// 这是上一步的工作，得到一个 token list
List<Token> toks = lex(); 

Node parser() {
	return program();
}

// <program> ::= <function>
Node program() {
    return function();
}

// <function> ::= "int" <id> "(" ")" "{" <statement> "}"
Node function() {
    Node func;
    reversed("int");                // 返回 false 则报错
    func.name = ident();
    reversed("(");
    reversed(")");
    reversed("{");
    while(!reserved("}")) {
        func.body.add(statment());
    }
    return func;
}

// <statement> ::= "return" <exp> ";"
Node statement() {
    Node state;
    reversed("return");
    state.ret_val = expr();
    return state;
}

// <exp> ::= <int>
Node expr() {
    Node expr;
    expr.val = num();
    return expr;
}

// 终结符，统一处理所有保留字
bool reversed(String s) {
    Token tok = toks.pop_first();
    return tok.kind == TK_RESERVED && tok.str == s;
}

// 终结符，处理标识符
String ident() {
    Token tok = toks.pop_first();
    if tok.kind == TK_IDNET {
        return tok.str;
    }
    return NULL;
}

// 终结符，处理数字字面量 
// 该实现有误，仅供参考思路
long num() {
	Token tok = toks.pop_first();
    if tok.kind == TK_NUM {
        return tok.val;
    }
    return NULL;
}
```

语法分析的递归下降过程是不断分解非终结符的过程，直到最终分解为终结符并与 token 相对应，在此过程，我们就构建了一颗 AST 树，我们可以通过 AST 树来检查我们的递归分解是否正确。

## 代码生成

有的时候，我们需要在 AST 之后进一步生成其他的中间表示，这将方便我们的代码生成与编译优化，但这并不是必须的。该教程直接从 AST 生成 汇编代码。

首先，来看看 return_2.c 在汇编中的样子，让我们用gcc来编译它。

```
$ riscv64-unknown-elf-gcc -S -O3 return_2.c
$ cat return_2.s
	.file	"return_2.c"
	.option nopic
	.text
	.section	.text.startup,"ax",@progbits
	.align	1
	.globl	main
	.type	main, @function
main:
	li	a0,2
	ret
	.size	main, .-main
	.ident	"GCC: (GNU) 9.2.1 20190831"
	.section	.note.GNU-stack,"",@progbits
```

我们可以忽略`.section`、`.align`等指令，这些汇编原语可参加[这里的介绍](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-directives.md)。如果删除它们，仍然可以生成并运行return_2执行程序。

简化后，我们有了实际的汇编指令。

```
	.global main
main:
	li	a0, 2
	ret
```

这里最重要的一点是，当一个函数返回时，a0 寄存器将包含其返回值。`main`函数的返回值将是程序的退出代码。在上面的汇编片段中，唯一可以改变的是返回值。

现在我们已经建立了一个AST，我们已经准备好生成汇编代码了！就像我们之前看到的，我们只需生成四行汇编码。为此，我们将大致按照程序执行的顺序遍历AST。

> 注意，我们经常（虽然并不总是）以[post-order](https://en.wikipedia.org/wiki/Tree_traversal#Post-order)的方式遍历树，在其父类之前访问子类。例如，我们需要在返回语句中引用返回值之前生成它。在后面的试验中，我们需要在生成对算术表达式进行操作的代码之前，生成算术表达式的操作数。

下面是我们要生成汇编码：

1. 要生成一个函数（如函数 "foo"）。

```
    .globl foo
foo:
    <FUNCTION BODY GOES HERE>
```

2. 生成一个返回语句（如：`return 3;`）的汇编码

```
    li	a0, 3
	ret
```

为了避免寄存器分配等难题，我们将采用栈式机的风格。

// TODO 栈式机

#### ☑任务：

写一个*generate*函数，接受一个AST并生成汇编。它可以以字符串的形式在屏幕上显示汇编代码，也可以直接把汇编代码写到文件中。它应该为所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)生成正确的汇编码。

#### 简单实现

遍历 AST 树来形成汇编代码。注意往往采用后序便利的方式，这一点在后续会有更多的体现。

* 函数：生成函数名称，而后一次生成 statement 对应的代码即可，这里仅有 return 一种 statement
* return 语句：首先计算返回值，取出返回值（此时返回值一定被 push 入栈），放到对应寄存器并执行返回语句
* num节点：将对应数值 push 入堆栈即可。

```c++
void generate() {
    gen(func);
}

void gen(Node node) {
  switch (node.kind) {
      case ND_FUNC:
          print("  .global {node.name}\n");
          print("{node.name}:\n");
          for(n in node.body)
              gen(n);
          break;
      case ND_RET:
          gen(node.ret_val);
          pop("t0");	 // 栈式机：取出上一个node的结果
          print("  mv a0, t0\n");
          print("  ret\n");
          break;
      case ND_NUM:
          print("  li t0, {node.val}\n");
          push("t0");    // 栈式机：将结果push如栈
          break;
      default:
          assert(false);
    }
}

// 包装 push 与 pop 指令
void pop(String reg) {
    print("  ld {reg}, 0(sp)\n add sp, sp, 8\n");
}

void push(String reg) {
    print("  sd {reg}, -8(sp)\n add sp, sp, -8\n");
}
```

