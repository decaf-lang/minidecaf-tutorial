# lab9：函数

在次试验中，我们将添加函数调用。我们将讨论调用惯例和栈帧以及C11标准的一些奇怪的角落。当然，我们的编译器已经可以处理函数定义，因为我们已经可以定义`main`。但在这篇文章中，我们将增加对函数调用的支持：

```
int three() {
    return 3;
}

int main() {
    return three();
}
```

我们还将增加对函数参数的支持：

```
int sum(int a, int b) {
    return a + b;
}

int main() {
    return sum(1, 1);
}
```

和对前向函数声明的支持：

```
int sum(int a, int b);

int main() {
    return sum(1, 1);
}

int sum(int a, int b) {
    return a + b;
}
```

###术语

- 一个函数**声明（declaration ）**指定了一个函数的名称（name）、返回类型（return type）以及可选的参数列表（parameter list）：
```
    int foo();
```

- 函数**原型（prototype ）**是一种特殊类型的函数声明，包括参数类型信息：

```
    int foo(int a);
```

**函数原型**是我们唯一会支持的**函数声明**。

- 一个函数**定义（definition ）**就是一个声明加上一个函数体（ function body）：

```
    int foo(int a) {
        return a + 1;
    }
```

> 注意：
>  - 你可以任意多次声明一个函数，但只能定义一次。
>  - 每当我们说 "所有函数声明 "时，都包括作为函数定义一部分的函数声明。

- 一个**前向声明**是一个没有函数体的函数声明。它告诉编译器你将在以后定义函数，可能是在不同的文件中，并让你在定义函数之前使用它：

```
    int foo(int a);
```

  你也可以声明一个已经定义好的函数。这是合法的，但没有特别的意义。

```
    int foo() {
        return 4;
    }
  
    int foo();
```

- 一个函数的**实际参数（arguments）**是传递给函数调用的值。一个函数的**形式参数（parameters ）**是在函数声明中定义的变量。在这段代码中，`a`是一个形式参数，`3`是一个实际参数：

```
    int foo(int a) {
        return a + 1;
    }
  
    int main() {
        return foo(3);
    }
```

### 限制

- 目前，我们只支持返回类型为`int`的函数和参数类型为`int`的函数。

- 我们不会支持缺少参数或类型信息的函数声明；换句话说，我们将要求所有函数声明都是函数原型，无论它们是否是函数定义的一部分。

- 我们将把一个空的参数列表（例如在声明`int foo()`中）解释为函数没有参数。这与C11标准有所偏离；根据C11标准，`int foo(void)`是一个函数原型，表示`foo`没有参数，而`int foo()`是一个没有指定参数的声明（即不是函数原型）。

- 我们不会支持使用标识符列表形式的函数定义，它看起来像这样：

```
    int foo(a)
    int a;
    {
        return a * 2;
    }
```

- 我们会在函数声明中要求参数名。例如，我们不会支持这样做：

```
    int foo(int, int);
```

- 我们不支持存储类指定符-- storage class specifiers (如`extern`、`static`)、类型限定符 -- type qualifiers (如`const`、`atomic`)、函数指定符 -- function specifiers(`inline`、`_Noreturn`)或对齐指定符 -- alignment specifiers(`_Alignas`)

## 词法分析

我们只需要添加逗号来分隔函数参数。这是目前的全部标记列表：

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
- `for`
- `while`
- `do`
- `break`
- `continue`
- **`,`**

#### ☑任务

在词典中增加对逗号的支持。它应该适用于测试套件中的所有step[1-9]的例子。

## 语法解析

我们先处理函数定义，然后处理函数调用。

###函数定义

在我们以前的定义中，一个函数只是有一个名称和一个主体。

```
function_declaration = Function(string, block_item list) //string is the function name
```

现在我们需要添加一个参数列表。我们还需要支持不包含函数体的声明。这里定义了一个单一的 "function_declaration "AST规则，其中包含一个可选的函数体，以表示声明和定义：

```
function_declaration = Function(string, // function name
                                string list, // parameters
                                block_item list option) // body
```

但如果你愿意，你也可以对函数的声明和定义有不同的规则。

请注意，我们没有包含函数的返回类型或参数类型，因为现在`int`是唯一的类型。当我们添加其他类型时，我们需要扩展这个定义。

我们还需要更新语法。这里是旧的`<function>`语法规则：

```
<function> ::= "int" <id> "(" ")" "{" { <block-item> } "}"
```

