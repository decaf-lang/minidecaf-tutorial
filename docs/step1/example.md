# 通过例子学习，一个仅有 return 的主函数编译全流程：

本步骤主要涉及的语法为主函数和 return 语句，完成本步骤之后，你的编译器将支持将一个仅有 return 的主函数编译为 32 位 RISC-V 汇编代码，并通过 RISC-V 工具链生成可以在硬件模拟器上正确运行的程序。因为这是大家首次接触 MiniDecaf 编译实验框架，我们给大家的代码框架中已经包含所有 step1 的实现，大家可以直接运行通过 step1 的测试用例。并且，我们在每个步骤的文档中会详细梳理介绍在当前步骤中需要用到的知识点以及对应的代码片段和注释，如果我们认为当前步骤并不需要了解某部分知识点（如数据流分析、寄存器分配），我们会在后续的步骤中进行知识点的讲解。

下面我们将通过一个简单的 step1 测试用例，一起走过它的编译全流程：

```C
int main() {
    return 2022;
}
```

> 请注意，这里给出的生成结果（抽象语法树、三地址码、汇编）只是一种参考的实现，同学们可以按照自己的方式实现，只要能够通过测试用例即可。但是，严格杜绝抄袭现象，如果代码查重过程中发现有抄袭现象，抄袭者与被抄袭者将被记为0分。

## 词法分析 & 语法分析

