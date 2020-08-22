
# Lab5：局部变量

本次试验，我们将添加对局部变量的支持，这样就可以编译多于一行的函数了。没有变量的编程是很难的。为了保持简单，我们现在将以一种非常有限的方式支持变量。
- 只支持局部变量, 在 "main "中声明；
- 不支持全局变量
- 我们只支持类型为`int`的变量
- 我们不支持 "short"、"long "或 "unsigned "等类型修饰符，不支持 "static "等存储类指定符，也不支持 "const "等类型限定符。只是普通的 "int"
- 每个语句只能声明一个变量。我们不支持像`int a, b;`这样的语句

你可以对一个变量做三件事：

- 声明（Declare ）：`int a;`
  - 当你声明它时，你也可以选择初始化它(`int a = 2;`)
- 赋值（Assign ）：(`a = 3;`)

- 引用（Reference ）：在一个表达式中引用它(`a + 2`)

我们需要增加对这三样事的支持。我们还将添加对包含多个语句的函数的支持。

## 词法分析

本周唯一的新标记是赋值操作符`=`。以下是我们的标记列表，最新增加的标记在底部用粗体表示。

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
- **Assignment `=`**

#### ☑任务

更新*lex*函数以处理`=`标记。它应该适用于测试集中所有step[1-5]的例子。

### 语法解析

本次实验中，我们需要对AST做很多修改。让我们来看一个要处理的示例程序：

```
int main() {
    int a = 1;
    a = a + 1;
    return a;
}
```

在这个程序中，`main`包含三个语句：

1. 变量声明（`int a = 1;`）
2. 变量赋值(`a = a + 1;`)
3. 函数返回（`return a;`）

我们需要更新AST中`function_declaration`的定义，这样一个函数就可以包含一系列语句，而不仅仅是一条语句：

```
function_declaration = Function(string, statement list) //string is function name
```

现在，我们定义的语句只有 "返回 "语句。这也不对。我们需要再增加一些：

```
statement = Return(exp) 
          | Declare(string, exp option) //string is variable name
                                        //exp is optional initializer
          | Exp(exp)
```

我们为变量声明添加了`Decl`。我们可以使用一个选项类型(如Rust中的`Option`，Haskell中的`Maybe`)来表示我们可能有也可能没有初始化操作：

`int a;`的AST可能是这样的：

```
decl = Declare("a", None) //None because we don't initialize it
```

而`int a = 3`的AST可能是这样的：

```
init_exp = Const(3)
decl = Declare("a", Some(init_exp))
```

请注意，我们并没有在AST中的任何地方存储变量的类型；我们不需要，因为它只能有类型`int`。一旦我们有了多个类型，我们就需要开始跟踪类型信息。

我们还添加了一个独立的`Exp`语句，这意味着我们现在可以编写这样的程序：

```
int main() {
    2 + 2;
    return 0;
}
```

这是有效的C语言的语句；如果你用GCC编译它，它会发出一个警告，但不会失败。

然而，`2+2;`并不是一个非常有用的语句。添加`Exp`语句的真正原因是为了让我们可以写出这样的语句：

```
a = 2;
```

变量赋值只是一个表达式!，所以下面这条语句是有效的：

```
a = 2 * (b = 2);
```

在上面的代码片段中，表达式`b=2`的值是`2`，更新`b`的副作用是有`2`这个值。这将被评价为：

```
a = 2 * (b = 2)
a = 2 * 2 //also b is 2 now
a = 4
```

现在我们需要更新AST定义中的`exp`，以处理赋值运算符。第一个想法是把`=`作为另一个二进制运算符添加进去--毕竟`a = b`看起来有点像`a + b`。但这完全错了：二进制运算符的两个操作数可以是任意表达式，但赋值运算符的左边不能。像`2 = 2`这样的语句没有任何意义，因为你不能给`2`赋一个新值。相反，我们只需将赋值定义为一种新的表达式类型。

```
exp = Assign(string, exp) //string is variable, exp is value to assign
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

现在我们可以像这样为语句`a = 2;`写AST：

```
assign_exp = Assign("a", Const(2))
assign_statement = Exp(assign_exp)
```

现在我们可以定义变量并更新它们的值，但这并不是超级有用的，除非我们真的可以引用它们。让我们把变量引用作为另一种类型的表达式来添加：

```
exp = Assign(string, exp)
    | Var(string) //string is variable name
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

现在我们可以像这样写AST`return a;`：

```
return_exp = Var("a")
return_statement = Return(return_exp)
```

如果我们把它放在一起，这里是本次实验的新AST：

```
program = Program(function_declaration)
function_declaration = Function(string, statement list) //string is the function name

statement = Return(exp) 
          | Declare(string, exp option) //string is variable name
                                        //exp is optional initializer
          | Exp(exp) 

exp = Assign(string, exp)
    | Var(string) //string is variable name 
    | BinOp(binary_operator, exp, exp)
    | UnOp(unary_operator, exp)
    | Constant(int)
```

我们还需要更新我们的语法。首先，我们需要更新`<function>`以允许多个语句。

旧定义：

```
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
```

新定义：

