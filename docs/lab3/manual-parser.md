## 手写 parser 简单实例

### 定义变化

```c++
struct Node {
-	Node* expr;
+	Node* lexpr;
+	Node* rexpr;
}
```

现在需要储存两个 expression。

### parse 过程变化

按照产生式变化对应修改即可，很简单。

```c++
expression
    : additive

additive
    : multiplicative
    | additive ('+'|'-') multiplicative
    
// ...

primary
    : Integer
    | '(' expression ')'
```

加法示例：

```c++
Node* additive() {
	Node* node = multiplicative();
	while(parse_reserved("+")) {		//这里只展示了 `+`, `-`同理
		node = new_binary(ND_ADD, node, multiplicative());
	}
    return node;
}

Node* new_binary(NodeKind kind, Node* lexpr, Node* rexpr); // 类似构造函数，简单赋值
```

注意左结合性，请思考为何这么写能够保证左结合。如果一种算法是右结合的，应该怎样写呢？