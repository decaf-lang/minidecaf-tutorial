# Visitor 模式速成
编译器的构造中会使用到很多设计模式，Visitor 模式就是常见的一种。 基础的设计模式都在 OOP 课程中覆盖，这里重提一下 Visitor 模式，并以框架中的代码为示例进行介绍。

我们知道，编译器里有很多的树状结构。最典型的就是，源程序通过上下文无关文法解析后，得到的抽象语法树。在语义分析和中间表示生成两个步骤中，我们都需要遍历整个抽象语法树。Visitor 模式的目的，就是对遍历树状结构的过程进行封装，本质就是一个 DFS 遍历。

让我们考虑 step1 的文法：

```
program : function
function : type Identifier '(' ')' '{' statement '}'
type : 'int'
statement : 'return' expression ';'
expression : Integer
```

以这个文法对应的一段 MiniDecaf 代码为示例：

```C
int main() {
    return 2;
}
```

它会对应如下的 AST 结构：

```
program
  function
    type(int)
    identifier(main)
    param_list
    return
      int(2)
```

> 我们用缩进表示树结构，其中 program, function, type, identifier, param_list, block, return, int 等均为 AST 上的结点类型。

## Python 框架

在框架中，我们有以下的 AST 结点类实现（进行了适当的简略）：

```python
'''
frontend/ast/node.py
'''
class Node: # 所有 AST 结点的基类
    # ...
'''
frontend/ast/tree.py
'''
class Program(ListNode[Union["Function", "Declaration"]]): # 程序，AST 的根结点类型
    # ...
class Function(Node): # 函数
    # ...
class Statement(Node): # 语句基类
    # ...
class Return(Statement): # return 语句
    # ...
class TypeLiteral(Node): # 类型基类
    # ...
class TInt(TypeLiteral): # 整型
    # ...
```

假设在经过了词法分析和语法分析后，我们已经成功将 MiniDecaf 代码转化为了 AST 结构。现在，我们想要编写代码对 AST 进行扫描。很容易写出递归的 DFS 遍历：

```python
def dfs(node: Node):
    if isinstance(node, Program):
        for func in node.functions:
            dfs(func)
    elif isinstance(node, Function):
        # do something for scanning a function node
    elif isinstance(node, Return):
        # ...
```

dfs 函数接收一个结点，根据这个结点的类型进行深度优先遍历。容易看出，dfs 函数根据被遍历的结点类型不同，执行不同的遍历逻辑。 那么我们把这些遍历逻辑封装到一个类里面，就得到了一个最简单的 Visitor。此外，为了便于实现，我们不使用 isinstance 来判断结点类型，而是调用结点自身的一个 accept 函数，并把不同的 visitXXX 函数抽象到一个接口里，各种具体的 Visitor 来实现这个接口。

```python
'''
frontend/ast/node.py
'''
class Node: # 所有 AST 结点的基类
    def accept(self, v: Visitor[T, U], ctx: T) -> Optional[U]:
        raise NotImplementedError
'''
frontend/ast/tree.py
'''
class Program(ListNode[Union["Function", "Declaration"]]):
    # ...
    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitProgram(self, ctx)
class Function(Node):
    # ...
    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitFunction(self, ctx)
# ...
'''
frontend/ast/visitor.py
'''
class Visitor(Protocol[T, U]):
    def visitOther(self, node: Node, ctx: T) -> None:
        return None
    def visitProgram(self, that: Program, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    def visitFunction(self, that: Function, ctx: T) -> Optional[U]:
        return self.visitOther(that, ctx)
    # ...
```

之后，如果我们想要编写一种遍历 AST 的方法，可以直接继承 Visitor 类，并在对应结点的 visit 成员方法下实现对应的逻辑。例如，框架中用如下的方法进行符号表构建：

```python
class Namer(Visitor[ScopeStack, None]):
    def visitProgram(self, program: Program, ctx: ScopeStack) -> None:
        # ...
        for child in program:
            if isinstance(child, Function):
                child.accept(self, ctx)    
    def visitFunction(self, func: Function, ctx: ScopeStack) -> None:
        # ...
    # ...
```

如果想要访问某个子结点 child，直接调用 child.accept(self, ctx) 即可。

## C++ 框架

在框架中，我们有以下的 AST 结点类实现（进行了适当的简略）：

```C++
// ast/ast.hpp
class ASTNode { // 所有 AST 结点的基类
public:
    virtual NodeType getKind (); // 返回结点类型
    // ...
};
class FuncDefn : public ASTNode { // 所有函数
    // ...
};
class Statement : public ASTNode { // 语句基类
    // ...
};
class ReturnStmt : public Statement { // return 语句
    // ...
};
class Type : public ASTNode { // 类型基类
    // ...
};
class IntType : public Type { // 整型
    // ...
};
```

假设在经过了词法分析和语法分析后，我们已经成功将 MiniDecaf 代码转化为了 AST 结构。现在，我们想要编写代码对 AST 进行扫描。很容易写出递归的 DFS 遍历：

```C++
void dfs(ASTNode *node) {
    if (node->getKind() ==  NodeType::PROGRAM) {
        for (auto &&item : ((Program*)node)->func_and_globals) {
            dfs(item);
        }
    } else if (node->getKind() == NodeType::FUNC_DEFN) {
        // do something for scanning a function node
    } else if (node->getKind() == NodeType::RETURN) {
        // ...
    }
}
```

dfs 函数接收一个结点，根据这个结点的类型进行深度优先遍历。容易看出，dfs 函数根据被遍历的结点类型不同，执行不同的遍历逻辑。 那么我们把这些遍历逻辑封装到一个类里面，就得到了一个最简单的 Visitor。此外，为了便于实现，我们不使用 getKind 来判断结点类型，而是调用结点自身的一个 accept 函数，并把不同的 visitXXX 函数抽象到一个接口里，各种具体的 Visitor 来实现这个接口。

```C++
// ast/ast.hpp
class ASTNode { // 所有 AST 结点的基类
public:
    virtual void accept(Visitor *) = 0;
};
class Program : public ASTNode {
public:
    void accept(Visitor *v) override {
        // 仅作示意，实际实现在对应的 .cpp 文件里
        v->visit(this);
    }
};
class FuncDefn : public ASTNode {
public:
    void accept(Visitor *v) override {
        // 仅作示意，实际实现在对应的 .cpp 文件里
        v->visit(this);
    }
};
// ast/visitor.hpp
class Visitor {
public:
    virtual void visit(Program *) {}
    virtual void visit(FuncDefn *) {}
};
```

之后，如果我们想要编写一种遍历 AST 的方法，可以直接继承 Visitor 类，并在对应结点的 visit 成员方法下实现对应的逻辑。例如，框架中用如下的方法进行符号表构建：

```C++
class SemPass1 : public Visitor {
    void visit(ast::Program* prog) {
        // ...

        // visit global variables and each function
        for (auto it = prog->func_and_globals->begin(); it != prog->func_and_globals->end(); ++it) {
            (*it)->accept(this);
            // ...
        }
        // ...
    }
}
```

如果想要访问某个子结点 child，直接调用 child.accept(self, ctx) 即可。