```
<function> ::= "int" <id> "(" ")" "{" { <statement> } "}"
```

由于中间穿插了表示重复的`{`/`}`和表示大括号的`"{"`/`"}"`，这几乎是完全不可读的。但这只是意味着一个函数可以有多个语句了。

我们需要处理多种类型的语句。我们已经有了返回语句：

```
"return" <exp> ";"
```

而且独立的表达也很简单：

```
<exp> ";"
```

变量声明需要一个类型说明符(`int`)和一个名称，后面还需要一个初始化器（initializer）。我们在这里使用`[]`表示某些东西是可选的。

```
"int" <id> [ = <exp> ] ";"
```

让我们把它放在一起，得到我们对`<statement>`的新定义：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "int" <id> [ = <exp> ] ";"
```

最后，我们需要更新`<exp>`。赋值（Assignment ）是最低优先级的运算符，所以它成为最高层（top level）的`<exp>`表达式。还要注意的是，与其他大多数运算符不同，它是右结合的，这使得它的表达更简单一些。

```
<exp> ::= <id> "=" <exp> | <logical-or-exp>
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> }
```

我们所有二进制操作的语法(从`<logical-and-exp>`到`<term>`)都没有变化。我们只需要修改`<factor>`，这样我们就可以引用变量和常量：

```
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int> | <id>
```

当你把它放在一起的时候，这是我们的新语法：

```
<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" { <statement> } "}"
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "int" <id> [ = <exp>] ";" 
<exp> ::= <id> "=" <exp> | <logical-or-exp>
<logical-or-exp> ::= <logical-and-exp> { "||" <logical-and-exp> } 
<logical-and-exp> ::= <equality-exp> { "&&" <equality-exp> }
<equality-exp> ::= <relational-exp> { ("!=" | "==") <relational-exp> }
<relational-exp> ::= <additive-exp> { ("<" | ">" | "<=" | ">=") <additive-exp> }
<additive-exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <exp> ")" | <unary_op> <factor> | <int> | <id>
<unary_op> ::= "!" | "~" | "-"
```

#### ☑ 任务

更新你的表达式解析代码以处理变量的声明（declaration）、赋值（assignment）和引用（references）。完成任务后，应该能成功解析测试集中所有step[1-5]中的例子。

## 代码生成

我们需要把局部变量保存在某个地方。简单起见，我们会把它们保存在栈上。我们还需要记住每个变量在栈上保存的确切位置，以便我们以后可以引用它。为了跟踪这些信息，我们将创建一个从变量名到位置的映射（也称map，散列，字典等）。

但是我们如何在编译时知道一个变量的位置呢？绝对的内存地址要到运行时才能确定。我们可以从ESP中存储变量的偏移量，但ESP的值会在我们把东西推到（push）栈上时改变。解决方法是将变量的偏移量存储在另一个寄存器EBP中。为了理解为什么这样做，我们需要了解一些关于栈帧的知识。

### 栈帧(Stack Frames)

每当我们调用一个函数时，我们都会在栈顶部为其分配一块内存--这块内存被称为*栈帧*。栈帧中存放着函数参数，函数返回后要跳转的地址，当然还有局部变量。我们已经知道ESP指向栈顶，也就是当前栈帧的顶部。EBP（或称基指针）寄存器指向当前栈帧的底部。如果没有EBP，我们就不知道一次栈帧在哪里结束，另一次栈帧在哪里开始，我们也无法找到函数的返回地址等重要值。

![义务调用栈图](./lab5-pics/call_stack.svg)

调用栈图，从栈底的较高地址到栈顶的较低地址。一、被调用者的栈帧 *被调用者的局部变量y *被调用者的局部变量x *返回地址 二、被调用者的栈帧 *保存的EBP（当前EBP点在此） *局部变量a *局部变量b（栈顶） 三、被调用者的栈帧 *保存的EBP（当前EBP点在此） *局部变量a *局部变量b（栈顶 调用者的栈帧 * 保存的EBP（当前EBP点在此） * 本地变量a * 本地变量b（栈顶；当前ESP点在此） 三．

当一个函数(我们称它为`f`)返回时，它的调用者需要能够接上它离开的地方。这意味着它的栈帧，以及ESP和EBP中的值，都需要和`f`被调用之前完全一样。`f`需要做的第一件事就是为自己建立一个新的栈帧，使用下面的指令。

```
    push %ebp       ; save old value of EBP
    movl %esp, %ebp ; current top of stack is bottom of new stack frame
```

这些指令称为函数前序（function prologue）。在`f`返回之前，它立即执行函数前序来删除这个栈帧，让一切都和函数前序之前一样。

```
    movl %ebp, %esp ; restore ESP; now it points to old EBP
    pop %ebp        ; restore old EBP; now ESP is where it was before prologue
    ret
