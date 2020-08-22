## Lab 1: Integers

(refer to dzy)

1. minilexer 是如何使得 int 被分析成一个关键字而非一个标识符的？
2. 修改 minilexer 的输入（lexer.setInput 的参数），使得 lex 报错，给出一个简短的例子。
miniparser 的算法，只有当语法满足什么条件时才能使用？
3. 修改 minilexer 的输入，使得 lex 不报错但 parser 报错，给出一个简短的例子。
4. 一种暴力算法是，只做 lex，然后在 token 流里面寻找连续的 Return，Integer 和 Semicolon，找到以后取得 Integer 的常量 a，然后类似上面目标代码生成。这个暴力算法有什么问题？
5. 除了我们的暴力 miniparser，形式语言与自动机课中也描述了一种算法，可以用来计算语法分析树。请问它是什么算法，时间复杂度是多少？

## Lab 2: Unary Operators

请将下述 MiniDecaf 代码的 `???` 换成若干个单目运算符，使得代码运行的返回结果为2。

```c++
int main() {
    return ???0;
}
```

```c++
int main() {
    return -~!0;
}
```

## Lab 3: Binary Operators & Parenthesis for ( expr )

1. 当你想把寄存器 t0 中的数值存储到栈中，应该使用什么指令？
```asm
addi sp,sp,-4
sd t0, 0(sp)
```
2. 当你想把栈顶的数值弹出并存储到寄存器 t0 中，应该使用什么指令？
```asm
ld t0, 0(sp)
addi sp, sp, 4
```
3. 如果我们把
```
<exp> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/" | "%") <factor> }
```
改成
```
<exp> ::= <factor> "+" <factor> | <factor> "-" <factor> | <factor> "*" <factor> | <factor> "/" <factor> | <factor> "%" <factor>
```
会发生什么？

## Lab 4: Logical Binary Operators

在 MiniDecaf 中，我们对于短路求值未做要求，但在包括 C 语言的大多数流行的语言中，短路求值都是被支持的。为何这一特性广受欢迎？你认为短路求值这一特性会给程序员带来怎样的好处？

## Lab 5: Local Variables

1. 当`main`函数中一次存在两个整数变量定义a、b时，函数结束前，栈顶的四个元素一次是什么：
    b a ra s0/fp
2. 当main函数中存在两个整数变量定义时，`main` 函数的汇编代码的第一行代码是：
```asm
addi sp, sp, -32
```

## Lab 6: Conditional statements & expressions

是否可以把语法规范中的
```
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <conditional-exp> ]
```
改成
```
<conditional-exp> ::= <logical-or-exp> [ "?" <exp> ":" <exp> ]
```
？请给你的判断和理由。

## Lab 7: Compound statements & definition scopes

请将下述 MiniDecaf 代码中的 `???` 替换为一个 32 位整数，使得程序运行结束后会返回 0。
```c++
int main() {
    int x = ???;
    if (x) {
        return x;
    } else {
        int x = 2;
    }
    return x;
}
```

## Lab 8: Loops

请分别使用 for 循环和 do-while 循环写出与下述代码在语义上等价的 MiniDecaf 代码
```c++
int s = 0;
int i = 1;
while (i <= n) {
    s += i;
    i += 1;
}
```

```c++
// for loop
int s = 0;
for (int i = 1; i <= n; i += 1) s += i;

// do-while loop
int i = 1;
do {
    s += i;
    i += 1;
} while (i <= n)
```

## Lab 9: Functions

在 C 中对于函数调用的参数求值的顺序是并未被规定的，试写出一段 MiniDecaf 代码，使得不同的参数求值顺序会导致不同的返回结果。

```c++
int fun(int x, int y) {
    return x + y;
}
int main() {
    int x = 1;
    return fun(x + 1, x = 2);
}
```

TODO: 应该也可以考察一下 calling convention

## Lab 10: Global Variables

1. 在 C 中，全局变量只能被常量表达式或字符串文字初始化（C99 Standard 6.7.8），它为何这么设计？
2. Java 并不直接支持全局变量这一特性，如何在 Java 中实现类似于 C 的“全局变量”？

## Lab 11: Pointer

## Lab 12: Array

