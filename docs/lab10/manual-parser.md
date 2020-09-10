## 手写 parser 简单实例

`Program`的构成再次发生变化，需要调整相关定义和解析方式，总体难度较小。这里仅作简单提示。

#### 如何区分全局变量和函数？

根据产生式，二者关键不同在于名称之后是否带一个　`(`　。

```c++
// 实际上这么写肯定不好
bool is_func() {
    return type() && parse_ident() && parser_reserved("(");
}
```

