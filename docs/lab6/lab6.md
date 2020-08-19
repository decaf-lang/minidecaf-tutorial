
# lab6：条件语句&条件表达式

本次实验将实现条件语句和表达式：

1. 条件语句（Conditional statements），又称 "if "语句
2. 三元条件表达式（Ternary conditional expression），其形式为`a ? b : c`

###  条件语句

一个 "if "语句由一个条件（condition）、一个如果条件为真则执行的子语句（substatement ）和另一个如果条件为假则执行的子语句组成。这些子语句中的任何一个都可以是一个单一的语句，比如：

```
if (flag)
  return 0;
```

或一个复合语句（compound statement），像这样：

```
if (flag) {
  int a = 1;
  return a*2;
}
```

添加对复合语句的支持是位于后续试验中的一项不同的任务，我们不会在本次实验中处理。所以现在，我们只支持上面第一个例子，不支持第二个例子。

我们说一个条件，如果它的值为`0`，那它就是**false**，否则就是**true**，就像我们在前面实验中实现布尔运算符一样。

#### Else If

注意，C语言没有明确的`else if`结构。如果一个`if`关键字紧跟在`else`关键字之后，整个`if`语句会被解析为`else`分支。换句话说，下面的代码片段是等价的：

代码片段1：
```
if (flag)
    return 0;
else if (other_flag)
    return 1;
else
    return 2;
```
代码片段2：
```
if (flag)
    return 0;
else {
    if (other_flag)
        return 1;
    else
        return 2;
}
```

### Conditional Expressions

这些表述的形式如下：

```
a ? b : c
```

如果`a`为真，表达式将评估为`b`；否则将评估为`c`。

> 注意，我们应该只执行我们实际需要的表达式。

在下面的代码片段中：
```
0 ? foo() : bar()
```

函数`foo`永远不应该被调用。你可能会想同时调用`foo`和`bar`，然后丢弃`foo`的结果，但这是错误的；`foo`可能会打印到控制台，进行网络调用，或取消引用一个空指针并使程序崩溃。显然这一点对于`if`语句也是正确的--我们应该执行`if`分支或`else`分支，但绝对不能同时执行。

条件表达式和`if`语句可能看起来非常相似，但需要记住，语句和表达式的使用方式完全不同。例如，表达式有一个值，但语句没有。所以下面的代码是合法的：

```
int a = flag ? 2 : 3;
```

但这下面的代码不合法：

```
//this is bogus
int a = if (flag)
            2;
        else
            3;
```

另一方面，一个语句可以包含其他语句，但一个表达式不能包含语句。例如，你可以在一个`if`语句中嵌套一个`return`语句：

```
if (flag)
    return 0;
```

但你不能在条件表达式中使用`return`语句：

```
//this is also bogus
flag ? return 1 : return 2;
```

## 词法分析

我们需要再定义一些标记："if "和 "else "关键字用于 "if "语句，加上": "和"? "运算符用于条件表达式。下面是全部标记的列表，新的标记在底部用粗体表示：

- Open brace `{`
- Close brace `}`
- Open parenthesis `(`
- Close parenthesis `)`
- Semicolon `;`
- Int keyword `int`
- Return keyword `return`
- Identifier `[a-zA-Z]\w*`
- Integer literal `[0-9]+`
- Minus `-`
- Bitwise complement `~`
- Logical negation `!`
- Addition `+`
- Multiplication `*`
- Division `/`
- AND `&&`
- OR `||`
- Equal `==`
- Not Equal `!=`
- Less than `<`
- Less than or equal `<=`
- Greater than `>`
- Greater than or equal `>=`
- Assignment `=`
- **If keyword `if`**
- **Else keyword `else`**
- **Colon `:`**
- **Question mark `?`**

#### ☑任务

更新*lex*函数以处理新的标记。它应该适用于测试套件中的所有step[1-6]的例子。

## 语法解析

我们将对条件表达式和`if`语句进行完全不同的解析。让我们先处理`if`语句。

### If 语句

到目前为止，我们已经在AST中定义了三种类型的语句：返回语句、表达式和变量声明。现在的定义是这样的：

```
statement = Return(exp) 
          | Declare(string, exp option) //string is variable name
                                        //exp is optional initializer
          | Exp(exp)
```

我们需要添加一个 "if "语句，它有三个部分：一个表达式（控制条件）、一个 "if "分支和一个可选的 "else "分支。下面是我们更新后的语句AST定义：

```
statement = Return(exp) 
          | Declare(string, exp option) //string is variable name
                                        //exp is optional initializer
          | Exp(exp)
          | If(exp, statement, statement option) //exp is controlling condition
                                                 //first statement is 'if' branch
                                                 //second statement is optional 'else' branch
```

