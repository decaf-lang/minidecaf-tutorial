## 手写 parser 简单实例

* 节点定义变化

    增加三种表达式节点，分别为：按位取反、取负、逻辑取反

    ```c++
    struct NodeKind {
        ND_NEG,
        ND_NOT,
        ND_BITNOT,
    }
    ```

    这一变化很简单，以后省略。

* parse 过程变化

  `expr()` 解析一个单目操作。

  ```c++
  Node* expr() {
  	return unary();
  }
  
  Node* unary() {
      if(parse_reserved("-")) {
          Node* neg = new Node(ND_NEG);
          neg->expr = unary()
          return neg;
      }
      //...
      return num();
  }
  ```

  注意，`unary()`的解析是递归的，参照生成式：
  
  ```c++
  expression
      : unary
  
  unary
      : Integer
      | ('-'|'!'|'~') unary
  ```
  
  