# 通过例子学习，一个仅有 return 的主函数编译全流程：

本步骤主要涉及的语法为主函数和 return 语句，完成本步骤之后，你的编译器将支持将一个仅有 return 的主函数编译为32位 RISC-V 汇编代码，并通过 RISC-V 工具链生成可以在硬件模拟器上正确运行的程序。因为这是大家首次接触 MiniDecaf 编译实验框架，我们给大家的代码框架中已经包含所有 Step1 的实现，大家可以直接运行通过 Step1 的测试用例。并且，我们在每个步骤的文档中会详细梳理介绍在当前步骤中需要用到的知识点以及对应的代码片段和注释，如果我们认为当前步骤并不需要了解某部分知识点（如数据流分析、寄存器分配），我们会在后续的步骤中进行知识点的讲解。

下面我们将通过一个简单的 step1 测试用例，一起走过它的编译全流程：

```C
int main() {
    return 2021;
}
```

> 请注意，这里给出的生成结果（抽象语法树、三地址码、汇编）只是一种参考的实现，同学们可以按照自己的方式实现，只要能够通过测试用例即可。

## 词法分析语法分析

> TODO：合理排版呈现，现在比较乱

Token流：

Int Identifier("main") LParen RParen LBrace Return  IntConst(2021)  Comma  RBrace

AST: 

Program -> Functions -> Type Identifier LParen RParen LBrace Statements RBrace

Statements -> ReturnStmt   ReturnStmt -> Return IntConst(2021) Comma

(制图?)

Makefile中调用了flex和bison来处理parser.y和scanner.l, 将对语法分析器和词法分析器的描述翻译为C++实现。

scanner.l和parser.y是配合使用的，简单来说，scanner.l定义了词法规则，parser.y定义了语法规则。parser.y自动生成的语法分析器，会调用scanner.l生成的yylex()函数, 相当于getNextToken()

将“return"解析为一个token的规则，在scanner.l中是

"return"      { return yy::parser::make_RETURN  (loc);   }

loc是表示当前扫描位置的line\column行列的全局变量，yy::parser::make_RETURN是parser.y自动生成的函数，构建一个parser能够使用的RETURN token。

在parser.y中，

%token

RETURN "return"

;

这一段就为parser声明了RETURN这个token。 

%token <std::string> IDENTIFIER "identifier" 

%token<int> ICONST "iconst"

具体语义可参考

https://www.gnu.org/software/bison/manual/html_node/Complete-Symbols.html。

非终结符也需要声明。

%nterm<mind::ast::Program* > Program FoDList

我们将非终结符都声明为语法树结点的指针类型。每条语法规则里对应的动作会构建一个新的语法树结点。如

FuncDefn : Type IDENTIFIER LPAREN FormalList RPAREN LBRACE StmtList RBRACE { $$ = new ast::FuncDefn($2,$1,$4,$7,POS(@1)); } |

$1, $2按顺序索引规则右侧的非终结符。

## 语义分析

在 Step1 语义分析步骤中，我们要遍历 AST，检验是否存在如下的语义错误：

* main 函数是否存在。

* return 语句是否有返回值。

* 返回值是否在 int 合法的范围内。

在实际操作中，我们遍历 AST 所用的方法就是的 [Visitor 模式](docs/step1/visitor.md)，通过 Visitor 模式，我们可以从抽象语法树的根结点开始，遍历整颗树的所有语法结点，并针对特定的语法结点作出相应的操作，如名称检查和类型检查等。在编译器中，这种基于 Visitor 的对语法树进行一次遍历，完成某种检查或优化的过程，称为遍（pass）。不难想到，一个现代编译器是由很多pass 组成的，如 gcc 根据优化等级不同会有数百个不等的 pass。下面，我们将指出，step1 中我们是如何实现符号表构建 pass 和类型检查 pass 的，选择不同语言的同学，可以选择去看相应的代码注释与实现细节。

### Python 框架

`frontend/typecheck/namer.py` 和 `typer.py` 分别对应了符号表构建和类型检查这两次遍历。在 Step1-10 中，同学们只需要考虑 `namer.py`（因为只有 int 类型，无需进行类型检查）。在框架中，namer 和 typer 都是继承 `frontend/ast/visitor.py` 中的 Visitor 类来通过 Visitor 模式遍历 AST 的。其实现细节参见代码。

### C++ 框架

`translation/build_sym.hpp` 和 `translation/type_check.hpp` 及相应 .cpp 文件分别对应了符号表构建和类型检查这两次遍历。在 Step1-10 中，同学们只需要考虑 `build_sym.hpp`（因为只有 int 类型，无需进行类型检查）。在框架中，两者都是继承` ast/visitor.hpp` 中的 Visitor 类来通过 Visitor 模式遍历 AST 的。其实现细节参见代码。