这是新的。注意，函数声明的结尾要么是函数体（如果是定义），要么是分号（如果不是）。

```
<function> ::= "int" <id> "(" [ "int" <id> { "," "int" <id> } ] ")" ( "{" { <block-item> } "}" | ";" )
```

###函数调用

函数调用是一个类似这样的表达式：

```
foo(arg1, arg2)
```

它有一个ID（函数名）和一个参数列表。它的参数可以是任意的表达式：

```
foo(arg1 + 2, bar())
```

所以我们可以更新AST定义这样的表达式：

```
exp = ...
    | FunCall(string, exp list) // string is the function name
    ...
```

我们还需要更新语法。函数调用具有尽可能高的优先级，与一元运算符一样。所以我们将把它们添加到语法中的`<factor>`规则中：

```
<factor> ::= <function-call> | "(" <exp> ")" | <unary_op> <factor> | <int> | <id>
<function-call> ::= id "(" [ <exp> { "," <exp> } ] ")"
```

### 顶层（Top Level）

在我们以前的定义中，一个程序由一个函数定义组成。现在它需要允许多个函数声明。

```
program = Program(function_declaration list)
<program> ::= { <function> }
```

#### ☑任务

更新语法解析过程，使所有step[1-9]的例子都能成功。

## 验证

我们需要验证程序中的函数声明和调用是否合法。这可以在代码生成过程中处理这些检查，或者在语法解析和代码生成之间增加一个新的验证阶段。

如果出现以下情况，你的编译器一定会失败：

- 程序中包含两个相同函数名的定义：

```
    int foo(){
        return 3;
    }
  
    int foo(int a){
        return a + 1;
    }
```

- 一个函数的两个声明的参数数量不同（不过参数名称不同也是允许的）  是不合法的：

```
    int foo(int a, int b);
  
    int foo(int a){
        return a + 1;
    }
```

 但这样是合法的：

```
    int foo(int a);
  
    int foo(int b){
        return b + 1;
    }
```

- 调用函数时，参数数量错误，如：

```
    int foo(int a){
        return a + 1;
    }
  
    int main() {
        return foo(3, 4);
    }
```

- 如果一个函数在被声明之前就被调用，你可以选择编译失败。请注意，调用一个已声明但未定义的函数是完全合法的。同样合法的还有声明一个函数而不定义它；但是，如果函数没有在链接器能找到的其他库中声明，链接就会失败。

  所以这是违法的：

```
    int main() {
        return putchar(65);
    }
  
    int foo(){
        return 3;
    }
```

  但这是合法的：

```
    int putchar(int c);
  
    int main() {
        putchar(65);
    }
```

  最后一点是可有可无的，因为GCC和clang都没有执行这一点--它们都会对上面的非法例子发出警告，但不会失败。在函数被声明之前调用函数被称为 "隐式函数声明"，在C99之前它是合法的，所以执行这个规则会破坏很多旧代码。测试集中不包含任何隐式函数声明，所以你可以随心所欲地处理它，仍然可以通过所有的测试。

#### ☑（可选）任务

更新你的编译器，你可以在代码生成过程中处理这个问题，或者在解析和代码生成之间新建一个阶段。有用的错误信息可以帮助开发人员理解源码中的错误。

为了处理这个问题，可能会想要遍历树，并维护一个映射来跟踪每个函数的参数个数，以及该函数是否已经被定义。

## 代码生成

再一次，我们将首先处理函数定义，然后是函数调用。但在我们做这些之前，我们先来讨论一下函数调用约定。

### （可选）函数调用惯例（Calling Conventions）

在上面的大多数例子中，我们定义了一个函数，然后在同一个文件中调用它。但是我们也想调用共享库中的函数；我们特别想调用标准库，这样我们就可以访问I/O函数，这样我们就可以写 "Hello，World"。当你使用一个共享库时，一般不会自己重新编译，而是链接到一个预编译的二进制库文件。我们肯定不希望重新编译整个标准库。这意味着我们需要生成能够与其他编译器构建的目标文件（object files）交互的机器代码。

换句话说，我们需要遵循相应的*调用惯例*。调用惯例可以回答如下的问题：	

- 参数是如何传递给被调用者（caller ）的？它们是在寄存器中还是在栈中传递？
- 在被调用者执行完后，调用者或被调用者（callee ）是否负责从栈中删除参数？
- 返回值是如何传回给调用者的？
- 哪些寄存器是调用者保存的，哪些是被调用者保存的？

