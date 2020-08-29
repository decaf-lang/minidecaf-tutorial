# lab7：复合语句



在本次实验中，我们将增加对复合语句（Compound Statements）的支持，复合语句有点奇怪，因为它们并没有多的功能，且几乎不会生成新的汇编，但我们将能够在最后编译出新的功能丰富的程序。

复合语句只是一个用大括号包裹的语句和声明的列表。它们通常被用作`if`、`while`和其他控制结构的子语句，如下面的代码片段：

```
if (flag) {
    //this is a compound statement!
    int a = 1;
}
```

但它们也可以是独立的，像这样：

```
int main() {
    int a;
    {
        //this is also a compound statement!
        a = 4;
    }
}
```

你可以有深度嵌套的复合语句：

```
int main() {
    //compound statement #1 (function bodies are compound statements!)
    int a = 1;
    {
        //compound statement #2
        a = 2;
        {
            //compound statement #3
            a = 3;
            if (a) {
                //compound statement #4
                a = 4;
            }
        }
    }
}
```

复合语句其实就是**block**的一种类型。C语言使用**词法作用域（lexical scoping）**，一个变量的作用域是由定义它所在的**block**所决定的(所谓 "作用域"，是指在程序中允许你引用变量的范围)。更准确地说，一个变量的作用域从它的定义开始，到退出定义它的块时结束。在这之前，函数体是唯一的**block**，所以一个变量在定义后可以在`main`中的任何一点使用。但有了复合语句后，就比较复杂了。这里将谈谈C语言中的作用域是如何工作的；如果你已经熟悉了这一点，你可以跳到下一节。

如果一个变量是在内部作用域中定义的，那么它就不能在外部作用域中被访问：

```
// here is the outer scope
{
    // here is the inner scope
    int foo = 2;
}

// now we're back in the outer scope
foo = 3; // ERROR - foo isn't defined in this scope!
```

然而，在内部作用域的代码可以访问外部作用域的变量：

```
int a = 2;
{
    a = 4; // this is okay
}
return a; // returns 4 - changes made inside the inner scope are reflected here
```

你不能在同一个作用域内有两个同名的变量：

```
int foo = 0;
int foo = 1; //This will throw a compiler error
```

但是你可以在*不同的*作用域中拥有两个同名的变量。一旦声明了内部作用域中的变量，它就会对外部作用域中的变量产生遮蔽（shadow）作用；外部变量将无法访问，直到内部变量离开作用域：

```
int foo = 0;
{
    int foo; // this is a TOTALLY DIFFERENT foo, unrelated to foo from earlier
    foo = 2; // this refers to the inner foo; outer foo is inaccessible
}
return foo; //this will return 0 - it refers to the original foo, which is unchanged
```

这里的关键点是，内部变量和外部变量`foo`是两个完全不相关的变量，只是碰巧有相同的名字。当我们在内部代码块中时，外部变量`foo`仍然存在，但我们没有办法引用它，因为现在引用的是内部变量`foo`。

但是，请注意，外部的`foo`在内部代码块中，在它被遮蔽之前是可以访问的：

```
int foo = 0;
{
    foo = 3; //changes outer foo
    int foo = 4; //defines inner foo, shadowing outer foo
}
return foo; //returns 3
```

## 词法分析

复合语句不需要任何新的标记，所以我们本周不需要对词法分析进行修改。

## 语法解析

这是目前我们AST中对语句（statements ）的定义：

```
statement = Return(exp) 
          | Exp(exp)
          | Conditional(exp, statement, statement option) //exp is controlling condition
                                                          //first statement is 'if' block
                                                          //second statement is optional 'else' block
```

我们只需要在这个定义中添加一个 "Compound  "语句。还记得我们在上一个lab中给AST添加了一个`block_item`节点：

```
block_item = Statement(statement) | Declaration(declaration)
```

复合语句只是一个语句和声明的列表，所以我们对语句的新定义将是这样的：

```
statement = Return(exp) 
          | Exp(exp)
          | Conditional(exp, statement, statement option) //exp is controlling condition
                                                          //first statement is 'if' block
                                                          //second statement is optional 'else' block
          | Compound(block_item list)
```

我们将对条件表达式和条件语句进行完全不同的解析。语句比较简单，所以我们先处理这些语句。

现在让我们更新一下语法。`blocks`的规则非常简单：

