# 手写简单 parser

程序定义出现变化：

```cpp
struct Program {
-    Function* func;
+    std::list<Function> funcs;
}
```

程序解析对应发生变化：

```cpp
Program* parse() {
    Program* prog = new Program();
    while(not_end()) {
        Function *fn = function();
        prog->funcs.push_back(fn);
    }
    return prog;
}
```

函数解析需要新增对于函数参数的解析，同时函数定义发生变化。

```cpp
struct Function {
+    std::list<Var*> args;
}

Function *function() {
    assert(type());
    char *name;
    parse_ident(name);
    Function *fn = new Function(name);
    parse_reserved("(");
+   fn->args = func_args();    
    parse_reserved(")");
    parse_reserved("{");
    while (!parse_reserved("}")) {
        fn->nodes.push_back(stmt());
    }
    return fn;
}
```

对函数调用的节点定义：

```cpp
struct FuncCall {
    char* name;
    std::list<Node*> args;
};

struct Node {
+    FuncCall* func_call;
}
```

对函数调用的解析，同时完成名称解析和参数检查（目前之要求数量相同）。

```cpp
Node* primary() {
    // ...
    char* name;
    if (parse_ident(name)) {
        parse_reserved("(")
        Node *node = new_node(ND_FUNC_CALL);
        // func_call() 完成对于 args 的解析，循环解析 expr, `,` 即可
        assert(node->func_call = func_call(name));
        // 不能调用未声明函数
        Function* fn;
        assert(fn = find_func(node->func_call->name));
        // 参数必须相同
        assert(fn->args.size() == node->func_call->args.size());
        return node;
    }
    // ...
}
```

这里没有展示如何与局部变量应用做区分，想想该如何做？

