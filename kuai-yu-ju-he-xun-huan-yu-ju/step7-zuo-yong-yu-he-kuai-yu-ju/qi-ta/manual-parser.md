# 手写简单 parser

## 定义变化

处理块语句时需要记录块若干条语句的信息，可以对 `Node` 进行这样的修改:

```cpp
struct Node {
+    std::list<Node*> body;
}
```