## 中间代码生成

在通过语义检查之后，编译器已经掌握了翻译源程序所需的信息（符号表、类型等），下一步要做的则是将抽象语法树翻译为便于移植和优化的中间代码，在本实验框架中就是三地址码。如何翻译抽象语法树？当然还是无所不能的 Visitor 模式，我们在中间代码生成步骤中再遍历一次语法树，对每个结点做对应的翻译处理。具体来说，在 step1 当中，我们只需要提取 return 语句返回的常量，为之分配一个临时变量，再生成相应的 TAC 返回指令即可。不难看出，本例对应的三地址码为：

```asm
main:           # main 函数入口标签
    _T0 = 2021  # 为立即数2021分配一个临时变量
    return _T0  # 返回
```

> 下面，我们同样也指出了在代码中我们是怎样实现这个中间代码生成 pass 的，大家可以参考注释和代码了解实现细节。

### Python 框架

`frontend/tacgen/tacgen.py` 中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。

`frontend/utils/tac` 目录下实现了生成 TAC 所需的底层类。其中 `tacinstr.py` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。提供给生成 TAC 程序流程的主要接口在 `funcvisitor.py` 中，若你增加了 TAC 指令，则需要在 FuncVisitor 类中增加生成该指令的接口。在本框架中，TAC 程序的生成是以函数为单位，对每个函数（Step1-8 中只有 main 函数）分别使用一个 FuncVisitor 来生成对应的 TAC 程序。除此之外的 TAC 底层类，同学们可以不作修改，也可以按照自己的想法进行修改。

### C++ 框架

`translation/translation.hpp` 及相应 .cpp 文件中通过一遍 AST 扫描完成 TAC 生成。和语义分析一样，这部分也使用了 Visitor 模式。

tac 目录下实现了生成 TAC 所需的底层类。其中 `tac/tac.hpp` 下实现了各种 TAC 指令，同学们可以在必要时修改或增加 TAC 指令。`tac/trans_helper.hpp` 及相应 .cpp 文件中的 TransHelper 类用于方便地生成 TAC 指令流，若你增加了 TAC 指令，则需要在 TransHelper 类中增加生成该指令的接口。除此之外的 TAC 底层类，同学们可以不作修改，也可以按照自己的想法进行修改。

## 目标代码生成

目标代码生成步骤是对中间代码的再一次翻译，在本例中，你需要了解并掌握的知识点有:

1. 如何将一个立即数装载到指定寄存器中？

   RISC-V 提供了 li <reg> <imm32> 指令来支持加载一个 32 位立即数到指定寄存器中，其中 <reg> 表示寄存器名，<imm32> 表示立即数值，如：`li t0, 2021`，就是将立即数 2021 加载到寄存器 t0 中。

2. 如何设置返回值？

   在 RISC-V 中，a0 和 a1 是 gcc 调用约定上的存储返回值的寄存器，返回值会按照其大小和顺序存储在 a0 和 a1 中。也就是说，如果你有一个 32 位的返回值，你可以放在 a0 中返回，如果你有两个 32 位的返回值，你就需要把它们分别放在 a0 和 a1 中返回。更多的返回值会全部放入内存返回，如约定好的栈的某个位置，这取决于函数调用约定。 

   在我们的实验要求中，返回值均是单个 32 位的值。因此在当前步骤中你只需要了解，将需要返回的值放入 a0 寄存器中，然后在后面加上一条 ret 指令即可完成函数返回的工作。

综上所述，我们上述中间代码翻译成如下 RISC-V 汇编代码：

```asm
    .text         # 代码段
    .global main  # 声明全局符号 main
main:             # 主函数入口符号
    li t0, 2021   # 加载立即数2021到t0寄存器中
    mv a0, t0     # 将返回值放到a0寄存器中
    ret           # 返回
```

>  关于实现细节，对应的代码位置在下面给出，代码中提供注释供大家学习：

### Python 框架

> TODO：补充 Python 框架目标代码生成细节。

### C++ 框架

C++ 框架中关于目标代码生成的文件主要集中在 `src/asm` 文件夹下，step1 中你只需要关注 `src/asm/riscv_md.cpp` 即可。具体来说，`riscv_md.cpp` 中的 `emitPiece` 函数是整个目标代码生成模块的入口。你只需要顺着函数调用的逻辑，以及我们提供的注释，就能够走通整个编译的流程。