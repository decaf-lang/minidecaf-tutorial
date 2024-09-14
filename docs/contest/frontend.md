# 前端梗概

前端的主要任务是将源代码转换为抽象语法树（Abstract Syntax Tree, AST），为中端和后端生成中间表示和目标代码提供基础。在这个过程中，前端会经历词法分析、语法分析、语义分析等多个步骤。

# 词法分析与语法分析

词法分析的任务是将源代码转换为一系列的符号（token），每个符号代表源代码中的一个最小单位，如关键词、标识符、操作符等。词法分析器会忽略空格、注释等非必要信息，并在此过程中进行基本的错误检测（如非法字符）。

下面我们以 Antlr 框架为例，介绍如何进行词法分析和语法分析。你也可以使用其他工具如 Flex & Bison, lex & yacc 等。

## Antlr简介

Antlr (Another Tool for Language Recognition) 是一个功能强大的解析器生成器，能够根据给定的语法规则自动生成词法分析器和语法分析器。Antlr 支持多种语言，包括 Java、Python 和 C++。通过定义语法文件（.g4 文件），Antlr 能够帮助我们生成解析源代码所需的词法分析和语法分析工具。

在这个项目中，我们推荐使用 Antlr 来处理 MiniDecaf 的词法分析和语法分析部分。

## 第一部分:依赖环境准备

ANTLR 工具需要 JVM 才能执行。

直接使用包管理器安装：

```bash
sudo apt install openjdk-19-jdk
```

### 1. 获取 ANTLR

