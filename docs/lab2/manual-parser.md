## 手写 parser 简单实例

* 节点定义变化

    增加三种表达式节点，分别为：按位取反、取负、逻辑取反

    ```c++
    struct NodeKind {
    +    ND_NEG,
    +    ND_NOT,
    +    ND_BITNOT,
    }
    ```

    这一变化很简单，以后省略。

* parse 过程变化

  按照产生式变化对应修改即可，很简单。

  ```c++
  expression
      : unary
  
  unary
      : Integer
      | ('-'|'!'|'~') unary
  ```
  
  ```c++
  Node* expr() {
  	return unary();
  }
  
  Node* unary() {
    if(parse_reserved("-")) {
          Node* neg = new Node(ND_NEG);
          neg->expr = unary();
          return neg;
      }
      //...　`!``~`同理
      return num();
  }
  ```
  
  注意，`unary()`的解析是递归的，这与产生式是一致的。
  
  