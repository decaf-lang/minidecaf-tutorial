
# Lab1：整数

这是关于编写minidecaf编译器的第一个步骤。

编写minidecaf编译器是参考了使用Abdulaziz Ghuloum的[An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)和Nora Sandler的[Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)作为路线图。这里的minidecaf语言基本上是C语言的一个子集。你通过从编译minidecaf源语言的一个微不足道的子集开始，能够生成[RISC-V汇编代码](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-intro.md)，并能在RISC-V机器（目前是基于QEMU模拟器）上运行/测试你写的编译器生成的最终机器代码。然后你再一步一步地添加新的语言特性。在第一步中，你只是返回常量；在后面的步骤中，你处理加法和减法；以此类推。每一步都小到足以让人感觉到易于管理，而在每一步结束时，你都有一个可以工作的编译器。另外，通过足够详尽的[测试程序](https://github.com/decaf-lang/minidecaf-tests)，你可以随时验证你的编译器在每次更新后是否正常工作。

# 前言

在你开始之前，你需要决定两件事：用什么语言来写你的编译器，以及如何处理词法分析（lexing）和语法解析（parsing ） 。你可以用任何你喜欢的语言来实现编译器

> 提示：建议使用具有和[sum type](https://chadaustin.me/2015/07/sum-types/)和模式匹配（ pattern matching）的语言，比如OCaml、Haskell或Rust。如果你这样做的话，构建和遍历一个AST会变得更加简单。前提是你能接受学习和掌握这些编程语言的所投入的时间与精力。

你还需要决定是自己写语法解析器和词法分析器，还是使用自动解析器和扫描器生成器（例如[flex](https://github.com/westes/flex)，[bison](https://www.gnu.org/software/bison/)，[antlr4](https://www.antlr.org)）。在整个实验环节中，两种方式都会提供。我们将展示如何手工编写一个词法器（或扫描器）和递归下降解析器。使用解析器生成器可能更容易，缺点是了解底层运行细节和调试bug可能会困难一些。如果能够直接设计实现解析器生成器，那么对编译课上讲的很多原理、算法的理解会更加深入。

> 注意：设计实现解析器生成器不是基本实验要求。

# 第一步 : 整数

本阶段我们将编译一个返回单个整数的minidecaf程序。我们还将建立编译器的三个基本阶段（pass）：词法、解析和代码生成。。第一步将有比较大的工作量，即建立了一个编译器的框架，该框架将使以后添加更多语言特性变得容易，对后续实验步骤有较大的帮助，

下面是一个我们要编译的程序 return_2.c

```
int main() {
    return 2;
}
```

我们将只处理有一个函数 "main "的程序，它由一个返回语句组成。唯一不同的是返回的整数的值，我们不会处理十六进制或八进制的整数，只处理十进制。我们不会处理十六进制或八进制的整数，只处理十进制。为了验证你的编译器是否正常工作，你需要编译一个程序，运行它，并检查它的返回代码。

```
$ YOUR_COMPILER return_2.c # 用例的编译器会把return_2.c编译为 return.s 汇编程序
$ riscv64-unknown-elf-gcc return_2.s -o return_2 # riscv-64汇编器把return.s翻译为return_2执行程序
$ qemu-riscv64 ./return_2 # 用QEMU for riscv-64硬件模拟器运行return_2执行程序
$ echo $? # 检查return_2执行程序的执行结果，应该是 2
2 
```

你的编译器会产生risc-v汇编代码。我们不会自己将汇编文件转化为可执行文件--那是汇编器和链接器的工作（最好有个链接介绍汇编器和连接器）。为了看看这个程序在汇编中的样子，让我们用GCC来编译它。

```
$ riscv64-unknown-elf-gcc -S -O3 return_2.c
$ cat return_2.s
    .section __TEXT,__text_startup,regular,pure_instructions
    .align 4
    .globl _main
_main:
    movl    $2, %eax
    ret
    .subsections_via_symbols
```

现在，让我们看看汇编程序本身。我们可以忽略`.section`、`.align`和`.subsections_via_symbols`指令，这些汇编原语可参加[这里的介绍](https://github.com/decaf-lang/minidecaf/blob/master/doc/riscv-assembly-directives.md)。--如果你删除它们，你仍然可以生成并运行return_2执行程序。`.globl main`表示`main`符号应该对链接器可见，否则它找不到程序的入口点。

最后，我们有了实际的汇编指令。

```
main:                  ; label for start of "main" function
    movl    $2, %eax    ; move constant "2" into the EAX register
    ret                 ; return from function
```

这里最重要的一点是，当一个函数返回时，XXX寄存器[5](https://norasandler.com/2017/11/29/Write-a-Compiler.html#fn5)将包含其返回值。`main`函数的返回值将是程序的退出代码。在上面的汇编片段中，唯一可以改变的是返回值。

> 注意：在实验指导中，将使用AT&T汇编语法。每当你在阅读汇编时，请确保你知道它使用的是什么语法!

## 词法分析

词法分析器（也叫扫描器或标记器）是编译器的一个阶段，它将一个字符串（源代码）分解成一个标记列表（token list）。一个标记（token）是语法解析器（parser）能够理解的最小单位--如果一个程序就像一个段落，那么标记就像一个个单词(许多标记是用空格隔开的独立的单词)。变量名（variable names）、关键字（keywords）、常量（constants）以及像括号（braces）这样的标点符号都是标记的例子。下面是 return_2.c 中所有标记的列表。

- `int` keyword
- Identifier “main”
- Open parentheses
- Close parentheses
- Open brace
- `return` keyword
- Constant “2”
- Semicolon
- Close brace

>  注意，有些标记有一个值 (例如常量(constant)标记的值是 "2")，有些则没有 (如括号和大括号)。

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

> 提示：你也可以直接使用 "keyword"这样统一的一个标记类型（token type），而不是为每个关键词使用不同的标记类型。

#### ☑任务：

写一个*lex*函数，接受一个文件并返回一个标记列表。它应该适用于[minidecaf测试用例](https://github.com/decaf-lang/minidecaf-tests)中的所有[`step1`](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)中的示例。为了保持简单，我们只对十进制整数进行词法分析。如果你愿意尝试，你也可以扩展你的词法分析器来处理八进制和十六进制整数。

> 注意：我们不能对负整数进行词法分析。这并不是偶然的--C 语言没有负整数常量。它只是有一个负一元运算符，可以应用于正整数。我们将在下一步添加负一元运算。

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

一个赋值语句（如`c=2;`）也有两个子节点：被更新的变量（`c`）和赋值给它的表达式（`2`）。

另一方面，`if body`是语句列表，它可以有任意数量的子节点--每个语句都是一个子节点。在本例中，它有两个子节点，因为有两条语句。这些子节点是有序的--`c=2;`排在`return c;`之前，因为在源代码中就是这样按序排列的。

下面是这段代码的完整AST：

![Image of diagram; text outline follows](./lab1-pics/AST.svg)

- if statement
  - condition: binary operation (<)
    - operand 1: variable a
    - operand 2: variable b
  - if body: statement list
    - statement 1: assignment
      - variable: c
      - right-hand side: constant 2
    - statement 2: return
      - return value: variable c
  - else body: statement list
    - statement 1: assignment
      - variable: c
      - right-hand side: constant 3

而这里是构造这个AST的伪代码：

```
//create if condition
cond = BinaryOp(op='>', operand_1=Var(a), operand_2=Var(b))

//create if body
assign = Assignment(var=Var(c), rhs=Const(2))
return = Return(val=Var(c))
if_body = [assign, return]

//create else body
assign_else = Assignment(var=Var(c), rhs=Const(3))
else_body = [assign_else]

//construct if statement
if = If(condition=cond, body=if_body, else=else_body)
```

不过现在我们不需要担心条件（conditionals）、变量赋值（variable assignments）或二进制操作符（binary operators）。现在，我们需要支持的AST节点只有程序（programs）、函数声明（function declarations）、语句（statements）和表达式（expressions）。下面是我们对`return_2.c`给出的AST节点的定义：

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

这里是return_2.c的AST图。

![Image of diagram; text outline follows](./Writing a C Compiler, Part 1_files/return_2_ast.svg)

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

上面的每一行都是一个产生式（*production* ），定义了如何从一种形式语言（BNF）的构造和标记来建立另外一个语言（minidecaf）的构造。每一个出现在产生式左侧的符号（即`<program>`、`<function>`、`<statement>`）都是一个非终结符（non-terminal symbol）。个别标记（keywords、id、punctuation等）是终结符（terminal symbols）。请注意，虽然这个语法告诉我们什么样的标记序列构成了一个有效的minidecaf程序，但它*没有告诉我们到底如何将这个程序转化为AST--例如，在AST中没有对应Constant节点的产生式。我们可以重写我们的语法，让常量有一个产生式，但这不是必须的。

现在的语法非常简单，每个非终结符只有一条产生式。在后续试验中，一些非终结符将有多个产生式。例如，如果我们增加了对变量声明的支持，我们就可以有以下的产生式。

```
<statement> ::= "return" <int> ";" | "int" <id> "=" <int> ";"
```

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

后面可以发现，产生式是递归的（例如一个算术表达式可以包含其他表达式），这意味着解析函数也将是递归的--因此这种技术被称为递归下降解析。

#### ☑任务：

编写一个*parse*函数，接受一个标记列表，并返回一个AST，根节点（root node）是Program节点。该函数应该为所有有效的[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)建立正确的AST。如果你愿意，你也可以让你的解析器在遇到超过INT_MAX（整数最大值）的整数常量时优雅地失败并指出解析失败的原因。

有很多方法可以在代码中表示AST--每种类型的节点可以是它自己的类或它自己的数据类型，这取决于你用什么语言来编写编译器。例如，以下是你如何将AST节点定义为OCaml数据类型：

```
type exp = Const(int)
type statement = Return(exp)
type fun_decl = Fun(string, statement)
type prog = Prog(fun_decl)
```

## 代码生成

现在我们已经建立了一个AST，我们已经准备好生成汇编代码了！就像我们之前看到的，我们只需生成四行汇编码。为此，我们将大致按照程序执行的顺序遍历AST。这意味着我们将按顺序访问：

- 函数名： function name  (不是真正的node，而是`function definition`node中的一个属性)
- 返回值：return value
- 返回语句：return statement

> 注意，我们经常（虽然并不总是）以[post-order](https://en.wikipedia.org/wiki/Tree_traversal#Post-order)的方式遍历树，在其父类之前访问子类。例如，我们需要在返回语句中引用返回值之前生成它。在后面的s试验中，我们需要在生成对算术表达式进行操作的代码之前，生成算术表达式的操作数。

下面是我们要生成汇编码：

1. 要生成一个函数（如函数 "foo"）。

```
    .globl foo
   foo:
    <FUNCTION BODY GOES HERE>
```

2. 生成一个返回语句（如：`return 3;`）的汇编码

```
    movl    $3, %eax
    ret
```

#### ☑任务：

写一个*generate*函数，接受一个AST并生成汇编。它可以以字符串的形式在屏幕上显示汇编代码，也可以直接把汇编代码写到文件中。它应该为所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)生成正确的汇编码。

## (可选) 漂亮的打印

你可能需要一个实用函数来打印出你的AST，以帮助调试。你可以现在就写，或者等到你需要的时候再写。下面是对return_2.c的AST输出例子：

```
FUN INT main:
    params: ()
    body:
        RETURN Int<2>
```

这个例子包含了一些AST不需要的信息，比如返回类型和函数参数列表。

#### ☑ 任务：写一个*pretty-print* funcion，它接收一个AST并以可读的方式打印出来。

写一个*pretty-print*的函数，接受一个AST并以可读的方式打印出来。

## 综合

#### ☑任务：

编写一个接受C源文件并输出可执行文件的程序（可以是一个包含调用你写的编译器和GCC的shell脚本）。该程序应该

1. 读取minidecaf源文件

2. 进行词法分析

3. 进行语法解析

4. 生成汇编码

5. 把汇编码写入到一个文件

6. 调用GCC命令，将生成的汇编码转换为可执行文件。在下面命令中，"assembly.s "是汇编文件的名称，"out "是你想生成的可执行文件的名称。

```
   riscv64-unknown-elf-gcc assembly.s -o out
```

7. (可选) 删除汇编文件。

## 测试

你可以修改[minidecaf测试](https://github.com/decaf-lang/minidecaf-tests)中的自动批量测试脚本，来测试你的编译器是否正常通过所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)。它将使用你的编译器编译一组测试程序，执行它们，并确保它们返回正确的值。


为了用脚本自动批量测试一组程序，你写的编译器需要遵循这个规范。

1. 它可以从命令行中调用，只需要一个C源文件作为参数，例如：1: `./YOUR_COMPILER /path/to/program.c`。
2. 当传入`program.c`时，它会在同一目录下生成`program.s`汇编代码文件。
3. 如果解析失败，它不会生成汇编代码文件。

脚本不会检查你的编译器是否输出合理的错误信息。

## 下一步

在[下一步]()中，我们将增加三个单数运算符。`-`、`~`和`！`。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)