你需要从 [ANTLR Download](https://www.antlr.org/download.html) 下载 `antlr-4.13.2-complete.jar`(截至文档写作时此为最新版)。

使用以下命令（记得把`/path/to/antlr-4.13.2-complete.jar`替换成你的 antlr 路径）测试是否能正常使用：

```bash
java -jar /path/to/antlr-4.13.2-complete.jar
```

你应该能看到类似以下的输出：

```bash
ANTLR Parser Generator  Version 4.13.2
 -o ___              specify output directory where all output is generated
 -lib ___            specify location of grammars, tokens files
 -atn                generate rule augmented transition network diagrams
 -encoding ___       specify grammar file encoding; e.g., euc-jp
... ...
```

### 3. ANTLR 运行时的编译链接

#### 1. 安装 ANTLR 运行时库

ANTLR 运行时库是解析器生成的代码在运行时所依赖的代码。对于 C++，你可以从 [ANTLR4 runtime Cpp的 GitHub 仓库](https://github.com/antlr/antlr4/tree/master/runtime/Cpp)下载预编译的库或者自己编译安装。但是官方的 CMAKE 脚本会从官方 git 仓库下载 ANTLR C++ 运行时并构建它，你在编译过程中很可能会因为网络等问题而失败，如果难以解决，可以直接 clone [ANTLR 运行时库的 C++ 源代码](https://www.antlr.org/download/antlr4-cpp-runtime-4.13.2-source.zip)到你的代码仓库里，并为你的整个项目编写一个 CMAKE 文件(**强烈建议**)。出于方便考虑，我在这里给出一个可能的项目结构与CMAKE文件实例.

- **项目结构**

  ```
  example-tree/
  ├── 3rd_party/
  │   └── antlr4-runtime/          # 第三方库 ANTLR 运行时目录(在源码的 src 目录下)
  │       ├── CMakeLists.txt       # antlr4-runtime 的 CMake 配置文件,需要你手动添加一个
  │       └── antlr4-runtime.h
  │       └── antlr4-common.h
  │       └── ...
  ├── CMakeLists.txt               # 根目录下的 CMake 配置文件
  └── src/                         # 源代码目录
      ├── frontend/                # 前端代码目录
      │   ├── lexer/               # 词法分析相关代码
      │   │   └── *.cpp            # 词法分析器源文件
      │   │   └── *.h              # 词法分析器头文件
      │   ├── parser/              # 语法分析相关代码
      │   │   └── *.cpp            # 语法分析器源文件
      │   │   └── *.h              # 语法分析器头文件
      │   └── ast/                 # 抽象语法树相关代码
      │       ├── *.cpp            # AST 源文件
      │       ├── *.h              # AST 头文件
      ├── backend/                 # 后端代码目录
      ├── midend/                  # 中间代码目录
      └── main.cpp                 # 程序入口文件
  ```

- 对应的 `CMakeLists.txt`

  ```cmake
  # 指定 CMake 的最小版本要求
  cmake_minimum_required(VERSION 3.10)

  # 设置项目名称和使用的语言（CXX 代表 C++）
  project(my_compiler CXX)

  # 设置 C++ 标准为 C++17
  set(CMAKE_CXX_STANDARD 17)

  # 设置 C++ 编译器标志，这里没有额外添加，使用默认
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

  # 设置调试模式下的编译器标志，开启 DEBUG 宏
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")

  # 使用 GLOB_RECURSE 模式递归查找 src 目录下所有的 .cpp 文件
  file(GLOB_RECURSE SRC "src/*.cpp")

  # 添加项目的 src 目录到头文件搜索路径
  include_directories(src)

  # 添加第三方库目录 antlr4-runtime 到头文件搜索路径
  include_directories(3rd_party/antlr4-runtime)

  # 添加 antlr4-runtime 子目录作为子项目进行构建
  add_subdirectory(3rd_party/antlr4-runtime)

  # 创建名为 my_compiler 的可执行文件，将所有源文件编译链接到这个可执行文件中
  add_executable(my_compiler ${SRC})

  # 将 antlr4_runtime 库与 my_compiler 可执行文件链接
  target_link_libraries(my_compiler antlr4_runtime)
  ```

- **为 antlr4-runtime 添加一个相应的 `CMakeLists.txt`**

```cmake
# 3rd_party/antlr4-runtime/CMakeLists.txt
file(GLOB_RECURSE ANTLR4_SRC "*.cpp")

add_library(antlr4_runtime STATIC ${ANTLR4_SRC})
```

## 第二部分：文法文件的编写与 parse tree 的生成

终于，在上一部分中，我们完成了项目的环境准备工作，可以着手开始编写代码了。在这一节中，我们会开始编写一个简单的 C 语言子集 `simpleC` 的文法文件 `simpleC.g4`，并利用它生成一个 parse tree。最终把一个简单的 C 语言程序 `test.c` 转换为一个 parse tree。

- `test.c`

  ```c
  int main(){
      int a = 1 ;
      int b = a + 2 ;
      int c = a + b + 1 ;
      return c ;
  }
  ```

- `parse tree`

  ```
  parse tree:
  (program
          (funcDeclaration int main ( ) {
              (statements
                  (statement int a =
                      (expression 1) ;)
                  (statement int b =
                      (expression
                          (expression a) +
                          (expression 2)) ;)
                  (statement int c =
                      (expression
                          (expression
                              (expression a) +
                              (expression b)) +
                          (expression 1)) ;)
                  (statement return
                      (expression c) ;)) }))
  ```



### 1. 编写simpleC.g4

`.g4` 文件是 ANTLR 使用的文法文件，用于定义语言的语法规则。它使用基于上下文的语法规则来描述语言的结构。一个典型的 `.g4` 文件包含以下几个部分：

1. **语法定义**：声明语法的名称，这是识别语法文件的关键字。这个语法名称必须要和包含这个语法的文件名完全相同(甚至包括大小写,因为 ANTLR 是对大小写敏感的)
2. **规则**：定义语言中各种结构的模式。
3. **词法规则**：定义词法单元（如关键字、标识符、符号等）。
4. **忽略规则**：通常用来忽略空格、换行等空白字符。
5. **操作**：在规则中嵌入的代码，用于在解析过程中执行特定的动作。

#### 示例 `.g4` 文件结构

```antlr
// 文件名: SimpleC.g4

grammar SimpleC; // 语法定义

// 程序的起始规则
program:   funcDeclaration ;

// 函数声明规则
funcDeclaration: Type ID LP RP LC statements RC ;

// 语句的规则
statements: statement* ;

// 声明和表达式
statement:   Type ID ASSIGN expression SEMI // varDeclaration
           | expression SEMI
           | 'return' expression SEMI
           ;

// 表达式的规则
expression: expression PLUS expression   // AddExpr
           | expression MINUS expression // SubExpr
           | expression MUL expression   // MulExpr
           | expression DIV expression   // DivExpr
           | '(' expression ')'          // ParenExpr
           | INT                         // IntExpr
           | ID                          // ID
           ;

// 类型的规则（这里只支持 int 类型）
Type: 'int' ;

// 整数的规则
INT: [0-9]+ ;

// 标识符的规则
ID: [a-zA-Z_] [a-zA-Z0-9_]* ;

// 忽略空格和换行
WS: [ \t\r\n]+ -> skip ;

// 定义括号和符号
LP: '(' ;
RP: ')' ;
LC: '{' ;
RC: '}' ;
SEMI: ';' ;
ASSIGN: '=' ;
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
```

通过编写 `.g4` 文件，我们能够为 ANTLR 提供足够的信息来构建一个能够理解和处理特定语言的解析器。这种形式的文法定义是编译器设计和语言工具开发的基础。

### 2. 使用文法文件生成 lexer & parser

在确认环境配置无误后，我们可以使用 ANTLR 和文法文件生成所需的 lexer & parser，只需要执行

```bash
java -jar /path/to/antlr-4.13.2-complete.jar -Dlanguage=Cpp -no-listener -visitor -o src/frontend/lexer_parser simpleC.g4
```

`-no-listener` 和 `-visitor` 选项分别用于禁止生成 listener（默认是激活的）和激活 visitor 模式。如果你还不知道 visitor 是什么，不用担心，我们稍后会看到。

-o 选项用于设置输出目录。我们将在 `src/frontend/lexer_parser` 目录中输出生成的代码。

### 3. 使用 lexer & parser

现在我们可以看到如何在 C++ 程序中使用我们生成的解析器。

```cpp
// src/main.cpp
#include "antlr4-runtime.h"
#include "frontend/lexer/SimpleCBaseVisitor.h"
#include "frontend/lexer/SimpleCLexer.h"
#include "frontend/lexer/SimpleCParser.h"
#include <fstream>
#include <iostream>

using namespace antlr4;
using namespace tree;
using namespace std;

int
main(int argc, const char* argv[])
{
  ifstream f_stream;
  f_stream.open(argv[1]);
  ANTLRInputStream input(f_stream);
  SimpleCLexer lexer(&input);
  CommonTokenStream tokens(&lexer);
  SimpleCParser parser(&tokens);
  ParseTree* tree = parser.program();
  cout << "parse tree: " << endl;
  SimpleCBaseVisitor parse_visitor;
  parse_visitor.visit(tree);
  cout << tree->toStringTree(&parser, true) << endl;
  return 0;
}
```

这是我们程序的主文件，展示了如何在 C++ 中设置使用 ANTLR。前几行（3-5）包含的头文件基本上是你总是会包含的标准头文件。第一个是使用运行时所需的，其他两个是为生成的词法分析器和解析器准备的。显然，它们的名字会根据语法的名字而改变，但概念保持不变。

16-21 行展示了使用 ANTLR 解析器的标准方式：

- 我们将输入转换为 ANTLR 格式
- 我们创建一个在该输入上工作的词法分析器
- 我们使用词法分析器产生一个 token 流
- 我们创建一个在令牌流上工作的解析器
- 然后，21 行使用解析器的一个方法，该方法对应于语法规则中的一个，以获得规则匹配的第一个节点。在我们的例子中，只有一个节点`program`，这是因为我们定义规则的方式。然而，原则上那可以是任意的，每次你调用相应的方法，你都会得到一个相应的结果。

现在，使用 cmake 构建并运行我们自己实现的编译器，你将会看到 `test.c` 对应的 parse tree 被输出到终端中。

```bash
./my_compiler test.c
```

总的来说，我们现在利用 ANTLR 实现了词法分析器分析输入（即字符）并产生 token，然后解析器分析 token 以产生 parser tree。这样，我们就把一个看似被复杂地组织起来的文本转化成了一个“树”，之后我们就可以使用 visitor 模式遍历这个树并对这个树的每个节点进行一些操作。

## 第三部分：AST 的生成

在生成 AST 时，我们通常是在解析树（parse tree）的基础上，通过提取语法的核心结构，生成更加精简的抽象语法树（AST）。AST 的节点通常只包含与程序执行相关的核心信息，去除了冗余的语法信息。

### 1. 定义 AST 结点

首先，我们需要为 AST 定义结点类型。每个结点对应于一种语法结构，比如条件语句、循环、表达式等。以下是一个简单的 `If` 语句结点的定义：

```cpp
class IfNode : public ASTNode {
public:
    std::unique_ptr<ASTNode> cond;   // 条件表达式
    std::unique_ptr<ASTNode> then;   // then 语句块
    std::unique_ptr<ASTNode> other;  // optional 的 else 语句块
    bool has_otherwise;
    IfNode(std::unique_ptr<ASTNode> cond, std::unique_ptr<ASTNode> then,
        std::unique_ptr<ASTNode> other = nullptr)
    : cond(std::move(cond)), then(std::move(then)), other(std::move(other)),
      has_otherwise(other != nullptr) {}
};
```

这个 `IfNode` 结点包含条件表达式`cond`、`then` 语句块和可选的 `else` 语句块。

### 2. 使用 Visitor 模式生成 AST

在生成 AST 时，我们需要遍历解析树（parse tree）并根据其结构生成对应的 AST 结点。这里我们可以使用 Visitor 模式，针对解析树的不同节点调用对应的处理函数，来生成合适的 AST 结点。

假设我们有一个解析树 `IfContext`，对应的语法规则如下：

```antlr
ifStatement
    : 'if' '(' expr ')' statement ('else' statement)?
    ;
```

我们可以继承 ANTLR 自动生成的 BaseVisitor 函数，为 `IfContext` 实现 Visitor 函数，以生成 `IfNode`：

```cpp
class ASTBuilderVisitor : public SimpleCBaseVisitor<std::unique_ptr<ASTNode>> {
public:
    // 访问 ifStatement 节点
    std::unique_ptr<ASTNode> visitIfStatement(SimpleCParser::IfStatementContext *ctx) override {
        // 访问并生成条件表达式的 AST 结点
        auto cond = visit(ctx->expr());

        // 访问并生成 then 语句的 AST 结点
        auto thenBranch = visit(ctx->statement(0));

        // 检查是否有 else 分支，并生成对应的 AST 结点
        std::unique_ptr<ASTNode> elseBranch = nullptr;
        if (ctx->statement(1)) {
            elseBranch = visit(ctx->statement(1));
        }

        // 构建 IfNode，并返回
        return std::make_unique<IfNode>(std::move(cond), std::move(thenBranch), std::move(elseBranch));
    }
};
```

这个 `ASTBuilderVisitor` 类的 `visitIfStatement` 方法遍历解析树中的 `ifStatement` 结点，生成 `IfNode` 并填充其条件表达式、then 和 else 分支。通过 Visitor 模式，代码变得结构清晰且便于扩展。

### 生成 AST 的完整流程

1. 编写 Antlr 语法文件，定义源语言的解析规则。
2. 使用 Antlr 生成词法分析器和语法分析器，解析源代码生成解析树。
3. 实现 Visitor 模式的遍历代码，逐个解析树结点处理并生成 AST 结点。
4. 利用 AST 结点构建抽象语法树，最终生成中间表示或目标代码。

通过这种方式，我们能够将解析树转换为精简的抽象语法树（AST），为后续的中端和后端处理提供基础。

## 第四部分：语义分析

语义分析的目标是检查程序的合法性，确保程序符合语言的语义规则。在大作业中，这一部分的实际作用主要是检测出 MiniDecaf 的错误测例并报告编译错误。这一步包括符号解析（名称绑定）和类型检查，以保证变量、函数等符号被正确地定义、引用和使用，并且操作符和操作数之间的类型匹配。

### 符号解析（namer）

符号解析的任务是将程序中使用的标识符（如变量名、函数名等）与它们的定义绑定起来。具体来说，符号解析会遍历抽象语法树（AST），并记录每个作用域中的符号定义。当在同一作用域或嵌套作用域中遇到符号引用时，解析器能够正确地找到该符号的定义或者报错。

#### 符号表

符号解析的核心工具是符号表（symbol table）。符号表是一个数据结构，用来存储标识符的名字及其相关信息（如类型、作用域、存储位置等）。通常符号表会随着作用域的嵌套而形成层级结构，以便在不同作用域之间正确解析符号。

```cpp
class SymbolTable {
public:
    std::unordered_map<std::string, std::shared_ptr<Symbol>> table;
    std::shared_ptr<SymbolTable> parent; // 指向父作用域的符号表

    SymbolTable(std::shared_ptr<SymbolTable> parent = nullptr)
        : parent(parent) {}

    // 在当前作用域查找符号
    std::shared_ptr<Symbol> lookup(const std::string &name){
      //···
    }

    // 向符号表中插入新的符号
    void insert(const std::string &name, std::shared_ptr<Symbol> symbol) {
      //···
    }
};

```

在符号解析过程中，我们会为每个作用域生成一个符号表，并随着进入和退出作用域对符号表进行管理。例如，在遇到函数定义时会创建一个新的局部符号表，当函数调用或变量引用时，会查找符号表以确保该符号已定义且在正确的作用域中。

#### 作用域管理

符号解析还需要管理作用域。通常在遇到新的作用域时（如函数、代码块、循环等），创建一个新的符号表，并在退出该作用域时销毁它。在解析过程中，确保每个符号在其可见的作用域内被正确解析。

```cpp
class SemanticAnalyzer {
public:
    std::shared_ptr<SymbolTable> currentScope;

    void enterScope() {
        currentScope = std::make_shared<SymbolTable>(currentScope);
    }

    void exitScope() {
        currentScope = currentScope->parent;
    }

    void declareVariable(const std::string &name, const std::shared_ptr<Symbol> &symbol) {
        currentScope->insert(name, symbol);
    }

    std::shared_ptr<Symbol> resolveVariable(const std::string &name) {
        return currentScope->lookup(name);
    }
};
```

通过 `enterScope()` 和 `exitScope()` 来管理作用域嵌套，当处理一个新的作用域（如函数或代码块）时，会创建新的符号表并进行相应的符号解析。

### 类型检查（typer）

类型检查的任务是确保程序中的所有操作符和操作数的类型兼容。例如，在算术表达式中，类型检查会确保运算符作用于正确的类型，并且操作数之间的类型一致。类型检查可以有效避免不合法的操作，如对整数进行除以字符串的运算。

#### 类型系统

编译器通常需要支持一套类型系统。类型系统包含基本类型（如整型、浮点型、布尔型等）和复杂类型（如指针、数组、结构体等）。类型检查器会根据这些类型系统对程序中的每个表达式、赋值和函数调用进行检查。

以下是一个简单的类型检查器示例：

```cpp
class TypeCheckerVisitor : public ASTVisitor {
public:
    std::shared_ptr<Type> visitBinaryExpr(BinaryExprNode *node) override {
        auto leftType = visit(node->left); // 检查左操作数的类型
        auto rightType = visit(node->right); // 检查右操作数的类型

        // 检查操作数的类型是否匹配
        if (!leftType->equals(rightType)) {
            throw std::runtime_error("Type mismatch in binary expression.");
        }

        // 返回表达式的类型
        return leftType;
    }

    std::shared_ptr<Type> visitVariableDecl(VariableDeclNode *node) override {
        // 检查变量声明的类型是否正确
        auto varType = node->type;
        if (!isValidType(varType)) {
            throw std::runtime_error("Invalid type for variable.");
        }

        return varType;
    }

    // 其他类型检查逻辑...
};
```

在该类型检查器中，我们遍历 AST 中的每个节点，检查其类型是否正确。例如，在二元表达式中，我们会检查左右操作数的类型是否匹配，并且确保运算符可以作用于该类型。此外，对于变量声明和函数调用等其他结构，也需要检查它们的类型。

#### *类型转换*

> 由于 MiniDecaf 只支持有限的数据类型，所以类型转换的部分可能并不需要实际实现。

类型检查的过程中，编译器有时需要进行类型转换。例如，将一个整数与浮点数进行加法运算时，编译器可能需要将整数提升为浮点数。编译器可以通过隐式类型转换来完成这类操作，但必须遵循一定的类型转换规则。

```cpp
class TypeCheckerVisitor : public ASTVisitor {
public:
    std::shared_ptr<Type> visitBinaryExpr(BinaryExprNode *node) override {
        auto leftType = visit(node->left);
        auto rightType = visit(node->right);

        // 进行隐式类型转换
        if (leftType->isInteger() && rightType->isFloat()) {
            leftType = floatType(); // 将整数提升为浮点数
        } else if (leftType->isFloat() && rightType->isInteger()) {
            rightType = floatType();
        }

        if (!leftType->equals(rightType)) {
            throw std::runtime_error("Type mismatch in binary expression.");
        }

        return leftType;
    }
};
```

通过检查和处理类型转换，我们确保程序的类型一致性，避免在运行时出现不可预知的错误。

### 预期目标

完成符号解析和类型检查后，编译器应该能够：

1. 通过符号表解析所有的变量和函数定义，确保它们在正确的作用域中被引用；
2. 检查所有的操作数和运算符的类型是否匹配；
3. 报告语义错误，如未定义的符号、类型不匹配等。

通过这些步骤，语义分析能够确保源代码符合语言的语义规则，为后续的中端优化和代码生成打下坚实的基础。

## 前端参考资料

- [Antlr 官方文档](https://www.antlr.org/)
- [MiniDecaf 教程](https://decaf-lang.github.io/)
- [编译原理经典书籍 Dragon Book](https://www.amazon.com/Compilers-Principles-Techniques-Tools-2nd/dp/0321486811)

## 前端预期目标

完成这部分内容后，你的编译器应该能够通过 Antlr 生成词法分析器和语法分析器，能够将 MiniDecaf 程序解析为抽象语法树（AST），并完成对 MiniDecaf 程序的语义分析。
