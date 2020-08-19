

# lab10：全局变量

本次实验将实现全局变量。这并不太复杂，但它让我们了解一些新的目标文件和程序内存的一些知识。

在前面的实验中，我们已经可以处理在函数内部声明的局部变量了，现在我们将增加对全局变量的支持，任何函数都可以访问这些全局变量。

```
int foo;

int fun1() {
    foo = 3;
    return 0;
}

int fun2() {
    return foo;
}

int main() {
    fun1();
    return fun2();
}
```

请注意，全局变量可以被同名的局部变量所遮挡（shadow）。

```
int foo = 3;

int main() {
    int foo = 4; //shadows global 'foo'
    return foo; // returns 4
}
```

全局变量类似于函数，它们可以被多次声明，但只被定义（即初始化）一次：

```
int foo; // declaration

int main() {
    return foo; // returns 3
}

int foo = 3; // definition
```

而且，和函数一样，全局变量在使用前必须先声明（但不一定要定义）：

```
int main() {
    return foo; // ERROR: not declared!
}

int foo;
```

声明一个函数和一个全局变量的名称相同是一个错误：

```
int foo() {
    return 3;
}

int foo = 4; // ERROR
```

与局部变量不同，全局变量不需要显式初始化。如果一个局部变量没有被初始化，它的值是未定义的，但是如果一个全局变量没有被初始化，它的值是0。

```
int main() {
    int foo;
    return foo; // This could be literally anything
}
int foo;

int main() {
    return foo; // This will definitely be 0
}
```