现在让我们更新一下语法。`if`语句的规则包括：

- `if`关键字
- 括号内的表达式（条件）
- 语句(如果条件为真，则执行)
- 可选择使用`else`关键字，接着是另一条语句（如果条件为假，则执行）

```
"if" "(" <exp> ")" <statement> [ "else" <statement> ]
```

所以更新后的语句语法是这样的：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "int" <id> [ = <exp> ] ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]
```

我们对语句的定义是递归的，但它不是左递归的，所以这不是问题。

但是我们还有一个问题。我们把变量声明定义为语句的一种类型，但是C语言中的声明**不是语句**。例如，这段代码是无效的：

```
//this will throw a compiler error!
if (flag)
  int i = 0;
```

当我们在以前的实验中添加了变量声明时，是否将它们定义为语句并不重要；无论哪种方式，我们都可以解析相同的C子集并生成相同的汇编。现在我们正在处理更复杂的结构，比如`if`语句，这种简化会影响我们可以和不可以解析的内容，所以我们需要修正它。

因此，我们需要把`Declare`从`statement`类型中移出，变成自己的类型。但是这又带来了一个新的问题：我们把函数体定义为一个语句列表，但是如果声明不是语句，那么在函数体中就不能有声明。为了解决这个问题，我们需要调整我们在AST中定义函数的方式。让我们介绍一些术语：

- 一个**block item **是一个语句（statement ）或声明（declaration）
- 一个**block **或**compound statement**是一个用大括号包裹的**block item **列表

函数体（Function bodies ）只是**block **的一种特殊情况，它们包含了一个声明（declarations ）和语句（statements）的列表。为了表示它们，我们将引入一个新的`block_item`类型，它可以包含一个语句或一个声明。当我们在接下来的实验中添加对一般**block **的支持时，这也会很方便。有了这些变化，我们AST的相关部分就会像这样：

```
statement = Return(exp)                                         
          | Exp(exp)
          | Conditional(exp, statement, statement option) //exp is controlling condition
                                                          //first statement is 'if' block
                                                          //second statement is optional 'else' block

declaration = Declare(string, exp option) //string is variable name 
                                          //exp is optional initializer

block_item = Statement(statement) | Declaration(declaration)

function_declaration = Function(string, block_item list) //string is the function name                                                                                      
```

这是更新后的语法：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]
<declaration> ::= "int" <id> [ = <exp> ] ";"
<block-item> ::= <statement> | <declaration>
<function> ::= "int" <id> "(" ")" "{" { <block-item> } "}"
```

现在我们有了AST和语法，你应该可以更新你的编译器来解析条件语句。

#### ☑ 任务

更新解析阶段代码以处理条件语句。它应该能成功地解析所有step[1-6]的例子。

### 条件表达式

现在让我们添加三元条件表达式。下面是我们到目前为止如何定义表达式的AST：

```
exp = Assign(string, exp)
    | Var(string) //string is variable name
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

直接添加一个 "Conditional "形式就可以了：

```
exp = Assign(string, exp)
    | Var(string) //string is variable name
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
    | Conditional(exp, exp, exp) //the three expressions are the condition, 'if' expression and 'else' expression, respectively
```

我们还需要更新表达式的语法产生式，目前是这样的：

```
<exp> ::= <id> "=" <exp> | <logical-or-exp>
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> } 
...more rules...
```

条件操作符的优先级比赋值（`=`）低，但比逻辑或（`||`）高，而且它是右结合的。我们可以直接从[C11标准](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf)的6.5.15节中提取其语法规则：

```
<conditional-exp> ::= <logical-or-exp> "?" <exp> ":" <conditional-exp>
```

我们想想为什么要这样定义。我把这三个子表达式称为**e1**、**e2**和**e3**，这样一个条件表达式的形式是`e1 ? e2 : e3`。表达式**e1**必须是一个`<logical-or-exp>`，因为它不能是赋值表达式（assignment expression）或条件表达式（conditional expression）。它不能是赋值表达式的原因是由于赋值的优先级比条件操作符低。换句话说：

```
a = 1 ? 2 : 3;
```

应该解析为：

```
a = (1 ? 2 : 3);
```

在我们目前的语法中，这是毫不含糊地指定的，但如果我们将条件表达式定义为：

```
<conditional-exp> ::= <exp> "?" <exp> ":" <conditional-exp>
```

那么就会有歧义；上面的说法也可以解析为：

```
(a = 1) ? 2 : 3;
```

请注意，`(a = 1) ? 2 : 3;`是一个有效的语句，但是你需要用括号来解析它。

所以这就是为什么**e1**不能成为赋值表达式的原因。它不能是条件表达式，因为`?`是右结合的。换句话说：

```
flag1 ? 4 : flag2 ? 6 : 7
```

应该解析为：

```
flag1 ? 4 : (flag2 ? 6 : 7)
```

如果我们把条件表达式定义为：

```
<conditional-exp> ::= <conditional-exp> "?" <exp> ":" <conditional-exp>
```

那么上面的例子也可以解析为：

```
(flag1 ? 4 : flag2) ? 6 : 7
```

语法上就会有歧义。

在我们的三元条件中，表达式**e2**可以采取任何形式；在`?`和`:`的安全保护下，它不能引入任何语法上的歧义。你可以认为隐式圆括号包裹了`?`和`:`之间的所有内容。

表达式**e3**可以是另一个三元条件，如例`a > b ? 4 : flag ? 6 : 7`. 但它不能是一个赋值语句--为什么不能呢？让我们看看下面的例子：

```
flag ? a = 1 : a = 0
```

如果我们尝试用GCC编译，我们会得到类似下面的错误信息：

```
error: expression is not assignable
    flag ? a = 1 : a = 0;
    ~~~~~~~~~~~~~~~~ ^
