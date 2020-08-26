# Visitor 模式速成
编译器的构造中会使用到很多设计模式，Visitor 模式就是常见的一种。
基础的设计模式都在 OOP 课程中覆盖，这里重提一下 Visitor 模式，顺带介绍一些参考代码用到的 python 技巧。

我们知道，编译器里有很多的树状结构。
最典型的就是，源程序通过上下文无关文法解析后，得到的语法分析树。
Visitor 模式的目的，就是遍历这些树状结构，本质就是一个 DFS 遍历。

下面通过一个例子说明 Visitor 模式。

## 表达式语法、语法树定义
我们有一个很简单的表达式文法，终结符包括整数和加减乘除模操作符，起始符号是 `expr`，大致如下

```
expr    -> int | binary

int     -> Integer

binary  -> expr '+' expr
        |  expr '-' expr
        |  expr '*' expr
        |  expr '/' expr
        |  expr '%' expr
```

这个文法有二义性，同样的字符串可能有多个语法分析树。
不过解析字符串、生成语法分析树不是 Visitor 模式的工作。
Visitor 模式只考虑某个确定的语法分析树。
如下面是 `20-13*3` 的一颗语法分析树

![图](./pics/parsetree.svg)

我们在代码里这样定义这个语法分析树（python 3.6）：

```python
class Node:
    pass

class IntNode(Node):
    def __init__(self, v:int): # 类型标注是给人看的，python 不检查
        self.v = v

    def __str__(self):
        return f"({self.v})" # f-string 特性

class BinopNode(Node):
    _legalOps = { *"+-*/%" }  # 使用 unpacking operator，等价于 set('+', '-', '*', '/', '%')
    def __init__(self, op:str, lc:Node, rc:Node):
        assert op in BinopNode._legalOps
        self.op, self.lc, self.rc = op, lc, rc

    def __str__(self):
        return f"({self.lc} {self.op} {self.rc})"

# 我们通过某种手段，得到了这么一个语法分析树
expr1 = BinopNode('*', BinopNode('-', IntNode(20), IntNode(13)), IntNode(3))
print(expr1) # (((20) - (13)) * (3))
```

我们忽略了 `Expr`，不过显然这无伤大雅。

## 表达式求值
显然，每个语法分析树都对应一个（加好括号）的表达式，比如上面的树就对应 `(20-13)*3`。
那么我们考虑一个问题：如何对这个表达式求值？

当然，我们可以让 python 帮我们做 `print(eval(str(expr1), {}, {}))`，
不过我们下面会用 Visitor 模式实现表达式求值。

写 Visitor 之前，我们看自己实现表达式求值的最简单的方法，一个递归遍历：
```python
def dfs(node:Node):
    if isinstance(node, IntNode):
        return node.v
    if isinstance(node, BinopNode):
        lhs = dfs(node.lc)
        rhs = dfs(node.rc)
        if node.op == "+": return lhs + rhs
        if node.op == "-": return lhs - rhs
        if node.op == "*": return lhs * rhs
        if node.op == "/": return lhs / rhs
        if node.op == "%": return lhs % rhs

print(dfs(expr1)) # 21
```

`dfs` 函数接受一个结点，然后对这个结点代表的子树进行求值，返回求值结果。
容易看出，`dfs` 函数根据被遍历的结点类型不同，执行不同的求值逻辑。
那么我们把这些求值逻辑封装到一个类里面，就得到了一个最简单的 Visitor。

```python
class EvaluationVisitor:
    def visit(self, node:Node):
        if isinstance(node, IntNode):
            return self.visitIntNode(node)
        if isinstance(node, BinopNode):
            return self.visitBinopNode(node)

    def visitIntNode(self, node:IntNode):
        return node.v

    def visitBinopNode(self, node:BinopNode):
        # 不确定子结点的类型，所以只能调用 visit 而非 visitIntNode 或者 visitBinopNode
        lhs = self.visit(node.lc)
        rhs = self.visit(node.rc)
        if node.op == "+": return lhs + rhs
        if node.op == "-": return lhs - rhs
        if node.op == "*": return lhs * rhs
        if node.op == "/": return lhs / rhs
        if node.op == "%": return lhs % rhs

print(EvaluationVisitor().visit(expr1)) # 21
```

