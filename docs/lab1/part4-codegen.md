## 代码生成

现在我们已经建立了一个AST，我们已经准备好生成汇编代码了！就像我们之前看到的，我们只需生成四行汇编码。为此，我们将大致按照程序执行的顺序遍历AST。这意味着我们将按顺序访问：

- 函数名： function name  (不是真正的node，而是`function definition`node中的一个属性)
- 返回值：return value
- 返回语句：return statement

> 注意，我们经常（虽然并不总是）以[post-order](https://en.wikipedia.org/wiki/Tree_traversal#Post-order)的方式遍历树，在其父类之前访问子类。例如，我们需要在返回语句中引用返回值之前生成它。在后面的s试验中，我们需要在生成对算术表达式进行操作的代码之前，生成算术表达式的操作数。

下面是我们要生成汇编码：

1. 要生成一个函数（如函数 "foo"）。

```
    .globl foo
   foo:
    <FUNCTION BODY GOES HERE>
```

2. 生成一个返回语句（如：`return 3;`）的汇编码

```
    movl    $3, %eax
    ret
```