```
"{" { <block-item> } "}
```

请注意，`"{" "}"`是大括号，`{ }`表示重复。这很难读懂! 但这只是意味着我们用大括号包裹了任意数量的`block items`--如果你参考一下`<function>`的语法，你就会发现我们定义函数体的方式完全相同。

把所有这些放在一起，我们更新后的语法是这样的：

```
<statement> ::= "return" <exp> ";"
              | <exp> ";"
              | "if" "(" <exp> ")" <statement> [ "else" <statement> ]
              | "{" { <block-item> } "}
```

#### ☑任务

更新解析过程，以处理`blocks`。它应该成功解析step[1-7]的所有例子。

## 代码生成

正如我们前面所看到的，有可能有两个不同的变量，在两个不同的作用域中，存储在栈的两个不同的位置，但名称相同。下面是这样一个例子：

```
int foo = 3;
{
  int foo = 4;
}
```

因此，每当程序引用变量`foo`时，我们生成的代码就需要在栈上访问正确的`foo`--如果`foo`已经超出了范围，则会引发一个错误。本次试验的代码生成步骤就是管理和访问变量映射表，所以我们总是能查找到正确的`foo`。

这里的诀窍是，**每个`block`都有一个对应且独立的变量映射表（variable map）**。这样一来，在内部作用域中定义（或重新定义）一个变量就不会干扰到外部作用域。而且如果你使用的是一个不可变（immutable ）的映射（应该是这样），每个块都必然会得到自己的变量映射，所以这种方法很简单。

让我们来看一些伪代码。在lab 5之后，你生成函数体的代码大概是这样的：

```
def generate_function_body(body):
  // initialize variable map and stack index
  var_map = Map()
  stack_index = -4

  //process statements one at a time
  for statement in body:
    var_map, stack_index = generate_statement(statement, var_map, stack_index) 
```

注意`generate_statement`必须返回一个新的`var_map`。每一个声明都会更新变量映射表（或者更准确地说，创建一个新的变量映射表），在lab5中，`generate_statement`也处理了声明（declarations）。每当我们处理一个声明时，都需要返回最新的、最大的变量映射表，这样未来的语句就可以引用我们刚刚声明的变量。

但是在上一篇文章中，我们在AST中把语句和声明分开了，所以你可能把最后一行改成了。

```
    var_map, stack_index = generate_statement_or_declaration(statement, var_map, stack_index) 
```

在这一点上，声明会创建一个新的变量映射，但语句不会。无论在语句中发生什么--包括复合语句，它本身可能包含声明--都不会对包围作用域的变量映射产生影响。一旦你理解了这一点，处理嵌套作用域就很容易了：

```
def generate_function_body(body):
  // initialize variable map and stack index
  var_map = Map()
  stack_index = -4

  //process statements one at a time
  for block_item in body:
    if block_item is a declaration:
        //update the variable map
        var_map, stack_index = generate_declaration(statement, var_map, stack_index)
    else:
        //don't update the variable map
        generate_statement(statement, var_map, stack_index)
```

当然，你需要将`generate_function_body`泛化为`generate_block`；生成函数体和其他任何`block`之间的一个区别是，你需要在函数体开始时，初始化你的空变量映射和栈索引。

现在让我们通过一个小例子来看看这样做是如何为不同的作用域维护正确的变量映射的：

```
int main(){
    // 1) function body
    {   // 2) block
        int a = 2; // 3) variable declaration
        a = 3; // 4) variable reference
    }
    return a; // 5) return statement
}
```

1. 用`generate_block`处理函数体，现在已经有了一个空的变量映射表。
2. 递归调用`generate_block`来处理内部块（ inner block）。变量映射表仍然是空的。
3. 这是一个声明，所以我们将`a`添加到变量映射表中（在实现上，我们创建一个包含`a`的变量映射的副本，因为所有这些映射都是不可变的）。
4. 我们在步骤3的变量映射表中查找`a`在栈中的位置。
5. 5.回到外层作用域，`var_map`指的是原始的、空的变量映射表。由于`a`没有在这个映射中定义，这将会抛出一个错误。

处理声明的代码也需要修改。lab 5中处理声明的伪代码包括这一行：

```
if var_map.contains("a"):
  fail() //shouldn't declare a var twice
```

