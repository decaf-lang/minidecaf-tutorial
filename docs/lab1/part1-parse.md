# 词法语法解析

## 词法解析

词法分析器（也叫扫描器或标记器）是编译器的一个阶段，它将一个字符串（源代码）分解成一个标记列表（token list）。一个标记（token）是语法解析器（parser）能够理解的最小单位。如果一个程序就像一个段落，那么标记就像一个个单词（许多标记是用空格隔开的独立的单词）。变量名（variable names）、关键字（keywords）、常量（constants）以及像括号（braces）这样的标点符号都是标记的例子。

下面是词法分析器（lexer）需要识别的所有标记，以及定义每个标记的正则表达式（regular expression）。

- Open brace `{`
- Close brace `}`
- Open parenthesis `\(`
- Close parenthesis `\)`
- Semicolon `;`
- Int keyword `int`
- Return keyword `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`

直接使用 "keyword" 这样统一的一个标记类型（token type），而不是为每个关键词使用不同的标记类型也是一种可行的方法。

## 语法解析

我们需要一个形式化的语法，它定义了一系列标记如何组合成语言构造。我们将基于[Backus-Naur Form](https://en.wikipedia.org/wiki/Backus-Naur_form-Naur_form)来定义：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <int>
```

上面的每一行都是一个产生式（*production* ），定义了如何从一种形式语言（BNF）的构造和标记来建立另外一个语言（minidecaf）的构造。每一个出现在产生式左侧的符号（即`<program>`、`<function>`、`<statement>`）都是一个非终结符（non-terminal symbol）。个别标记（keywords、id、punctuation等）是终结符（terminal symbols）。请注意，虽然这个语法告诉我们什么样的标记序列构成了一个有效的minidecaf程序，但它*没有告诉我们到底如何将这个程序转化为AST--例如，在AST中没有对应Constant节点的产生式。我们可以重写我们的语法，让常量有一个产生式，但这不是必须的。

现在的语法非常简单，每个非终结符只有一条产生式。在后续试验中，一些非终结符将有多个产生式。例如，如果我们增加了对变量声明的支持，我们就可以有以下的产生式。

```
<statement> ::= "return" <int> ";" | "int" <id> "=" <int> ";"
```

下一步是将我们的标记列表转化为抽象的语法树（Abstract Syntax Tree，简称AST）。AST是表示程序结构的一种方式。在大多数编程语言中，像条件和函数声明这样的语言结构是由更简单的结构组成的，比如变量和常量。AST捕捉到了这种关系；AST的根将是整个程序，而每个节点将有子节点代表它的组成部分。

现在，我们需要支持的AST节点只有程序（programs）、函数声明（function declarations）、语句（statements）和表达式（expressions）。对于一个可以返回正整的main函数，下面我们给出AST节点的定义：

```
program = Program(function_declaration)
function_declaration = Function(string, statement) //string is the function name
statement = Return(exp)
exp = Constant(int) 
```

现在，一个程序由一个函数`main`组成。在后面的步骤中，我们将把一个程序定义为一个函数列表。一个函数有一个名称（name）和一个函数体（body）。以后，一个函数还会有一个参数列表（list of arguments）。在实际的编译器中，我们还需要存储函数的返回类型（return type），但现在我们只有整数类型。函数体中只包含一条单一的语句（后续会扩展为语句列表）。语句的类型只有一种：返回语句（return statement）。以后我们会增加其他类型的语句，比如条件（conditionals）和变量声明（variable declarations）。一个返回语句有一个子语句，即表达式--这就是被返回的值。现在一个表达式只能是一个整数常量。以后我们会让表达式包含算术运算，这将使我们能够解析像`return 2+2;`这样的语句。

当我们添加新的语言结构时，我们会更新AST节点的定义。例如，我们最终会添加一种新的语句类型：变量赋值。当我们这样做的时候，我们会在我们的`statement`定义中添加一个新的形式。

```
statement = Return(exp) | Assign(variable, exp)
```

以一个最简单的程序为例：

```
int main() {
    return 2;
}
```

AST如下所示：

- Program
  - Function (name: main)
    - body
      - return statement
        - constant (value: 2)

最后，

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

后面可以发现，产生式是递归的（例如一个算术表达式可以包含其他表达式），这意味着解析函数也将是递归的。因此这种技术被称为递归下降解析。