在词法分析 & 语法分析这一步中，我们需要将输入的程序字符流按照[语法规范](./spec.md)转化为后续步骤所需要的 AST，我们使用了 lex/yacc 库来实现这一点。[yacc](https://en.wikipedia.org/wiki/Yacc) 是一个根据 EBNF 形式的语法规范生成相应 LALR parser 的工具，支持基于属性文法的语法制导的语义计算过程。你可以根据我们的框架中对 lex/yacc 的使用，结合我们的文档，来快速上手 lex/yacc，完成作业；也可以选择阅读一些较为详细的文档，来系统地进行 lex/yacc 的入门，但这不是必须的。

为了方便同学们理解框架，我们将同时在这一段中说明为了加入取负运算所需要的操作。在 C++ 框架中，我们使用的是 lex/yacc 的高级替代 flex/bison，其使用方法和 lex/yacc 极为相似。在 Python 框架中，我们使用的是 lex/yacc 的一个纯 python 实现，称为 python-lex-yacc（简称 ply），其使用方法与 lex/yacc 有一些差异。

[C++ flex/bison 快速入门](https://www.gnu.org/software/bison/manual/html_node/A-Complete-C_002b_002b-Example.html)

[Python-lex-yacc 快速入门](https://www.dabeaz.com/ply/ply.html)

### C++ 框架

Makefile 中调用了 flex 和 bison 来处理 `parser.y` 和 `scanner.l`。flex 和 bison 会将这两个文件中的语法/词法描述翻译为 C++ 实现。

#### 概述

`src/frontend/scanner.l` 为词法描述。flex 生成的词法分析器，会将示例程序解析为这样的一串 Token：

`Int Identifier("main") LParen RParen LBrace Return  IntConst(2022) Comma RBrace`

这个程序的具体语法树中用到的语法规则如下: 

```C
Program -> Functions
Functions -> Type Identifier LParen RParen LBrace Statements RBrace
Statements -> ReturnStmt   
ReturnStmt -> Return IntConst(2022) Comma
```

`parser.y` 生成的语法分析器，分析获得的抽象语法树为：

```
Program 
  |-FoDList 
    |- FuncDefn
      |- (ret_type) Type INT
        |- (name) Identifier "main"
          |- (stmts) StmtList
            |- ReturnStmt 
              |- Expr int_const 2022
```

框架中 `scanner.l` 和 `parser.y` 是配合使用的，简单来说，`scanner.l` 定义了词法规则，`parser.y` 定义了语法规则。bison 生成的语法分析器，会调用 flex 生成的 `yylex()` 函数，这个函数的作用为获取 token 流的下一个 token。

#### 具体代码

让我们看看示例对应的 parser 代码：

`scanner.l` 中生成一个 Token 的规则，形如:

```C
"-"    { return yy::parser::make_MINUS(loc); }
# 该规则将一个'-'字符，解析为parser中的MINUS token。
```

> `yy::parser::make_MINUS()` 函数是在 `parser.y` 中声明 `MINUS` 这个 token 之后，yacc 自动生成的 token 构造函数。loc 是表示当前扫描位置的行列的全局变量。下面一段就是 `parser.y` 中声明 `MINUS` 这个 token 的位置。具体语义可参考 [Bison 教程](https://www.gnu.org/software/bison/manual/html_node/Complete-Symbols.html)。

```c
%define api.token.prefix {TOK_}
%token
   //more tokens...
   MINUS "-"
   //more tokens...
;
```

具体语义可参考[链接](https://www.gnu.org/software/bison/manual/html_node/Complete-Symbols.html)。

一元负号对应的语法树节点为 `NegExpr`，相关定义分散在 `src/ast/ast.hpp`，`src/ast/ast.cpp`，`src/ast/ast_neg_expr.cpp`，`src/ast/visitor.hpp`，`src/define.hpp` 中。注意 `ast.hpp` 中定义了节点的枚举类型 `NodeType`，`ast.cpp` 中定义了一个字符数组按顺序存储这些节点的名称，请保持和 `NodeType` 中的顺序一致。

```c++
// src/ast/ast.hpp
class NegExpr : public Expr {
  public:
//these member functions defined in src/ast/ast_neg_expr.cpp
    NegExpr(Expr *e, Location *l);
    virtual void accept(Visitor *);
    virtual void dumpTo(std::ostream &);
  public:
    Expr *e;
};
```
在 `parser.y` 中，要为一元负号编写对应的语法规则和动作。省略 `Expr` 对应的其他规则，形如：

```c
Expr : MINUS Expr %prec NEG { $$ = new ast::NegExpr($2, POS(@1));} ;
```

其中，`$2` 意味着右侧的 `Expr` 语法树节点，基于此，调用 `ast::NegExpr` 构造函数，获得新的 `NegExpr`，赋值给`$$`，作为这一级语法分析返回的节点。`%prec NEG` 注明的是这条规则的优先级，和优先级定义中的 `NEG` 相同。

```c
/*   SUBSECTION 2.2: associativeness & precedences */
%nonassoc QUESTION
%left     OR
%left     AND
%left EQU NEQ
%left LEQ GEQ LT GT
%left     PLUS MINUS
%left     TIMES SLASH MOD
%nonassoc LNOT NEG BNOT
%nonassoc LBRACK DOT
```
这是 `parser.y` 中的优先级定义，自上而下优先级越来越高。`%left, %nonassoc` 标注了结合性。注意，非终结符也需要声明。如 `parser.y` 中 `%nterm<mind::ast::Expr*> Expr` 表示 `Expr` 非终结符对应的语法树节点是 `mind::ast::Expr*` 类型（的指针）。我们将非终结符都声明为语法树结点的指针类型。每条语法规则里对应的动作会构建一个新的语法树结点，像刚才看到的 `NegExpr`。之后，你可能需要自己增加 token 的定义、语法树节点的定义。

### Python 框架

程序的入口点在 `main.py`，它通过调用 `frontend.parser.parser`（位于 `frontend/parser/ply_parser.py`）来完成语法分析的工作，而这一语法分析器会自动调用位于 `frontend/lexer/ply_lexer.py` 的词法分析器进行词法分析。语法的定义和语法分析器都位于 `frontend/parser/ply_parser.py`，而词法的定义位于 `frontend/lexer/lex.py`。AST 节点的定义位于 `frontend/ast/tree.py` 中。以下表示中的符号都出自于这几个文件。

当程序读入上述程序的字符流之后，它首先会被 lexer 处理，并被转化为如下形式的一个 Token 流：

`Int Identifier("main") LParen RParen LBrace Return Integer(2022) Comma RBrace`

并被 yacc 生成的 LALR(1) parser 转化为如下形式的 AST：

```
Program
    |- (children[0]) Function
        |- (ret_t) TInt
        |- (ident) Identifier("main")
        |- (body) Block
            |- (children[0]) Return
                |- (expr) IntLiteral(2022)
```

得到的这个 AST 也就是 `main.py` 中 `step_parse` 这一函数里 `parser.parse(...)` 的输出。

如果我们想把返回值从 `2022` 变成 `-2022`，则在这一步中你可能需要进行以下操作（实际上这些实现已经在框架里提供）：

* 在 `frontend/ast/tree.py` 里加入新的 AST 节点定义（以及相应的其它东西），可能长这样：

```python
class Unary(Expression):
    def __init__(self, op: Operator, operand: Expression):
        ...
```

    并在 `frontend/ast/visitor.py` 中加入相应的分派函数。

    它将在后续的 parser 语义计算中被用到。

* 在 `frontend/lex/lex.py` 里加入新的 lex token 定义:

```python
t_Minus = "-"
```

    在 ply 的 lexer 中，定义的新 token 需要以 `t_`开头。更具体的解释见文件注释或[文档](https://www.dabeaz.com/ply/ply.html)。

* 在 `frontend/parser/ply_parser.py` 里加入新的 grammar rule，可能包含（不限于）以下的这些：

```python
def p_expression_precedence(p): # 定义的新语法规则名。可以随便起，但必须以 `p_` 开头以被 ply 识别。
    """
    expression : unary
    unary : primary
    """ # 以 [BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) 定义的新语法规则，以 docstring 的形式提供。
    p[0] = p[1] # 这条语法规则相应的语义计算步骤，下标对应着产生式中的相应符号。
    # 语法分析器直接产生的实际上是一棵语法分析树，而构建 AST 这一数据结构则通过相应语法制导的语义计算过程来完成。

def p_unary_expression(p):
    """
    unary : Minus unary
    """
    p[0] = tree.Unary(UnaryOp.Neg, p[2])
```

    更多的用法同样可参见[文档](https://www.dabeaz.com/ply/ply.html)。

这样就基本完成了词法 & 语法分析步骤里加入取负运算的所有步骤。后续步骤中可能需要在某些 visitor 中实现相应的检查、转化至 TAC 的逻辑。

另外需要留意的一点是，python 框架中解决运算符结合律、优先级和悬吊 else 问题的方法与 C++ 框架中略有不同：C++ 框架下使用了 yacc 的特性直接指定了相应语法规则的优先级和结合律，但在 python 框架中我们通过对相应语法规则进行变换来达到这一目的，这些变换方法（优先性级联、规定左结合/右结合、最近嵌套匹配）在学习 CFG 时应有涉及，此处不多赘述。

## 语义分析

在 step1 语义分析步骤中，我们要遍历 AST，检验是否存在如下的语义错误：

* main 函数是否存在。

* return 语句是否有返回值。

* 返回值是否在 int 合法的范围内。

在实际操作中，我们遍历 AST 所用的方法就是的 [Visitor 模式](./visitor.md)，通过 Visitor 模式，我们可以从抽象语法树的根结点开始，遍历整颗树的所有语法结点，并针对特定的语法结点作出相应的操作，如名称检查和类型检查等。在编译器中，这种基于 Visitor 的对语法树进行一次遍历，完成某种检查或优化的过程，称为遍（pass）。不难想到，一个现代编译器是由很多遍扫描组成的，如 gcc 根据优化等级不同会有数百个不等的 pass。下面，我们将指出，step1 中我们是如何实现符号表构建 pass 和类型检查 pass 的，选择不同语言的同学，可以选择去看相应的代码注释与实现细节。

### Python 框架

`frontend/typecheck/namer.py` 和 `typer.py` 分别对应了符号表构建和类型检查这两次遍历。在框架中，`Namer` 和 `Typer` 都是继承 `frontend/ast/visitor.py` 中的 `Visitor` 类来通过 Visitor 模式遍历 AST 的。其实现细节参见代码。

### C++ 框架

`translation/build_sym.hpp` 和 `translation/type_check.hpp` 及相应 cpp 文件分别对应了符号表构建和类型检查这两次遍历。在框架中，两者都是继承 `ast/visitor.hpp` 中的 `Visitor` 类来通过 Visitor 模式遍历 AST 的。在新增 AST 节点后，必须在两者中增加对应的 `visitXXX` 函数。其实现细节参见代码。

## 中间代码生成

在通过语义检查之后，编译器已经掌握了翻译源程序所需的信息（符号表、类型等），下一步要做的则是将抽象语法树翻译为便于移植和优化的中间代码，在本实验框架中就是三地址码。如何翻译抽象语法树？当然还是无所不能的 Visitor 模式，我们在中间代码生成步骤中再遍历一次语法树，对每个结点做对应的翻译处理。具体来说，在 step1 当中，我们只需要提取 return 语句返回的常量，为之分配一个临时变量，再生成相应的 TAC 返回指令即可。不难看出，本例对应的三地址码为：

```asm
main:           # main 函数入口标签
    _T0 = 2022  # 为立即数2022分配一个临时变量
    return _T0  # 返回
```

> 下面，我们同样也指出了在代码中我们是怎样实现这个中间代码生成 pass 的，大家可以参考注释和代码了解实现细节。

### Python 框架

`frontend/tacgen/tacgen.py` 中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。

`frontend/utils/tac` 目录下实现了生成 TAC 所需的底层类。其中 `tacinstr.py` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。提供给生成 TAC 程序流程的主要接口在 `funcvisitor.py` 中，若你增加了 TAC 指令，则需要在 `FuncVisitor` 类中增加生成该指令的接口。在本框架中，TAC 程序的生成是以函数为单位，对每个函数（step1-8 中只有 main 函数）分别使用一个 `FuncVisitor` 来生成对应的 TAC 程序。除此之外的 TAC 底层类，同学们可以不作修改，也可以按照自己的想法进行修改。

### C++ 框架

`translation/translation.hpp` 及相应 .cpp 文件中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。

tac 目录下实现了生成 TAC 所需的底层类。其中 `tac/tac.hpp` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。`tac/trans_helper.hpp` 及相应 cpp 文件中的 `TransHelper` 类用于方便地生成 TAC 指令流，若你增加了 TAC 指令，则需要在 `TransHelper` 类中增加生成该指令的接口。除此之外的 TAC 底层类，同学们可以不作修改，也可以按照自己的想法进行修改。

## 目标代码生成

目标代码生成步骤是对中间代码的再一次翻译，在本例中，你需要了解并掌握的知识点有:

1. 如何将一个立即数装载到指定寄存器中？

   RISC-V 提供了 li <reg> <imm32> 指令来支持加载一个 32 位立即数到指定寄存器中，其中 <reg> 表示寄存器名，<imm32> 表示立即数值，如：`li t0, 2022`，就是将立即数 2022 加载到寄存器 t0 中。

2. 如何设置返回值？

   在 RISC-V 中，a0 和 a1 是 gcc 调用约定上的存储返回值的寄存器，返回值会按照其大小和顺序存储在 a0 和 a1 中。也就是说，如果你有一个 32 位的返回值，你可以放在 a0 中返回，如果你有两个 32 位的返回值，你就需要把它们分别放在 a0 和 a1 中返回。更多的返回值会全部放入内存返回，如约定好的栈的某个位置，这取决于函数调用约定。 

   在我们的实验要求中，返回值均是单个 32 位的值。因此在当前步骤中你只需要了解，将需要返回的值放入 a0 寄存器中，然后在后面加上一条 ret 指令即可完成函数返回的工作。

综上所述，我们上述中间代码翻译成如下 RISC-V 汇编代码：

```asm
    .text         # 代码段
    .global main  # 声明全局符号 main
main:             # 主函数入口符号
    li t0, 2022   # 加载立即数2022到t0寄存器中
    mv a0, t0     # 将返回值放到a0寄存器中
    ret           # 返回
```

>  关于实现细节，对应的代码位置在下面给出，代码中提供注释供大家学习：

### Python 框架

Python 框架中关于目标代码生成的文件主要集中 `backend` 文件夹下，step1 中你只需要关注 `backend/riscv` 文件夹中的 `riscvasmemitter.py` 以及 `utils/riscv.py` 即可。具体来说 `backend/asm.py` 中会先调用 `riscvasmemitter.py` 中的 `selectInstr` 方法对每个函数内的 TAC 指令选择相应的 RISC-V 指令，然后会进行数据流分析、寄存器分配等流程，在寄存器分配结束后生成相应的 `NativeInstr` 指令（即所有操作数都已经分配好寄存器的指令），最后通过 `RiscvSubroutineEmitter` 的 `emitEnd` 方法生成每个函数的 RISC-V 汇编。

### C++ 框架

C++ 框架中关于目标代码生成的文件主要集中在 `src/asm` 文件夹下，step1 中你只需要关注 `src/asm/riscv_md.cpp` 即可。具体来说，`riscv_md.cpp` 中的 `emitPiece` 函数是整个目标代码生成模块的入口。你只需要顺着函数调用的逻辑，以及我们提供的注释，就能够走通整个编译的流程。