注意，我们使用 "声明（declaration） "和 "定义 （definition）"这两个术语的方式与我们对函数使用的方式相同。这是一个全局变量声明[。

```
int foo;
```

这既是一个声明，也是一个定义：

```
int foo = 1;
```

`static`和`extern`关键字会增加一些额外的复杂性，但目前的实验还不支持这些。


## 词法分析

本次试验没有新的标记，所以我们不用去碰词法分析部分。

## 语法解析

以前，一个程序是一个函数声明的列表。现在它是一个顶层（top-level）声明的列表，每一个顶层声明要么是一个函数声明，要么是一个变量声明。

所以我们的顶层AST定义现在是这样的：

```
toplevel_item = Function(function_declaration)
              | Variable(declaration)
toplevel = Program(toplevel_item list)              
```

而我们需要对顶层语法规则进行相应的修改：

```
<program> ::= { <function> | <declaration> }
```

#### ☑任务

更新解析通道以支持全局变量。现在解析阶段应该在1-10阶段的所有有效例子上成功。

## 代码生成

全局变量需要住在内存中的某个地方。它们不能住在堆栈上，因为它们需要从每个堆栈框架中访问。取而代之的是，它们生活在另一块内存中，即数据区域（data section）。我们已经看到了一个正在运行的程序的堆栈是什么样的，现在让我们退一步，看看它的所有内存是如何布局的。

![程序内存布局图](./lab10-pics/program_memory_layout.png)

到目前为止，我们一直在处理的x86指令都在代码区域（text section），而我们的全局变量则在数据区域（data section），我们可以将其进一步细分为初始化和未初始化的数据--未初始化的数据区域通常称为BSS。我们的全局变量将在数据区域，我们可以进一步将其细分为初始化数据和未初始化数据--未初始化数据部分通常称为BSS。

到目前为止，我们只为代码区域生成了汇编，其中包含了实际的程序指令；让我们看看在数据区域描述一个变量的汇编是什么样的：

```
    .globl _my_var ; make this symbol visible to the linker
    .data          ; what's next describes the data section    
    .align 2       ; this data should aligned on 4-byte intervals (i.e. it should be word-aligned)
_my_var:
    .long 1337     ; allocate a long integer with value 1337
```

这里有几件事要注意：

- `.data`指令告诉汇编器我们在数据区域。我们还需要一个`.text`指令来指示我们何时切换回代码区域。
- 像 `_my_var`这样的标签可以标注一个内存地址。汇编器和链接器并不关心这个地址是指代码区域的指令还是数据区域的变量，它们会以同样的方式处理它。
- 在macOS上，`.align n`的意思是 "将下一个东西对齐到2n个字节的倍数"。所以`.align 2`意味着我们使用4字节的对齐方式。在Linux上，`.align n`的意思是 "将下一个东西对齐到n个字节的倍数"，所以你需要`.align 4`来得到同样的结果。

一旦你分配了一个变量，你就可以在汇编中直接引用它的标签：

```
    movl %eax, _my_var ; move the value in %eax to the memory address of _my_var
```

所以这里重要的基本要点是：

1. 当你遇到一个全局变量的声明时，将其添加到变量映射表（variable map）中。变量映射表的条目（entry）将是它的标签，而不是栈索引。

```
    var_map = var_map.put("my_var", "_my_var")
```

   请注意，这个新的变量映射表条目必须在我们以后生成的顶层项（top-level items）时可见，我们在处理函数定义时添加的条目就不是这样处理了。

2. 遇到有初始化器（initializer）的全局变量的定义时，要生成汇编代码，处理在数据区域的分配。然后再生成`.text`指令（directive ），再去生成函数定义。

3. 当你遇到一个变量的引用时，用之前的方法处理它。如果它在变量映射表中的条目是一个标签而不是栈索引，则应该直接使用它而不是作为`%ebp`的偏移。如果它没有条目，那就是一个错误。


### 未初始化变量

如果在程序结束时，我们还剩下一些已经声明但没有定义的变量，我们需要将它们声明在一个特殊的区域，用于保存未初始化的数据。在Linux上，所有未初始化的数据都在BSS区域，其中也包括任何初始化为0的变量。在macOS上，这就有点复杂了：未初始化的静态变量放在BSS中，而未初始化的全局变量放在共用区域（common section），这就向链接器表明它们可能在不同的目标文件（object file）中被初始化。我们还不支持静态变量，所以在macOS上我们不需要在BSS中存储任何东西。当然，我们也没有任何使用多个源文件的测试，所以如果你只是使用BSS区域而不是common区域，使所有的全局变量成为静态变量，测试仍然会通过。

数据区域由我们数据的实际值组成，我们可以直接加载到内存中，按原样使用。另一方面，BSS和common区域并不包含我们所有未初始化的值，因为它们只是一大块零。在磁盘上存储一大块零会很浪费空间。相反，我们只需在二进制中存储BSS和common的大小值，并在加载程序时为它们分配这么多的内存。所以将初始化变量和未初始化变量分开，只是一个减少二进制文件大小的技巧。

在macOS上，我们可以使用`.comm`指令在common部分分配空间。

```
    .text
    .comm _my_var,4,2 ; allocate 4 bytes for symbol _my_var, with 4-byte alignment
```

另一方面，在BSS中分配空间，看起来与分配一个非零变量几乎完全一样，但我们将使用`.zero 4`来分配4个零的字节，而不是使用`.long n`来分配一个值`n`的长整数。

```
    .globl _my_var ; make this symbol visible to the linker
    .bss           ; what's next describes the BSS section    
    .align 4       ; this data should aligned on 4-byte intervals (Linux align directive)
_my_var:
    .zero 4        ; allocate 4 bytes of zeros
```

请注意，在汇编中，与C语言不同的是，在定义标签之前，完全可以引用像`_my_var`这样的标签。这就是为什么我们可以等到程序结束时再分配任何未初始化的变量。

### 非常量初始化器（Non-Constant Initializers）

全局变量在程序启动前就被加载到内存中，这意味着我们不能执行任何指令来计算它们的初始值。因此它们的初始化器需要是常量。例如，下面的代码片段是不成立的：

```
int foo = 5;
int bar = foo + 1; // NOT A CONSTANT!
int main() {
    return bar;
}
```

大多数编译器允许用常量表达式来初始化全局变量，比如：

```
int foo = 2 + 3 * 5;
```

这需要你在编译时计算`2 + 3 * 5`。如果你愿意，你可以支持这一点，但你不必这样做；测试集不会检查它。

### （可选）验证

总结一下，以下是我们需要验证的内容。

- 变量，包括全局变量，都是在定义之前声明的。
- 没有一个全局变量被定义超过一次。
- 没有一个全局变量是用非常量值初始化的。
- 没有一个符号既被声明为函数又被声明为变量。

在代码生成过程中验证第一点很容易，反正我们对局部变量也是这样做的。其余的要点可以在代码生成过程中验证，或者在一个单独的验证阶段中验证。建议在任何验证函数定义和调用的地方处理它们。

#### ☑ 任务

更新代码生成极端，对于所有step[1-10]的例子能成功编译并产生沼气结果。

## （可选）PIE 

如果你使用真正的编译器编译一个带有全局变量的程序，那么程序集看起来会和我们上面描述的完全不同。你也可能会注意到，如果你在macOS上，链接器会对你的编译器产生的汇编进行警告。

```
$ ./my_compiler global.c
ld: warning: The i386 architecture is deprecated for macOS (remove from the Xcode build setting: ARCHS)
ld: warning: PIE disabled. Absolute addressing (perhaps -mdynamic-no-pic) not allowed in code signed PIE, but used in _main from /var/folders/9t/p20tf0zs4ql425tdktwnfjkm0000gn/T//cczcZcyQ.o. To fix this warning, don't compile with -mdynamic-no-pic or link with -Wl,-no_pie
```

PIE是 "Position-Independent Executable "的缩写，意思是指完全由位置无关的代码组成的可执行文件。本节简要解释什么是位置无关代码，以及为什么可能需要它，但没有解释如何实现它。如果你不感兴趣，可以随意跳过它。

与位置无关的代码是无论在内存中的哪个位置加载都能运行的代码，因为它从不引用绝对内存地址。我们的编译器产生的代码不是位置无关的，因为它有如下指令：

```
    movl $3, _my_var
```

为了使这条指令能够运行，链接器需要用一个绝对的内存地址来代替`_my_var`。如果我们事先知道数据部分和BSS部分的绝对地址，这样做是可行的。

而与位置无关的代码，从来不会直接引用`_my_var`这样的符号地址，相反，这些地址是相对于当前指令指针计算的。位置无关的汇编代码生成在64位指令集的情况下要简单得多：

```
movl $3, _my_var(%rip) ; use _my_var as offset from instruction pointer
```

要想在32位架构下得到同样的结果，你需要这样的东西：

```
    call    ___x86.get_pc_thunk.ax
L1$pb:
    leal    _my_var-L1$pb(%eax), %eax
    movl    (%eax), %eax
```

这里不会详细介绍这段代码到底在做什么；如果你好奇，[这篇文章](https://eli.thegreenplace.net/2011/11/03/position-independent-code-pic-in-shared-libraries/)给出了一个关于x86的位置无关代码的很好的介绍。

你可能想生成位置无关的代码有两个原因：

1. 你正在编译一个共享库。也许这是一个广泛使用的库，比如libc。也许一个系统上的所有或大多数进程都想要这个库的副本。为每个进程都分配一个单独的库副本，占用你所有的RAM，似乎是一种浪费。相反，我们可以只将库加载到物理内存中一次，然后将其映射到每个需要它的进程的虚拟内存中。但是我们不能保证一个库在每个加载它的进程中都有相同的起始地址。所以，在几个进程之间共享一个库，只有在库无论在什么内存地址都能工作的情况下才行--也就是说，它需要与位置无关。不过，我们是在编译一个可执行文件，而不是一个库，所以这一点对我们并不适用。
2. 你启用了地址空间布局随机化（ASLR）。ASLR是一种安全特性，它使一些内存损坏攻击更难实施。这些攻击中有许多涉及强迫程序执行跳转到攻击者想要执行的指令。启用ASLR后，内存段被加载在随机位置，这使得攻击者更难弄清要跳转到哪个地址。当加载到随机内存地址时，代码需要独立于位置才能正确运行。由于苹果真的希望所有的macOS应用都支持ASLR，所以链接器会在默认情况下尝试构建一个位置独立的可执行文件，如果不能，就会抱怨。

事实上，目前实验实现的编译器不能生成与位置无关的可执行文件。

## 下一步

接下来的实验是完成对指针的支持。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)