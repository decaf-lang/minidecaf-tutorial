## 手写 parser 简单实例

新增的两种单目操作和很容易实现，不做赘述。

你需要调整 `type()`使它能够正确的处理指针类型，一个循环的事，不做赘述。

### 类型系统

你可以在 parse 阶段一并完成类型检查。

首先，引入类型系统。注意，相关的结构体定义不一定要一样，你可以有自己的定义方式。

```c++
enum TypeKind {
    TY_INT,
    TY_PTR,
};

// 事实上，minidecaf （即便是lab12）不需要这么复杂的类型，你可以仅仅记录指针的重数，请根据自己的理解灵活实现
struct Type {
    TypeKind kind;
    // int size;  目前的 minidecaf 中，为一常量 4，lab12 才出现其他长度的类型
    // int align; 目前的 minidecaf 中，为一常量 4
    Type* base;
};

// 注意：Node 的类型的意义是，这个节点所代表的表达式的类型，语句节点没有类型。
struct Node {
+	Type* ty;
    // 你可以通过左值计算得到每个节点是不是左值，但真的需要这么复杂吗？
+	bool is_lvalue;
}

// 函数和变量也需要增加类型字段
```

引入类型比较的函数

```c++
bool type_equal(Type*, Type*);
```

在 parse 的同时计算类型。基础节点（也就是 primary 节点，包含变量、函数调用、数字字面量）返回的类型可以直接确定，其余节点的类型需要根据操作数的类型做计算。比如：如果允许指针加减(这被放在了 lab12 )，那么加法运算的结果可能是整数，也可能是指针，对应节点的类型类似，但是乘法运算一定会返回一个整数。此外还需要在构造节点的同时进行类型检查，具体内容参见[这里](./typeck.md)。

类型计算:

```c++
Node* factor() {
    // function call
	node->ty = fu->ret_ty;
    // variable
    node->ty = var->ty;
    // num
    node->ty = int_type();
}

Node* add() {
    // 如果允许指针加减，lab11 的加法运算和乘法的类型要求一致，只能计算整数
    if(is_integer(node->lexpr) && is_integer(node->rexpr)) {
        node->ty = int_type();
    }
}
```

类型检查：

```c++
Node* mul() {
    // 乘法两个操作数必须都是整数
    assert(is_integer(node->lexpr) && is_integer(node->rexpr);
    // 必定产生整数
    node->ty = int_type();
}
           
Node* assign() {
    // 赋值要求双方类型相同
    assert(type_equal(node->lexpr, node->rexpr));
    // 节点类型就是左操作数或者右操作数的类型
    node->ty = node->lexpr->ty;
}
```

类型计算后，你必须保证每一个表达式节点都有正确的类型。类型检查需要在类型出错时报错报错。

### 左值计算

左值计算可以通过可类型计算相似的方式进行。

### 强制类型转换

强制类型转换容易与括号表达式（`( expr )`）相混淆，我们需们需要知道括号后的 token 类型才能作出判断，这里介绍一种作弊的方式：可以不必严格遵循 LL1 的解析方式，我们可以实现一个撤销操作。

```c++
void checkout_token();
```

功能是与 `next_token()`相反，这样，我们可以在错误的消耗掉 token 之后回退到之前的状态。

强转可以这样写：

```c++
Node* cast() {
	if (parse_reserved("(")) {
        Type* ty;
        if(ty = parse_type()) {
            assert(parse_reserved(")"));
            Node* node = new_cast(unary(), ty);
            return node;
        }
        // 这表明这其实是一个括号表达式，我们应该撤销对于 `(` 的消耗。
        // 当然，你也可以在解析 `(` expr `)` 的时候直接跳过对 `(` 的解析。
        // 请灵活实现
        checkout_token();
    } 
}
```