```

到目前为止，我们可以不需要函数前序（function prologue）或函数收尾（function epilogue），但现在我们需要添加它们。添加它们有两方面的帮助：

- **可以将变量位置保存为EBP的偏移量**。我们知道EBP上面没有任何东西（因为我们在函数前序中设置了一个空的堆栈框架），而且我们知道EBP在函数收尾之前不会改变。
- 我们可以安全地将局部变量推送到栈上，而不改变调用者的栈帧。

我们应该在函数定义的开始处生成函数前序，就在函数的标签之后，并在返回语句中生成函数收尾，即在`ret`指令之前。

除了我们的变量映射，我们还需要跟踪一个*栈索引（stack index）*，它告诉我们栈上的下一个可用位置的偏移（相对于`EBP`）。下一个可用的位置总是ESP之后的字（`word`），在`ESP - 4`处。在函数前序之后，EBP和ESP是一样的。这意味着堆栈索引也将是-4。每当我们将一个变量推到（push）堆栈上时，我们将把堆栈索引递减`4`。

现在让我们看看如何处理变量的声明、赋值和引用。

### 变量声明

遇到变量声明时，只需将变量保存到栈中，并将其添加到变量映射表（`variable map`）中。请注意，在同一个局部作用域中两次声明一个变量是非法的，就像下面的代码片段一样：

```
int a;
int a;
```

所以如果变量已经在变量映射表中，你的程序应该会失败。下面是如何为语句`int a = expression`生成汇编的伪代码：

```
  if var_map.contains("a"):
    fail() //shouldn't declare a var twice
  generate_exp(expression)      // generate assembly to calculate e1 and move it to eax
  emit "    pushl %eax" // save initial value of "a" onto the stack
  var_map = var_map.put("a", stack_index) // record location of a in the variable map
  stack_index = stack_index - 4 // stack location of next address will be 4 bytes lower
```

这里有几点说明：

- 如果一个变量没有被初始化，你可以直接把它初始化为0。
- 变量映射表存在于代码生成过程中，而不是在运行时。
- 你应该为变量映射表**明确地使用一个不可变的数据结构（immutable data structure）**。在后续试验中，我们将添加`if`语句，然后我们将有嵌套的作用域；在`if`块中声明的变量在其外部是不可访问的。这样就不用担心来自内部作用域的代码会影响到外部作用域的变量映射。

> 提示：immutables data structure是基于此数据结构的变量被初始化后，就不能再被更新了。


### 变量赋值

我们可以在变量映射表中查找一个变量在内存中的位置；如果要给它分配一个新的值，只需将该值移动到正确的内存位置即可。下面是如何处理`a = expression`的过程：

```
  generate_exp(expression) // generate assembly to calculate expression and move it to eax 
  var_offset = var_map.find("a") //if "a" isn't in the map, fail b/c it hasn't been declared yet
  emit "    movl %eax, {}(%ebp)".format(var_offset) //using python-style string formatting here
```

请注意，`expression`的值仍在EAX中，所以这个赋值表达式的值是正确的。

### 变量引用

要引用表达式中的变量，只需将其从堆栈中复制到EAX即可：

```
  var_offset = var_map.find("a") //find location of variable "a" on the stack
                                 //should fail if it hasn't been declared yet
  emit "    movl {}(%ebp), %eax".format(var_offset) //retrieve value of variable
```

### 缺少返回声明

现在我们支持多种类型的语句，我们可以成功解析完全没有返回语句的程序。

```
int main() {
  int a = 2;
}
```

这里的预期行为是什么？根据[C11标准](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)第5.1.2.2.3节。

> 如果`main`函数的返回类型是与`int`兼容的类型，那么从初始调用`main`函数后的返回相当于以`main`函数返回的值作为参数调用`exit`函数；到达结束`main`函数的`}`时，返回的值为0。

所以，`main`如果缺少返回语句，需要返回0。现在`main`是我们唯一的函数，所以这是我们唯一需要处理的情况。

最终，我们需要在`main`以外的函数中处理这个问题。下面是标准的6.9.1节关于缺失返回语句的一般说明。

>如果到达了终止函数的`}`，而函数调用的值被调用者使用，那么行为是未定义的。

所以下面这个程序的行为是未定义的：

```
int foo() {
  1 + 1;
}

int main() {
  return foo();
}
```

从技术上讲，你可以按照自己的想法来处理这个问题--失败，继续默默地进行，发出`halt`指令。

另一方面，这个程序是完全有效的，因为从`foo()`返回的值从来没有被使用过：

```
int foo() {
  1 + 1;
}

int main() {
  foo();
  return 0;
}
```

老实说，这里的规范在我们看来真的不合适。如果我写了一个没有返回语句的非 "void "函数，那是错误的，我希望编译器能拯救我，即使我在技术上还没有以非法的方式使用它。

然而，这就是规范，所以我们的函数必须成功返回，即使它们缺少返回语句。这意味着即使缺少返回语句，你也需要发出函数的尾声和`ret`指令。统一处理`main`函数可能是最简单的，所以你可以直接从任何没有返回语句的函数中返回0。

#### ☑任务

更新你的代码生成阶段：

- 生成函数前序和函数收尾
- 为变量声明、变量赋值和变量引用生成正确的代码
- 使`main`返回0，即使缺少返回语句

新的编译器应该在测试集的step[1-5]中的所有例子中成功。



## 下一步

在下一次试验中，我们将添加 "if "语句和条件运算符("a ? b : c")。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)