上面就是 Visitor 的核心思想，实际使用中我们一般会有两点改进
1. 不使用 `isinstance` 来判断结点类型，而是调用结点自身的一个 `accept` 函数
2. 把几个 `visitXXX` 函数抽象到一个接口里，各种具体的 Visitor 来实现这个接口

改进后的 Visitor 如下。
```python
class Node:
    def accept(self, visitor):
        pass

class IntNode(Node):
    # ... 同上
    def accept(self, visitor):
        return visitor.visitIntNode(self)

class BinopNode(Node):
    # ... 同上
    def accept(self, visitor):
        return visitor.visitBinopNode(self)

class Visitor: # 默认行为是遍历一遍，啥也不做，这样比较方便
    def visitIntNode(self, node:IntNode):
        pass

    def visitBinopNode(self, node:BinopNode):
        node.lc.accept(self)
        node.rc.accept(self)

class EvaluationVisitor(Visitor):
    def visitIntNode(self, node:IntNode):
        # ... 同上

    def visitBinopNode(self, node:BinopNode):
        lhs = node.lc.accept(self)
        rhs = node.rc.accept(self)
        # ... 同上
```

## 总结
从上面可以看到，Visitor 模式的要素有
1. 被访问的对象。例如上面的 `Node`。
2. Visitor 封装的 `visitXXX`，表示对上述对象实施的操作。例如 `EvaluationVisitor`。

每种被访问的对象在自己的定义中都有一个 `accept` 函数，并且在 Visitor 里面也对应一个 `visitXXX` 函数。

## 有状态的 Visitor
```python
subexpr = BinopNode('-', IntNode(20), IntNode(13))
expr1 = BinopNode('*', subexpr, IntNode(3))
```

显然，表达式求值的过程中，所有子表达式也都会被求值。
如上，求值 `expr1` 的过程中，`subexpr` 也也会被求值。
我们想把子表达式的值记录下来，以后直接使用，就不需要对子表达式重新求值了。

为了实现这点，还是使用上面的 `EvaluationVisitor`，但我们用一个字典 `Node -> int` 记录求值结果，并且把字典作为 Visitor 的状态。
```python
class EvaluationVisitor2(Visitor):
    def __init__(self):
        self.value = {} # Node -> int
```

每次 `EvaluationVisitor2.visitXXX(self, node)` 返回的时候，我们都记录一下 `self.value[node] = value`，其中 `value` 是返回值。
我们用一个函数修饰器来完成记录的动作，如下

```python
class EvaluationVisitor2(Visitor):
    def __init__(self):
        self.value = {} # Node -> int

    def SaveValue(visit): # decorator
        def decoratedVisit(self, node):
            value = visit(self, node)
            self.value[node] = value
            return value
        return decoratedVisit

    @SaveValue
    def visitIntNode(self, node:IntNode):
        return node.v

    @SaveValue
    def visitBinopNode(self, node:BinopNode):
        lhs = node.lc.accept(self)
        rhs = node.rc.accept(self)
        if node.op == "+": return lhs + rhs
        if node.op == "-": return lhs - rhs
        if node.op == "*": return lhs * rhs
        if node.op == "/": return lhs / rhs
        if node.op == "%": return lhs % rhs

subexpr = BinopNode('-', IntNode(20), IntNode(13))
expr1 = BinopNode('*', subexpr, IntNode(3))
visitor = EvaluationVisitor2()
expr1.accept(visitor)
print(visitor.value[subexpr]) # 7
print(visitor.value[expr1]) # 21
```
