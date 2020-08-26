# 词法分析

本阶段需要引入两种新的标记：左中括号`[`和右中括号`]`。

例子：

```c
int main() {
  int a[10];
  return 0;
}
```

这个程序中`int a[10];`这个片段对应的标记列表是：

```
Keyword int
Identifier a
Open bracket [
Integer literal 10
Close bracket ]
Semicolon ;
```