现在这是不正确的，只要声明的变量不在同一个作用域中，那么声明两个同名的变量是合法的。为了解决这个问题，我们需要一种方法来区分定义在当前作用域中的变量，和定义在外部作用域中的变量。一个解决方案是维护一组定义在当前作用域中的变量，这意味着`generate_block`现在的样子是这样的：

```
def generate_block(block, var_map, stack_index):

  current_scope = Set()

  //process statements one at a time
  for block_item in block:
    if block_item is a declaration:
        //update the variable map
        var_map, stack_index, current_scope = generate_declaration(statement, var_map, stack_index, current_scope)
    else:
        //don't update the variable map
        generate_statement(statement, var_map, stack_index)
```

最后，我们检查`current_scope`，而不是`var_map`，检查是否有重复的变量声明，并在成功时将变量添加到两个结构中：

```
if current_scope.contains("a"):
  fail() //shouldn't declare a var twice in the same scope
else:
  //emit assembly, update stack_index and var_map as before...
  new_scope = current_scope.add("a")
  return (var_map, stack_index, current_scope)
```

这个解决方案感觉很tricky，也许你能想出更好的方案。

现在，如果`a`在一个内部作用域中被重新定义，它只是覆盖了变量映射表中的旧`a`，所以这个作用域和任何内部作用域将使用正确的栈位置，对应于`a`的最内部定义。这完全不会影响外层作用域，因为外层作用域仍然使用原始的、未修改的变量映射表。

### 释放变量

我们已经小心翼翼地管理变量映射表，以防止一个`block`干扰其包围范围内的任何变量声明。但是有一个我们无法避免的副作用：分配一个变量会改变栈指针。这是个问题，因为栈指针和我们的`stack_index`变量会不同步。考虑下面的例子：

```
int main() {
  {
    int i = 0;
  }
  int j = 1;
  return j;
}
```

一开始，变量映射表是空的，`stack_index`是`-4`，因为栈的第一个空闲槽（empty spot）是在EBP下面的4个字节的位置：

![EBP and ESP point to the same location, the lowest address on the stack; the stack index points to the address just below it.](./lab7-pics/bad_stack_pointer.svg)

当我们在这个例子中用`generate_block`处理`block`时，我们将把`i`推到（push）栈上。

```asm
    movl $0, %eax
    push %eax
```

现在`ESP` 位于 `EBP - 4`的位置, and `stack_index` is `-8`：

![ESP points at the address just below EBP on the call stack, which holds literal value 0. the stack index points just below that value. An entry in the variable map associates i with address EBP - 4](./lab7-pics/bad_stack_pointer_2.svg)

在我们退出`block`之后，我们忘记了我们分配了`i`。这意味着`i`已经不在我们的变量映射表中了，而我们仍然使用我们原来的栈索引`-4`工作；记住`generate_block`并不返回栈索引。我们*应该忘记`i`，因为它不在范围内。

问题是，`i`仍然存在，因为ESP仍然指向它。

![ESP and stack index both point at EBP - 4, the address where i was allocated. The variable map is empty.](./lab7-pics/bad_stack_pointer_3.svg)

所以，当我们push  "j "时，它将在 "i "的下方，在EBP-8处：

```asm
  movl $1, %eax
  push %eax
```

![ESP and the stack index both point at EBP - 8, which contains literal value 1. However, the variable map associates j with EBP - 4. ](./lab7-pics/bad_stack_pointer_4.svg)

但是由于栈索引是`-4`，我们将在变量映射表中添加一个从`j`到`-4`的映射。以后对`j`的任何引用（比如在返回语句中）都会错误地使用`i`的栈位置。

我们可以通过让`generate_block`返回一个栈索引来解决这个问题，但最好是在`generate_block`结束时，直接从栈中弹出变量。`current_scope`的大小可以告诉我们需要弹出多少个变量：

```
def generate_block(block, var_map, stack_index)

  current_scope = Set()
  ...as before...

  bytes_to_deallocate = 4 * current_scope.size()
  emit "    addl ${}, %esp".format(bytes_to_deallocate)
```

#### ☑任务

更新代码生成阶段的代码，以正确处理复合语句。并在step[1-7]中的例子上成功。

## 下一步

在接下来的试验中，我们将添加 "for"、"do "和 "while "循环。

## 参考

- [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf)
- [Writing a C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)