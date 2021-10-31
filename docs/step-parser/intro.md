# 实验指导 parser-stage：自顶向下语法分析器

 在 Stage1-2 中，实验框架使用了 bison（C++ 框架）或 ply（Python 框架）作为语法分析器，解析 MiniDecaf 程序并生成 AST。

在 parser-stage 中，我们将结合课堂上学习的 LL(1) 分析方法，完成一个**手工实现的递归下降**语法分析器。为了降低难度和工作量，将提供分析器的基本框架和部分实现，同学们只需要补全代码片段即可。所实现的手工语法分析器，只需要支持 [**Step1-6 的语法**](spec.md)。

## 准备工作


parser-stage 不涉及中端、后端部分，所以请同学们将 stage2 中完成的中后端代码合并到 parser-stage 的实验框架上。具体的操作可以参考如下步骤：

```bash
$ git switch parser-stage
$ git merge stage-2
```

（本步骤所需要的额外文件请在[此处](https://cloud.tsinghua.edu.cn/d/9b34fdf53a3c48b8bc52/)获取，C++ 的文件在 cpp/ 下，Python 的文件在 python/ 下）

**对于 C++ 框架**，在切换到 `parser-stage` 分支之后进行如下操作：

1. 将[链接](https://cloud.tsinghua.edu.cn/d/9b34fdf53a3c48b8bc52/)中的 `my_parser.hpp` 及 `my_parser.cpp` 放入 `src/frontend/` 中。
2. 使用上述链接中的 `scanner.l` 覆盖原有的 `scanner.l`。
3. 对于 `src/Makefile` 和 `src/compiler.hpp` 的修改分为以下两种情况：
   1. 如果你没有修改过 `Makefile` 和 `compiler.hpp` ，直接使用上述链接中的同名文件覆盖即可。
   
   2. 如果做过修改，请按照下述方法在文件中添加相关内容：
   
        ```C++
        // compiler.hpp
        1. #include "parser.hpp" 修改为 #include "frontend/myparser.hpp"
        2. 删除 #define YY_DECL yy::parser::symbol_type yylex()
        3. 删除 YYDECL;
        
        // Makefile
        1. 删除 YACC = bison
        2. 删除 YFLAGS = -dv
        3. 在 LEXCFLAGS = -O $(CFLAGS) 之前加上 LFLAGS = -8
        4. 删除 PARSER  = parser.cpp parser.hpp location.hh position.hh stack.hh
        5. FRONTEND = scanner.o parser.o 修改为 FRONTEND = scanner.o frontend/myparser.o
        6. 删除 $(PARSER): frontend/parser.y $(YACC) $(YFLAGS) $<
        7. parser.o: config.hpp 3rdparty/boehmgc.hpp define.hpp 3rdparty/list.hpp 修改为 frontend/myparser.o: config.hpp 3rdparty/boehmgc.hpp define.hpp 3rdparty/list.hpp frontend/myparser.hpp frontend/myparser.cpp
        8. parser.o: error.hpp ast/ast.hpp location.hpp compiler.hpp 修改为 frontend/myparser.o: error.hpp ast/ast.hpp location.hpp compiler.hpp
        9. scanner.o: error.hpp ast/ast.hpp parser.hpp location.hpp 修改为 scanner.o: error.hpp ast/ast.hpp frontend/myparser.hpp location.hpp
        ```

**对于 Python 框架**，在切换到 `parser-stage` 分支之后，从[链接](https://cloud.tsinghua.edu.cn/d/9b34fdf53a3c48b8bc52/)下载 python 目录下的文件，并使用 `frontend/parser/` 目录整个替换你 stage2 代码的对应目录，然后在整体框架上完成实验。

**需要注意的是**，parser-stage 的实验相对于其他 stage 是独立的。在后续进行 stage3 的实验时，应从 stage2 所完成的代码开始，而不需要用 parser-stage 的代码。未来在进行 stage3 实验时，建议进行如下操作：

```bash
$ git switch stage-3
# 注意不要从 parser-stage merge
$ git merge stage-2
```

## 背景知识

如果你已经很熟悉自顶向下语法分析、自底向上语法分析的原理，可以跳过这部分。这里我们只对两种语法分析方法进行简单介绍，**详细原理请参考课件**。

bison/ply 自动生成的语法分析器，属于 LALR(1) 语法分析，是**自底向上**的语法分析方法。
     
具体来说，维护一个栈（保存状态和符号），每一步操作如果是移进（shift）操作，则将新的 token 加入栈顶；如果是规约（reduce）操作，则依据规约对应的产生式的右端，将栈顶的状态和符号依次弹出，然后将产生式左端的非终结符（以及对应转移到的状态）入栈。根据规约的结果，从语法树的最底层开始，自底向上构建 AST 结点，最终得到整个 AST。


而**递归下降**语法分析的过程是:

从文法开始符号（对应 AST 的根结点）起，通过预测集合 PS（实际实现中，为了简便，直接采用了 First 集和 Follow 集）以及输入符号，选择对应的产生式。对于产生式右侧的非终结符和终结符分别进行不同的操作，对于非终结符通过调用递归函数进行处理，对于终结符通过 matchToken（实际实现中，用lookahead函数实现） 进行处理。由于在递归下降分析的过程中，只有分析完叶子结点后，才会返回，所以实际的 AST 构造过程也是自底向上构建 AST 结点，最终得到整个 AST。


## 任务描述

要求：
1. 使用所提供的 parser-stage 框架替换你的编译器中的 parser 部分，完善框架中的实现，**通过 Step1-6 的测试**。
2. 本步骤需要修改的代码均有 `TODO` 标识，并有相关的引导注释。其中 C++ 框架需要修改的文件为 `src/frontend/my_parser.cpp`，Python 框架需要修改的文件为 `frontend/parser/my_parser.py`。
3. 完成实验报告（具体要求请见实验指导书的首页）。