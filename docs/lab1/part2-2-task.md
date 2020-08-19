#### ☑任务：

编写一个*parse*函数，接受一个标记列表，并返回一个AST，根节点（root node）是Program节点。该函数应该为所有有效的[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)建立正确的AST。如果你愿意，你也可以让你的解析器在遇到超过INT_MAX（整数最大值）的整数常量时优雅地失败并指出解析失败的原因。

有很多方法可以在代码中表示AST--每种类型的节点可以是它自己的类或它自己的数据类型，这取决于你用什么语言来编写编译器。例如，以下是你如何将AST节点定义为数据类型伪代码：

```
type exp = Const(int)
type statement = Return(exp)
type fun_decl = Fun(string, statement)
type prog = Prog(fun_decl)
```