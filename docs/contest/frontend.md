# 前端梗概

前端的主要任务是将源代码转换为抽象语法树（Abstract Syntax Tree, AST），为中端和后端生成中间表示和目标代码提供基础。在这个过程中，前端会经历词法分析、语法分析、语义分析等多个步骤。

# 词法分析与语法分析

词法分析的任务是将源代码转换为一系列的符号（token），每个符号代表源代码中的一个最小单位，如关键词、标识符、操作符等。词法分析器会忽略空格、注释等非必要信息，并在此过程中进行基本的错误检测（如非法字符）。

### Antlr简介

Antlr 是一个功能强大的解析器生成器，能够根据给定的语法规则自动生成词法分析器和语法分析器。Antlr 支持多种语言，包括 Java、Python 和 C++。通过定义语法文件（.g4 文件），Antlr 能够帮助我们生成解析源代码所需的词法分析和语法分析工具。

在这个项目中，我们推荐使用 Antlr 来处理 MiniDecaf 的词法分析和语法分析部分。

## 第一部分:依赖环境准备

ANTLR 工具需要 JVM 才能执行；另一方面，为了方便使用 grun，你需要一个能够编译 java 源文件的环境。因此，你需要一个完整的 Java Development Kit。

直接使用包管理器安装

```bash
sudo apt install openjdk-19-jdk
```

### 1.获取antlr

