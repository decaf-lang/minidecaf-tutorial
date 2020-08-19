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