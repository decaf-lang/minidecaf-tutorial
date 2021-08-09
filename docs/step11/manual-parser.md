## 手写 parser 简单实例

### 定义变化

引入了新类型数组，你可以这样定义类型。注意，你可以有自己的定义方式，这种定义稍显复杂。

```c++
enum TypeKind {
    TY_INT,
    TY_PTR,
    TY_ARR,
};

struct Type {
    TypeKind kind;
    // 数组大小可变，其余类型皆为 4
    // 数组 size = elem_size * arr_len
    int size;
    // 数组元素的类型，可能是另一个数组
    Type* base;
    // 数组长度
    int arr_len;
    // 数组元素大小， elem_size = base->size，可省略
    int elem_size;
    // 数组维度
    int arr_dim;
};

struct Node {
    // 用于记录数组被引用时的 index
+	std::list<Node*> arr_index;
}
```

### 声明解析

注意对于类型的解析要分成两部分。

```c++
Node* declaration() {
    Type* ty = type();
    char* name;
    assert(ty && parse_ident(name));
    // 这里完成对 index 后缀的解析，最终确定类型
    // suffix 消耗若干个 `[` num `]`
    ty = suffix(ty);
    // ...
    return node;
}
```

### 引用解析

对于 index 后缀的解析比较简单，注意：

* minidecaf 允许数组和指针两种类型的变量进行 index 运算，但是意义完全不同。

* 仔细计算最终生成节点的类型。