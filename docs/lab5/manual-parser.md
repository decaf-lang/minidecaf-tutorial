## 手写 parser 简单实例

推荐你先阅读本节其他部分，了解对局部变量的处理方式。

### 定义变化

```c++
struct Node {
+	Var* var;
}

// 如果你要进行名称解析，具体内容见下
struct Var {
    char* name;
    int offset;		// 在栈中距离 fp 的 offset
    Node* init;		// 初始化的值
}
```

### parse 变化

语句类别变多了：

```c++
Node* stmt() {
    Node* node = NULL;
    Type* ty;
    // Return statement
    if (parse_reserved("return")) {   
        node = new_stmt(ND_RETURN, expr());
        assert(parse_reserved(";"));
        return node;
    }
    // 局部变量声明
    if (type()) {
        return declaration();
    }
    // 直接由表达式构成的语句，注意 a = 1; 就是此类，有一个表达式的值没有用到
    node = expr();
    assert(parse_reserved(";"));
    return new_stmt(ND_UNUSED_EXPR, node);
}
```

具体的 `declaration()`等按照生成式很容易写出来。

你可以在 parse 中一并完成名称解析（也就是在变量被引用时确定到底引用了哪一个变量，变量的本质区别是 offset，这一步完成一个从名称到 offset 的映射），也可以后续专门遍历 AST 来实现这一步。

### 名称解析

在声明时维护已声明变量信息，可以简单加入一个链表，也可以使用你喜欢的数据结构来维护它。

```c++
Node* declaration() {
    // type() 已经在 stmt() 中完成
    char* name;
    assert(parse_ident(name));
    Var* var = new Var(name);
    // 这里储存已经声明变量的信息，为名称解析做准备
    add_local(var);				
    // 如果进行了初始化
    if (parse_reserved("=")) {
        var->init = expr();
    }
    assert(parse_reserved(";"));
    Node* node = new_stmt(ND_DECL);
    node->var = var;
    return node;
}
```

在被引用时：

```c++
Node* primary() {
    // ...
    char* name;
    if (parse_ident(name)) {
        // find_var 负责寻找同名变量, 在 add_local 维护的数据结构中寻找即可
        Var* var = find_var(name);
        return new_var_node(var);
    }
    // ...
}
```

注意 `add_local()`应该可以完成 offset  的确定。