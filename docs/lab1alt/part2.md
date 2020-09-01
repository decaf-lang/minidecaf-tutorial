# 实验指导 step1：词法语法分析工具
第一部分中，我们已经自己从零开始暴力实现了一个编译器，接下来我们就来改进它。
第一个方向是： **使用工具完成词法语法分析，而不是自己手写** 。

当然你可以自己写 lexer 和 parser，但你就需要理解 lexer 和 parser 的算法，并且代码量更大。
请直接看[手写 lexer 和 parser](#手写 lexer 和 parser)。

## 工具概述
从 minilexer/miniparser 的代码可以看出，lexer 和 parser 包含两部分：
1. 被分析的词法/语法的描述。例如 minilexer 的那个 `TokenType` 列表，以及 miniparser 的 `rules` 字符串；
2. lexer 和 parser 的驱动代码。例如 `lex` 和 `parse` 函数。

使用工具，我们只需要完成第一步，描述被分析的词法或者语法。
然后工具从我们的描述，自动生成 lexer 或者 parser 供你使用，十分方便。

> 所以这类工具被称为 lexer/parser generator，例子有：C 的 lex/yacc、往届使用的 JFlex / Jacc、mashplant 助教自己写的 lalr1。
>
> 对有兴趣的同学：除了这类工具以外，还有一类工具称为 parser combinator，多在函数式语言中使用。
> 最有名的如 Haskell 的 parsec、scala 的 fastparse，rust 的 nom。课程不涉及其中内容。

下面是助教写的一些工具的速成介绍，你可从中选择一个学习使用，
你也可以自己另找其他工具自学使用。

## ANTLR
ANTLR 是一个比较易用的 parser generator，速成文档在[这里](./antlr.md)。

## LALR1
TODO：如果较长，写在单独的文档里面

## 手写 lexer 和 parser
TODO：如果较长，写在单独的文档里面


# 任务
1. **如果你选择使用工具**：按照你选择的工具，描述 step1 的 MiniDecaf 词法语法，并从 AST 生成汇编。
2. **如果你不选择使用工具**：实现你自己的 lexer 和 parser，并生成汇编。