你需要从 [ANTLR Download](https://www.antlr.org/download.html) 下载 `antlr-4.13.2-complete.jar`(截至文档写作时此为最新版)。

然后，你需要将该jar包的路径加入到环境变量 `CLASSPATH` 中，注意将下面`/path/to/your/`改为你的路径

```
export CLASSPATH=".:/path/to/your/antlr-4.13.2-complete.jar:$CLASSPATH"
```

> 最好将它加到`bashrc`中（对于bash）,以避免每次打开终端时需要重新配置。

##### 检查

在命令行中输入

```bash
java org.antlr.v4.Tool
```

你应该可以看见`ANTLR Parser Generator  Version 4.13.2`以及一些帮助信息,这说明可以正确使用antlr了.

### 2. antlr4 和 grun 工具

可以定义别名 `antlr4` 表示 ANTLR 工具，即

```bash
alias antlr4='java org.antlr.v4.Tool'
```

这样，你可以直接使用 `antlr4 your.g4` 来为your.g4 生成解析器源码。

ANTLR 的运行时库中还提供了一个灵活的测试工具 `TestRig`，它可以显示解析器如何匹配输入的许多相关信息。`TestRig`使用Java的反射机制来调用编译过的解析器。为了方便用户使用，ANTLR 提供了一个 `grun` 工具来使用 `TestRig`。

`grun` 本质上是一个别名，可以定义如下：

```bash
alias grun='java org.antlr.v4.runtime.misc.TestRig'
```

或

```bash
alias grun='java org.antlr.v4.gui.TestRig'
```

同样的，你可以将这些别名命令加入到`.bashrc`，以节省你配置和使用的时间。

### 3. ANTLR 运行时的编译链接

#### 1. 安装 ANTLR 运行时库

ANTLR 运行时库是解析器生成的代码在运行时所依赖的代码。对于 C++，你可以从 [ANTLR4 runtime Cpp的 GitHub 仓库](https://github.com/antlr/antlr4/tree/master/runtime/Cpp)下载预编译的库或者自己编译安装。但是官方的CMAKE脚本会从官方 git 仓库下载 ANTLR C++ 运行时并构建它，你在编译过程中很可能会因为网络等问题而失败，如果难以解决，可以直接clone [ANTLR 运行时库的 C++ 源代码](https://www.antlr.org/download/antlr4-cpp-runtime-4.13.2-source.zip)到你的代码仓库里，并为你的整个项目编写一个CMAKE文件(**强烈建议**)。处于方便考虑，我在这里给出一个可能的项目结构与CMAKE文件实例.

- **项目结构**

  ```
  example-tree/
  ├── 3rd_party/
  │   └── antlr4-runtime/          # 第三方库ANTLR运行时目录(在源码的src目录下)
  │       ├── CMakeLists.txt      # antlr4-runtime的CMake配置文件,需要你手动添加一个
  │       └── antlr4-runtime.h
  │       └── antlr4-common.h
  │       └── ...
  ├── CMakeLists.txt               # 根目录下的CMake配置文件
  └── src/                         # 源代码目录
      ├── frontend/                # 前端代码目录
      │   ├── lexer/               # 词法分析相关代码
      │   │   └── *.cpp           # 词法分析器源文件
      │   │   └── *.h             # 词法分析器头文件
      │   ├── parser/              # 语法分析相关代码
      │   │   └── *.cpp           # 语法分析器源文件
      │   │   └── *.h             # 语法分析器头文件
      │   └── ast/                 # 抽象语法树相关代码
      │       ├── *.cpp            # AST源文件
      │       ├── *.h              # AST头文件
      ├── backend/                  # 后端代码目录
      ├── midend/                   # 中间代码目录
      └── main.cpp                 # 程序入口文件
  ```

- 对应的`CMakeLists.txt`

  ```cmake
  # 指定CMake的最小版本要求
  cmake_minimum_required(VERSION 3.10)
  
  # 设置项目名称和使用的语言（CXX代表C++）
  project(my_compiler CXX)
  
  # 设置C++标准为C++17
  set(CMAKE_CXX_STANDARD 17)
  
  # 设置C++编译器标志，这里没有额外添加，使用默认
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
  
  # 设置调试模式下的编译器标志，开启DEBUG宏
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")
  
  # 使用GLOB_RECURSE模式递归查找src目录下所有的.cpp文件
  file(GLOB_RECURSE SRC "src/*.cpp")
  
  # 添加项目的src目录到头文件搜索路径
  include_directories(src)
  
  # 添加第三方库目录antlr4-runtime到头文件搜索路径
  include_directories(3rd_party/antlr4-runtime)
  
  # 添加antlr4-runtime子目录作为子项目进行构建
  add_subdirectory(3rd_party/antlr4-runtime)
  
  # 创建名为my_compiler的可执行文件，将所有源文件编译链接到这个可执行文件中
  add_executable(my_compiler ${SRC})
  
  # 将antlr4_runtime库与my_compiler可执行文件链接
  target_link_libraries(my_compiler antlr4_runtime)
  ```

- **为antlr4-runtime添加一个相应的`CMakeLists.txt`**

```cmake
# 3rd_party/antlr4-runtime/CMakeLists.txt
file(GLOB_RECURSE ANTLR4_SRC "*.cpp")

add_library(antlr4_runtime STATIC ${ANTLR4_SRC})
```

- `<somepath>`是你指定的安装目录,你也可以不指定`<DESTDIR>`,直接安装到系统。

## 第二部分：文法文件的编写与parse tree的生成

终于，在上一部分中，我们完成了项目的环境准备工作，可以着手开始编写代码了。在这一节中，我们会开始编写一个简单的C语言子集`simpleC`的文法文件`simpleC.g4`，并利用它生成一个`parse tree`.最终把一个简单的c语言程序`test.c`转换为一个`parse tree`

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

  

### 1.编写simpleC.g4

> todo:如何编写一个ANTLR文法文件.

`.g4` 文件是 ANTLR (Another Tool for Language Recognition) 使用的文法文件，用于定义语言的语法规则。它使用基于上下文的语法规则来描述语言的结构。一个典型的 `.g4` 文件包含以下几个部分：

1. **语法定义**：声明语法的名称，这是识别语法文件的关键字。这个语法名称必须要和包含这个语法的文件名完全相同(甚至包括大小写,因为ANTLR是对大小写敏感的)
2. **规则**：定义语言中各种结构的模式。
3. **词法规则**：定义词法单元（如关键字、标识符、符号等）。
4. **忽略规则**：通常用来忽略空格、换行等空白字符。
5. **操作**：在规则中嵌入的代码，用于在解析过程中执行特定的动作。

### 示例 `.g4` 文件结构

```antlr
// 文件名: SimpleC.g4

grammar SimpleC; //语法定义

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
expression: expression PLUS expression # AddExpr
           | expression MINUS expression # SubExpr
           | expression MUL expression # MulExpr
           | expression DIV expression # DivExpr
           | '(' expression ')' # ParenExpr
           | INT # IntExpr
           | ID # ID
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

### 2.使用文法文件生成lexer&parser

在确认环境配置无误后,我们可以使用ANTLR+文法文件生成所需的lexer&parser,只需要执行

```bash
antlr4 -Dlanguage=Cpp -no-listener -visitor -o src/frontend/lexer_parser simpleC.g4
```



`-no-listener` 和` -visitor `选项分别用于停止生成`listener`（默认是激活的）和激活`visitor`模式。如果你还不知道`visitor`是什么，不用担心，我们稍后会看到。

-o 选项用于设置输出目录。我们将在`src/frontend/lexer_parser`目录中输出生成的代码。

### 3.使用lexer&parser

现在我们可以看到如何在 C++ 程序中使用我们生成的解析器。

```cpp
//src/main.cpp
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
- 我们使用词法分析器产生一个token流
- 我们创建一个在令牌流上工作的解析器
- 然后，21 行使用解析器的一个方法，该方法对应于语法规则中的一个，以获得规则匹配的第一个节点。在我们的例子中，只有一个节点`program`，这是因为我们定义规则的方式。然而，原则上那可以是任意的，每次你调用相应的方法，你都会得到一个相应的结果。

现在，使用cmake构建运行我们自己实现的编译器。你将会看到一个`parse tree`

```bash
./my_compiler test.c
```

总得来说,我们现在利用ANTLR实现了词法分析器分析输入（即字符）并产生token，然后解析器分析token以产生`parser tree`。这样，我们就把一个看似被复杂地组织起来的文本转化成了一个“树”，有了“树”之后我们就可以各种花式遍历这个树并对这个树的每个节点进行一些操作，如何遍历呢？我们用到了`Visitor`模式。

## 第三部分:ast的生成

## Visitor模式代码的编写方法

在编写编译器时，我们通常使用 Visitor 模式来遍历和处理 AST。Visitor 模式提供了一种解耦的方式来在不同的节点上执行操作。通过定义 Visitor 类，我们可以根据 AST 的不同节点执行特定的逻辑操作。

在 Antlr 中，Visitor 类会根据语法文件中的每个语法规则生成对应的函数，例如：

```java
public class MiniDecafVisitor extends MiniDecafBaseVisitor<Void> {
    @Override
    public Void visitAddSub(MiniDecafParser.AddSubContext ctx) {
        // 处理加法和减法操作
        return null;
    }
}
```

通过覆写`BaseVisitor`中的这些函数，我们可以实现对`parse tree`的递归遍历和处理，生成AST或执行静态检查。

## 第四部分 语义分析

### 符号解析（namer）

### 类型检查（typer）

## 前端参考资料

- [Antlr 官方文档](https://www.antlr.org/)
- [MiniDecaf 教程](https://decaf-lang.github.io/)
- [编译原理经典书籍 Dragon Book](https://www.amazon.com/Compilers-Principles-Techniques-Tools-2nd/dp/0321486811)

## 预期目标

完成这部分内容后，你的编译器应该能够通过 Antlr 生成词法分析器和语法分析器，并能够将 MiniDecaf 程序解析为抽象语法树（AST）。