```

换句话说，gcc试图解析这样的表达式：

```
(flag ? a = 1 : a) = 0
```

这显然是行不通的，因为左边的表达式不是一个变量。你可能会奇怪为什么我们不能使用下面的语法规则：

```
<conditional-exp> ::= <logical-or-exp> "?" <exp> ":" <exp>
```

那么gcc可以这样解析：

```
flag ? a = 1 : (a = 0)
```

这个语法规则会很好用；事实上，C++中就是这样定义条件表达式的。我们不知道为什么在C中不一样，但如果你知道的话，我们想听听你的观点。

我们还需要一种方法来指定不是条件表达式的表达式，所以我们将把这个语法规则中的 "条件 "部分变成可选的：

```
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]
```

总之，我们现在知道了正确的语法。下面是所有关于表达式的新的和更新的语法规则：

```
<exp> ::= <id> "=" <exp> | <conditional-exp>
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> } 
...
```

#### ☑任务

更新语法解析过程以处理三元条件表达式。在这一点上，它应该成功地解析所有step[1-6]的例子。

### 整合

为了完整起见，这里是我们AST的完整定义和语法，新的和改变的部分用粗体表示：

AST：

```
program = Program(function_declaration)

function_declaration = Function(string, block_item list) //string is the function name

block_item = Statement(statement) | Declaration(declaration)

declaration = Declare(string, exp option) //string is variable name 
                                          //exp is optional initializer

statement = Return(exp) 
          | Exp(exp)
          | Conditional(exp, statement, statement option) //exp is controlling condition
                                                          //first statement is 'if' block
                                                          //second statement is optional 'else' block
                                                          
exp = Assign(string, exp)
    | Var(string) //string is variable name
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
    | CondExp(exp, exp, exp) //the three expressions are the condition, 'if' expression and 'else' expression, respectively
```

语法：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" { <block-item> } "}"
<block-item> ::= <statement> | <declaration>
<declaration> ::= "int" <id> [ = <exp> ] ";"
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]

<exp> ::= <id> "=" <exp> | <conditional-exp>
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
<logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
<equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
<relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
<additive-exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int> | <id>
<unary_op> ::= "!" | "~" | "-"
```

## 代码生成

为了生成 "if "语句和条件表达式的汇编代码，我们将需要有条件和无条件的跳转，我们在lab4中介绍过这些指令。我们可以比较容易地为条件表达式 "e1 ? e2 : e3 "生成汇编代码，如下所示：

```
    <CODE FOR e1 GOES HERE>
    cmpl $0, %eax
    je   _e3                  ; if e1 == 0, e1 is false so execute e3
    <CODE FOR e2 GOES HERE>  ; we're still here so e1 must be true. execute e2.
    jmp  _post_conditional    ; jump over e3
_e3:
    <CODE FOR e3 GOES HERE>  ; we jumped here because e1 was false. execute e3.
_post_conditional:            ; we need this label to jump over e3
```

生成`if`语句的汇编很相似，尽管它因可选的`else`子句而略显复杂。

就像我们前面看到的`&&`和`||`的汇编一样，标签（label）必须是唯一的。

#### ☑任务

更新代码生成过程，以正确处理三元条件表达式和`if`语句。它应该在所有step[1-6]的例子上成功。

## 下一步

在接下来的实验中，我们将添加复合语句。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)