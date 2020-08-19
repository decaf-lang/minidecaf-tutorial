# lab8：循环

在这次试验中，我们将添加循环，要实现[C11标准](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)所说的迭代语句；如果你想参考标准本身，它们在6.8.5节。有一些不同的迭代语句。

### `for`循环

首先是一些术语。我将把 "for "循环头的三个部分称为*初始子句（initial clause）*、*控制表达式（controlling expression）*和*后表达式（post-expression）*，如。

```
for (int i = 0; // initial clause
     i < 10;    // controlling expression
     i = i + 1  // post-expression
     ) {
        // do something
}
```

`for`循环有两种风格：一种是初始语句是变量声明，另一种只是表达式。

第1种情况：

```
for (int i = 0; i < 10; i = i + 1) {
    // do something
}
```

第2种情况：

```
int i;
for (i = 0; i < 10; i = i + 1) {
    //do something
}
```

关于`for`循环的一个有趣的事情是，循环头中的任何一个表达式都可以是空的：

```
for (;;) {
    //do something
}
```

但如果控制表达式为空，编译器需要用一个常量非零表达式[1](https://norasandler.com/2018/04/10/Write-a-Compiler-8.html#fn1)来代替。所以上面的例子就相当于：

```
for (;1;) {
    //do something
}
```

### `while` 和 `do` 循环

下面是一些小的代码片段：

```
while (i < 10) {
    i  = i + 1;
}
do {
    i = i + 1;
} while (i < 10); // <- the semicolon is required!
```

### `break` 和 `continue`

"break "和 "continue "不是循环，但它们总是出现在循环中，用于控制循环的走向，所以现在添加它们是有意义的。C11标准称它们为 "跳转语句"，并在6.8.6节中定义了它们。

循环内部的 "break "语句会使执行跳转到循环的末端：

```
while (1) {
    break; // go to end of loop
}
// break statement will go here
```

`continue`语句会使执行跳转到循环体的末尾--紧接在for循环中的后表达式之前。

```
for (int i = 0; i < 10; i = i + 1) {
    if (i % 2)
        continue;
    // do something

    //continue statement will jump here
}
```

在上面的例子中，循环将执行10次，但只对i的奇数值 "做一些事情"。

###空语句

就像你可以在 "for "循环中使用空表达式一样，你也可以使用空语句（null statements）：

```
int a = 0;
; // does nothing
return a;
```

空语句其实和循环没有什么关系，但是它们和for循环中的表达式有一个共同的特点：它们都是用标准中的可选表达式（optional expression）来定义的。既然我们需要在for循环中支持可选表达式，那么也很容易添加对空语句的支持。

像往常一样，我们将依次更新词法分析、语法解析和代码生成过程。

## 词法分析

我们在这篇文章中增加了五个关键词。`for`, `do`, `while`, `break`和`continue`。这是目前我们所有的标记：

- `{`
- `}`
- `(`
- `)`
- `;`
- `int`
- `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`
- `-`
- `~`
- `!`
- `+`
- `*`
- `/`
- `&&`
- `||`
- `==`
- `!=`
- `<`
- `<=`
- `>`
- `>=`
- `=`
- `if`
- `else`
- `:`
- `?`
- **`for`**
- **`while`**
- **`do`**
- **`break`**
- **`continue`**

#### ☑ 任务

更新*lex*函数以处理新的标记。它应该适用于测试套件中的所有step[1-8]的例子。

## 语法解析

我们增加了六种语句。`do`循环、`while`循环、两种不同的`for`循环、`break`和`continue`。我们还改变了`Exp`语句，它的参数现在是可选的，所以我们可以用它来表示空语句。现在我们可以像这样在AST中构造一个空语句：

```
null_exp = Exp(None)
```

`for`循环中的初始表达式和后表达式也是可选的。

下面是AST中语句的最新定义，新的和改变的部分如下表示：

```
statement = Return(exp) 
          | Exp(exp option)
          | Conditional(exp, statement, statement option) // exp is controlling condition
                                                          // first statement is 'if' block
                                                          // second statement is optional 'else' block
          | Compound(block_item list)
          | For(exp option, exp, exp option, statement) // initial expression, condition, post-expression, body
          | ForDecl(declaration, exp, exp option, statement) // initial declaration, condition, post-expression, body
          | While(expression, statement) // condition, body
          | Do(statement, expression) // body, condition
          | Break
          | Continue
```

> 注意，这里的AST允许 "break "和 "continue "语句出现在循环之外，尽管这是不合法的；我们可在代码生成过程中发现这个错误，而不是解析。

这里语法中最棘手的部分是处理可选表达式。我通过定义一个`<exp-option>`符号来处理这个问题：

```
<exp-option> ::= <exp> | ""
```

一旦我们添加了这些，更新语句的语法就非常容易了。

```
<statement> ::= "return" <exp> ";"
              | <exp-option> ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]
              | "{" { <block-item> } "}
              | "for" "(" <exp-option> ";" <exp-option> ";" <exp-option> ")" <statement>
              | "for" "(" <declaration> <exp-option> ";" <exp-option> ")" <statement>
              | "while" "(" <exp> ")" <statement>
              | "do" <statement> "while" <exp> ";"
              | "break" ";"
              | "continue" ";"
```

如果你想知道为什么第一条 "for "产生式规则中的初始`<exp-option>`后面有一个分号，而第二条产生式规则中的初始`<declaration>`后面却没有，这是因为`<declaration>`的规则也包含一个分号。

解析`<exp-option>`并不很直接的，因为空字符串其实并不是一个标记。目前处理这个问题的方法是向前看，看看下一个标记是右括号--close paren（在后表达式（post-expression）之后）还是分号--semicolon （在语句（statement）、后表达式（post-expression）或控制条件（controlling condition）之后）。如果是右括号，则表达式为空；如果不是，则表达式不为空。

这种方法违反了一些关于无上下文语法和LL解析器的形式主义：为了解析一个`<exp-option>`符号，你可能不得不看一个在这个符号之后的标记。这实际上不是一个问题，但如果它困扰着你，你可以重构语法来避免它。

```
<exp-option-semicolon> ::= <exp> ";" | ";"
<exp-option-close-paren> ::= <exp> ")" | ")"
<statement> ::= ...
                | <exp-option-semicolon> // null statement
                | "for" "(" <declaration> <exp-option-semicolon> <exp-option-close-paren> ")" <statement>
...
```
请注意，这里的语法和AST定义之间有一个差异；语法允许 "for "循环中的控制表达式为空，但AST不允许。这是因为，正如前面提到的，一个空的控制表达式需要用一个非零的常量来代替。所以我们解析`for`循环中控制表达式的方法是这样的：
```
match parse_optional_exp(controlling_expression) with
| Some e -> e
| None -> Const(1) // construct a constant nonzero expression
```

如果你想的话，你可以在代码生成阶段而不是在解析阶段进行上述处理。

#### ☑ Task:

更新语法解析过程以处理循环。它应该成功地解析所有step[1-8]的例子。

## 代码生成

### 空语句

对空语句的代码生成过程很简单，即不要为空语句生成任何汇编。

### `while`循环

给定一个`while`循环：

```
while (expression)
    statement
```

我们可以这样描述它的代码生成控制流程：

1. 评估`expression`
2. 如果是假的，跳到步骤5
3. 执行`statement`
4. 跳到步骤1
5. 完成

在这里就展示需要生成的具体汇编了，现在你已经知道了，可以自己想办法（如使用GCC等）了。最主要的是给步骤1和步骤5打上标签（label），这样当我们需要跳转指令时，就有地方可以跳转了。值得注意的是，循环体（loop body）是一个新的作用域，你需要相应地重新设置你的`current_scope`集合。

### `do`循环

这些循环基本上和`while`循环一样，只是在语句后评估表达式。

### `for`循环

给出这样一个`for`循环：

```
for (init; condition; post-expression)
    statement
```

我们可以用类似上面`while`循环的方法来分解代码生成控制流程：

1. 评估`init`
2. 评估`condition`
3. 如果是假的，跳到步骤7
4. 执行`statement`
5. 执行`post-expression`
6. 跳到步骤2
7. 完成

`init`和`post-expression`可能是空的，在这种情况下，我们只是不为步骤1和步骤5产生任何汇编。请注意，"for "循环，包括头，是一个有自己作用域（scope）的块（block），而 "for "循环的*体（body）*也是一个块（block）。这意味着你可以有这样的代码：

```
int i = 100; // scope 1
for (int i = 0; i < 10; i = i + 1) { // scope 2 - variable i shadows previous i
    int i; //scope 3 - this variable i shadows BOTH previous i's
}
```

这里的主要问题是，当你退出代码块时，你需要把在`init`中声明的变量从堆栈中弹出，就像你在上一篇文章中需要处理释放其他变量一样。

### `break`和`continue`语句

我们可以用一条jmp指令实现这两条语句——关键是找出跳转到哪里。一个break语句 "终止执行最小的包围`switch`或迭代语句"，所以我们要跳转到循环之后的那个位置。我们已经有了一个 "循环结束 "标签，当控制条件为false时，我们就会跳转到这个标签；我们只需要将这个标签与变量映射表、堆栈索引和当前作用域一起传递给代码生成逻辑即可。

我们还需要传递另一个标签给`continue`来参考。`continue`"导致跳转到最小包围迭代语句的循环-继续部分；也就是跳转到循环体的末端")--也就是上面`while`循环中的第4步或`for`循环中的第5步。

与栈索引、变量映射等不同，如果你不在一个循环里面，跳转和继续标签可以是空的。当这些标签为空时，打一个`break`或`continue`语句，应该会引起错误。

> 提示：在代码生成逻辑中，需要传递足够多的参数。为简化参数传递，可定义一个`Context`类型，并将要传递的参数其全部封装在其中。你可能想做类似的事情，但你不必这样做。

## 下一步

在下一个实验中，我们将实现一个很基本的概念。**函数调用**。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)