32位OS X、Linux和其他类似Unix的系统上的C程序使用`cdecl`调用约定，这意味着。

- 参数是在栈上传递的。它们在栈上从右到左被推送（所以第一个函数参数在最低地址）。
- 调用者从栈中清理参数。
- 返回值在`EAX`寄存器中传递。(完整的答案比较复杂，但只要我们只能返回整数就够了)。
- `EAX`、`ECX`和`EDX`寄存器是调用者保存的，其他都是调用者保存的。我们在下一节中会看到，被调用者在返回前要恢复`EBP`和`ESP`，并用`ret`指令恢复`EIP`。正常情况下，它还需要还原`ESI`、`EDI`和`EBX`，但实际上我们并不使用这些寄存器。而且我们已经把`EAX`、`ECX`和`EDX`的值推到栈上了，如果我们以后需要它们的话。所以基本上，我们根本不用担心保存和恢复寄存器的问题。

OS X和Linux之间有两个导入差异。

- 栈对齐（stack alignment）：在OS X上，在函数调用开始时（即发出`call`指令时），栈需要进行16字节对齐。这在Linux上不是必须的，但GCC仍然保持栈16字节对齐。
- 名称装饰（name decoration）：在OS X上，汇编中的函数名会在前面加上下划线(例如，`main`变成`_main`)。在使用ELF文件格式的系统上（Linux和大多数其他unix系统），没有下划线。这不是调用惯例本身的一部分，但它很重要。

我们需要对所有这些都很熟悉才能自己实现。

### cdecl函数调用的细节

```
foo(1, 2, 3);
```

当你的计算机执行这行代码时，到底会发生什么？我们在lab5中提到了这个问题，但现在我们将深入研究它。我们暂时不担心保持栈16字节对齐的问题。

我们假设`foo`被另一个函数`bar`调用。上面的那行C语言将变成这个汇编

```
push $3
push $2
push $1
call _foo
add $0xc, %esp
```

首先，在开始调用 "foo "函数之前，我们先看看这个程序的执行状况：

