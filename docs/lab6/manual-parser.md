## 手写 parser 简单实例

### 定义变化

增加两种新节点的同时，需要增加 Node 的内容。

```
struct NodeKind {
+	ND_IF,
+	ND_TERN,		// :? 运算
}

struct Node {
+	Node* cond;		// 储存条件表达式
+	Node* then;		// 储存条件判断成功时执行的语句（返回的表达式）
+	Node* else;		// 储存条件判断失败时执行的语句（返回的表达式）
}
```

注意，对于 `:?`运算符，`then` 和 `else` 是两个表达式节点， 对于 if 语句，这两个变量是两个语句节点。

### 解析变化

按照生成式变化改变即可。if 语句示例如下：

```c++
Node* stmt() {
    // ...
    // IF statement
    if (parse_reserved("if")) {
        assert(parse_reserved("("));
        node = new_node(ND_IF);
        node->cond = expr();
        assert(parse_reserved(")"));
        node->then = stmt();
        if(parse_reserved("else"))
            node->els = stmt();
        return node;
    }
    // ...
}
```

以后同质化的内容不再展示。