![EBP points at the base of bar's stack frame at 0x14. ESP is 4 bytes below it at 0x10. EIP points at "pushl $3".](./lab9-pics/before_function_call.svg)

内存中有一块区域包含了栈帧，我们已经很熟悉了。`EBP`和`ESP`寄存器分别指向栈帧的底部和顶部，所以处理器可以找出栈的位置。

另一块内存，我们还没有谈及，包含正在执行的CPU指令。`EIP`寄存器包含当前指令的内存地址。要前进到下一条指令，CPU只需将`EIP`递增。`call`指令，以及我们已经遇到的所有跳转指令，都是通过操纵EIP来工作的。在这些图中，我将显示`EIP`指向我们将要执行的指令。

当`bar`函数要调用`foo`函数时，第一步就是把函数参数放到栈上，让`foo`能找到它们。它们以相反的顺序被推到栈上：

```
push $3
push $2
push $1
```

也就是说现在的程序执行状态是这样的

[值3, 2, 和1已经被推送到堆栈中, 依次为. ESP指向内存地址0x20，里面有值1。EIP指向 "调用_foo"。EBP没有变化。](./lab9-pics/before_function_call_args_pushed.svg)

接下来`bar`发出`call`指令，做两件事：

1. 将`call`之后的指令*地址（"返回地址"）推到栈上。
2. 跳转到`_foo`（把`_foo`的地址移到`EIP`中）。

现在程序的执行状态看起来是这样的：

[after_call](./lab9-pics/after_call.svg)

好了，我们现在正式进入`foo`了。下一步是通过函数前序来建立一个新的栈帧：

```
push %ebp
mov %esp, %ebp
```

![ESP and EBP both point at 0x28, which holds the previous value of EBP (0x10).](./lab9-pics/after_function_prologue.svg)

现在我们可以执行`foo`的函数主体。我们可以访问它的参数，因为它们在堆栈上相对于`EBP`的一个可访问的位置：`%ebp + 0x8`，`%ebp + 0xc`，和`%ebp + 0x10`。

一旦我们在`foo`中做了一些事情，并在`EAX`中放置了一个返回值，就可以返回到`bar`了。除了那个返回值，我们希望堆栈上的一切都和调用前完全一样。第一步是运行函数收尾（function epilogue）来恢复旧的栈帧：

```
mov %ebp, %esp ; deallocate any local variables on the stack
pop %ebp        ; restore old EBP
```

现在的堆栈看起来和在`call`指令后，函数前序前这个时刻的堆栈一模一样。这意味着返回地址又在栈顶了。

然后我们执行`ret`指令，将栈顶的值从栈顶弹出，并无条件跳转到栈顶（即复制到`EIP`）。

![ESP points at 0x20, which holds function argument 1. EIP points to the address of the instruction right after "_call foo".](./lab9-pics/after_ret.svg)

现在我们只需要从堆栈中删除函数参数，就可以了。不需要一个一个的删除，我们只需要调整`ESP`的值就可以了。

```
add $0xc, %esp
```

现在堆栈已经完全恢复到调用前的状态，我们可以继续执行`bar`的其他部分。

现在我们终于可以实现编译器的代码生成阶段了。

### 函数定义

和 "main "一样，我们要让每个函数都成为全局函数（这样就可以从其他文件中调用它）并给它打上标签。

```
    .globl _fun
_fun:
```

如果你是在OS X上，请确保在函数名前加上前导下划线，否则不需要。

我们已经知道如何生成函数前序（prologue）和收尾（epilogue），因为这也和`main`完全一样。我们只需要将所有的函数参数添加到`var_map`和`current_scope`中。正如我们上面所看到的，第一个参数将在`ebp + 8`处，随后的每个参数将比上一个参数高四个字节。

```
param_offset = 8 // first parameter is at EBP + 8
for each function parameter:
    var_map.put(parameter, param offset)
    current_scope.add(parameter)
    param_offset += 4
```

然后，参数会像函数体中的其他变量一样被处理：

### 函数原型

我们不会为不属于定义的函数原型（function prototypes）生成任何汇编。

### 函数调用

正如我们上面所看到的，函数调用方需要执行如下操作：

1. 按照相反的顺序，把参数放在堆栈上：

```
    for each argument in reversed(function_call.arguments):
        generate_exp(arg) // puts arg in eax
        emit 'pushl %eax'
```

2. 发出 `call`指令：

```
        emit 'call _{}'.format(function_name)
```

3. 在被调用者返回后，从堆栈中删除参数：

```
        bytes_to_remove = 4 * number of function arguments
        emit 'addl ${}, %esp'.format(bytes_to_remove)
```

####堆栈对齐

在 OS X 上，当调用指令发出时，栈需要 16 字节对齐。一个正常的 C 编译器会准确地知道要添加多少padding来保持这种对齐。但由于我们将表达式的中间结果推送到堆栈上，而函数调用可能发生在较大的表达式中，所以当我们遇到函数调用时，我们不知道堆栈指针在哪里。目前的解决方案是在每次函数调用前生成汇编码，用于计算出需要多少padding，相应地从ESP中减去，然后将padding计算的结果推送到堆栈上，这一切都在将函数参数放到堆栈上之前完成。函数返回后，调用者首先删除参数，然后弹出（pop off）填充计算的结果，最后将该值加到ESP中，使其恢复到原来的执行状态。

下面是完成上述工作的汇编代码：

```
    movl %esp, %eax
    subl $n, %eax    ; n = (4*(arg_count + 1)), # of bytes allocated for arguments + padding value itself
                     ; eax now contains the value ESP will have when call instruction is executed
    xorl %edx, %edx  ; zero out EDX, which will contain remainder of division
    movl $0x20, %ecx ; 0x20 = 16
    idivl %ecx       ; calculate eax / 16. EDX contains remainder, i.e. # of bytes to subtract from ESP 
    subl %edx, %esp  ; pad ESP
    pushl %edx       ; push padding result onto stack; we'll need it to deallocate padding later
    ; ...push arguments, call function, remove arguments...
    popl %edx        ; pop padding result
    addl %edx, %esp  ; remove padding
```

这个方案有点难看，如果你想出更好的方案，请告诉我。

### 顶层（Top Level）

显然，你需要为每个函数定义生成汇编，而不仅仅是一个老的`main`函数。

#### ☑任务

更新你的编译器，以处理所有step[1-9]的例子。确保它产生正确的返回代码。

## Fibonacci

现在我们可以计算Fibonacci数字。

```
int fib(int n) {
    if (n == 0 || n == 1) {
        return n;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

int main() {
    int n = 10;
    return fib(n);
}
```

## 下一步

接下来的实验室实现对全局变量（global variables）的支持。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)