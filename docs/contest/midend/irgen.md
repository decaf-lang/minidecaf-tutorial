# 中间代码生成

## 介绍
前端解析后，我们会得到一棵抽象语法树，接下来我们需要将这棵抽象语法树转换为中间代码。依据你设计的IR，你需要在保证语义的情况下，将AST用你的IR表示出来。可以参考基础实验框架中`frontend/tacgen/`的代码。**推荐在生成中间代码时就先利用 Alloca、Load、Store 指令来简单地实现 SSA 形式的中间代码，方便之后用`mem2reg`进一步优化**（你可以先阅读[静态单赋值](./ssa.md)简单了解什么是SSA）。

## 部分处理思路
整体思路是通过遍历AST的节点，根据节点类型进行相应的处理。推荐先根据AST的遍历顺序写一个框架，再填充具体的处理逻辑。

由于每个组的AST和IR设计不尽相同，本部分仅介绍一些重点的处理思路和具体示例，结合小实验文档食用效果更佳。

注意：
- **本部分仅供参考，你需要根据自己设计的AST和IR进行调整。**
- 在遍历AST的过程中，**要记得维护一些数据**，比如当前所在函数、当前所在基本块、函数的寄存器数量、函数的基本块数量、前端变量到IR的`Data`对象的映射表等。

### program
对于`program`节点，先新建一个IR的`Program`对象，然后我们只需要再遍历子节点。
- 如果子节点是`function`，就新建一个IR的`Function`对象，再访问该`function`节点，从而将该函数的前端信息存入`Function`对象中，最后将其加入到当前`Program`对象中的`functions`列表。
- 如果子节点是`declaration`，说明这是一个全局变量，就新建一个`Data`对象，再访问该`declaration`节点，从而将该全局变量的前端信息存入`Data`对象中，最后将其加入到当前`Program`对象中的`global_data`列表。

### parameter_list
对于`parameter_list`节点，可以把前几个寄存器编号分配给参数。
- 如果是标量参数，要另外在栈上开空间。（这是为了满足 SSA 形式）
- 如果是数组参数，则可以直接保存在寄存器中。

### declaration
对于`declaration`节点，需要根据是否为全局变量、是否为数组来进行处理。**为了满足 SSA 形式，哪怕是局部标量，也要用`Alloca`指令得到一个地址，后续就通过这个地址来对该变量进行读写操作**。

如果有初始化，
- 对于标量，需要访问`expression`节点并获取其**运算结果**对应的寄存器，然后新增`Store`指令，表示将得到的寄存器的值存入该标量对应的地址。
- 对于数组则需要遍历`Integer`节点，并分别使用`Store`指令将数组元素存入数组的相应地址，对于全局变量可以考虑是否加入`.bss`段。

### lvalue
`lvalue`节点表示的是左值，可能出现的地方为：`assignment`的等号左边部分、`expression`的某个部分，如果是后者且该节点表示的是一个具体值，则返回**存有该值**的寄存器，否则返回其**对应地址**的寄存器。（下面会对“表示的是一个具体值”进行解释）
- 先通过前端变量到IR的`Data`对象的映射表，找到该节点所表示的前端变量对应的`Data`对象。
  - 如果这是个全局变量，则新增`LoadAddr`指令，表示加载全局变量的地址，获取**对应地址**的寄存器
  - 如果这是个局部变量，则直接通过`Data`对象获取**对应地址**的寄存器
- 如果这是个数组，那么前端节点应该会记录下标，每个下标都是`expression`节点，故需要访问每个下标节点，获取其**运算结果**对应的寄存器，可以将这些寄存器存起来，比如存进`index_temps`中，之后再利用这些信息来构造相应的`GetElementPtr`指令，表示通过数组基地址和下标获取元素的**地址**。
- 目前不管是全局变量还是局部变量，不管是标量还是数组，我们得到的都是存有其**对应地址**的寄存器，需要根据具体情况确定返回内容。
  - 如果该`lvalue`节点是`expression`的某个部分，且表示的是一个具体值，则先新增`Load`指令，表示将地址里的值加载到一个寄存器中，最后返回这个寄存器；否则，就直接返回其**对应地址**的寄存器。
  - 什么是“表示的是一个具体值”？举个例子，如果已知有一个数组`a[2][3]`，那么如果该`lvalue`节点表示的是`a[1][2]`，则表示的是一个具体值，如果表示的是`a`、`a[0]`，则不是一个具体值而是一个地址。

### 中场休息
看了前面的内容感觉很抽象怎么办？没关系，我们不急着往后学，先休息一下，看一个具体的用到`parameter_list`, `declaration`, `lvalue`节点的例子，希望能帮到你。
```c
int a = 1;
int foo(int x, int y[]) {
    return x + y[1];
}
int main() {
    int b[2][3] = {1, 2, 3, 4, 5, 6};
    return foo(a, b[1]);
}
```
生成的AST可能如下：
```
```
上述代码转化为IR后可能如下：
```asm
i32 foo(i32 _T0, i32* _T1) {
_B0:
  alloca i32* _T2 = 4
  store *(i32* _T2 + 0) = i32 _T0
  load i32 _T3 = *(i32* _T2 + 0)
  i32 _T4 = 1
  i32* _T5 = elementptr: i32* _T1[i32 _T4]
  load i32 _T6 = *(i32* _T5 + 0)
  i32 _T7 = i32 _T3 + i32 _T6
  return i32 _T7
}
i32 main() {
_B0:
  alloca i32[3]* _T0 = 24
  i32 _T1 = 1
  store *(i32[3]* _T0 + 0) = i32 _T1
  i32 _T2 = 2
  store *(i32[3]* _T0 + 4) = i32 _T2
  i32 _T3 = 3
  store *(i32[3]* _T0 + 8) = i32 _T3
  i32 _T4 = 4
  store *(i32[3]* _T0 + 12) = i32 _T4
  i32 _T5 = 5
  store *(i32[3]* _T0 + 16) = i32 _T5
  i32 _T6 = 6
  store *(i32[3]* _T0 + 20) = i32 _T6
  i32* _T7 = LoadAddr $a
  load i32 _T8 = *(i32* _T7 + 0)
  i32 _T9 = 1
  i32* _T10 = elementptr: i32[3]* _T0[i32 _T9]
  i32 _T11 = call foo(i32 _T8, i32* _T10)
  return i32 _T11
}
```
在本例中，
- `foo`函数的参数表示为`_T0`, `_T1`。为了满足 SSA 形式，使用标量`x`时，需要另外在栈上开空间，这样之后对`x`的读写操作都可以直接通过`_T2`来进行。对于`y[1]`，利用下标和`getElementptr`指令可以得到其地址，然后通过`load`指令可以得到其值。（`getElementptr`指令是为了写起来方便快捷；这里你也可以通过基地址`_T1`和下标`1`，构造出`_T1 + 1 * 4`的式子来计算出`y[1]`的地址）
- `main`函数中对于数组`b`，先使用`Alloca`指令获取其栈上地址，再将初始值存到各个元素的地址中。由于`a`是`foo`函数的实参，所以这是一个`lvalue`节点，同时我们知道这是一个具体值，所以在`LoadAddr`指令获取`a`的地址之后，还要用`Load`指令将其值加载到一个寄存器中。`b[1]`在这里虽然也是一个`lvalue`节点，但是由于它不是一个具体值，所以我们直接使用其**对应地址**的寄存器。

### expression
访问`expression`节点之后需要返回存有其**运算结果**的寄存器，方便后续使用。以下分两种情况进行处理：
- `unary '=' expression`，表示赋值表达式。
  - 对于等号左边，访问该`lvalue`节点并获取其**对应地址**的寄存器。
  - 对于等号右边，访问该`expression`节点并获取其**运算结果**对应的寄存器。
  - 最后新增`Store`指令，表示将右边的寄存器里的值存入左边的寄存器里的地址，并返回左边的寄存器。
- `conditional`，表示条件表达式。
  - 如果这是个三目运算符，可参考`if`节点的处理方式，区别在于，对于`:?`运算符，`then` 和 `else` 是两个表达式节点，对于`if`语句，这两个变量是两个语句节点。
  - 如果这是个`logical_or`节点，则直接访问`logical_or`节点，由于可能出现逻辑短路的情况，所以你需要思考如何新增`Branch`指令来进行分支跳转，可以参考[短路求值](short_circuit.md)。
- 具体示例可以参考[短路求值](short_circuit.md)。

### if
- 先给当前函数新增一个基本块`true_bb`表示`if`语句的`true`分支入口。
- 如果有`else`部分，则给当前函数新增一个基本块`false_bb`表示`if`语句的`false`分支入口。
- 给当前函数新增一个基本块`next_bb`表示`if`之后的基本块。
- 分支条件是一个`expression`节点，访问该`expression`节点并获取其**运算结果**对应的寄存器。
  - 由于`expression`节点可能出现逻辑短路的情况，所以你需要思考如何新增`Branch`指令来进行分支跳转，可以参考[短路求值](short_circuit.md)。
- 将当前基本块改为`true_bb`，然后访问`true`分支的前端节点，再新增一个`Jump`指令，表示从`true_bb`跳转到`next_bb`。
- 如果有`else`部分，则将当前基本块改为`false_bb`，然后访问`false`分支的前端节点，再新增一个`Jump`指令，表示从`false_bb`跳转到`next_bb`。
- 最后将当前基本块改为`next_bb`。
- 例：
    ```C
    int main(){
        int a = 2;
        int b = 0;
        if(a)
            b = 1;
        else
            b = -1;
        return b;
    }
    ```
    生成的AST可能如下：
    ```
    Program
        |- (children[0]) Function
            |- (ret_t) TInt
            |- (ident) Identifier("main")
            |- (body) Block
                |- (children[0]) VarDecl
                    |- (type) TInt
                    |- (ident) Identifier("a")
                    |- (init) IntLiteral(2)
                |- (children[1]) VarDecl
                    |- (type) TInt
                    |- (ident) Identifier("b")
                    |- (init) IntLiteral(0)
                |- (children[2]) If
                    |- (cond) Identifier("a")
                    |- (children[0]) Assign
                        |- (lhs) Identifier("b")
                        |- (rhs) IntLiteral(1)
                    |- (children[1]) Assign
                        |- (lhs) Identifier("b")
                        |- (rhs) UnaryOp(NEG)
                            |- (expr) IntLiteral(1)
                |- (children[3]) Return
                    |- (expr) Identifier("b")
    ```

    上述代码转化为IR后可能如下：

    ```asm
    i32 main() {
    _B0:
        alloca i32* _T0 = 4
        i32 _T1 = 2
        store *(i32* _T0 + 0) = i32 _T1
        alloca i32* _T2 = 4
        i32 _T3 = 0
        store *(i32* _T2 + 0) = i32 _T3
        load i32 _T4 = *(i32* _T0 + 0)
        if i32 _T4 == 0 jump _B2 else jump _B1
    _B1:
        i32 _T5 = 1
        store *(i32* _T2 + 0) = i32 _T5
        jump _B3
    _B2:
        i32 _T6 = 1
        i32 _T7 = -i32 _T6
        store *(i32* _T2 + 0) = i32 _T7
        jump _B3
    _B3:
        load i32 _T8 = *(i32* _T2 + 0)
        return i32 _T8
    }
    ``` 
    在本例中，生成了`_B1`, `_B2`, `_B3`三个基本块，分别表示`true`分支入口、`false`分支入口和`if`之后的基本块。`_B0`的结尾是一个`Branch`指令，`_B1`, `_B2`结尾都是`Jump`指令，表示从`true_bb`、`false_bb`跳转到`next_bb`。

### while
这里的翻译方式采用的是[step8的思考题](../../step8/example.md)中的第二种。**在翻译过程中，你还要维护好循环所需的`break/continue`标签。**
- 给当前函数新增一个基本块`body_bb`表示`while`语句的循环体入口。
- 给当前函数新增一个基本块`body_cond_bb`表示第二个`while`语句的条件部分。
- 给当前函数新增一个基本块`next_bb`表示`while`之后的基本块。
- 开始访问第一个`while`语句的条件部分，分支条件是一个`expression`节点，可以直接访问该`expression`节点。
  - 由于`expression`节点可能出现逻辑短路的情况，所以你需要思考如何新增`Branch`指令来进行分支跳转，可以参考[短路求值](short_circuit.md)进行学习。
- 将当前基本块改为`body_bb`，然后访问`true`分支的前端节点，再新增一个`Jump`指令，表示从`body_bb`跳转到`body_cond_bb`。
- 将当前基本块改为`body_cond_bb`，第二个`while`语句的条件部分是一个`expression`节点，访问该`expression`节点并获取其**运算结果**对应的寄存器。
  - 由于`expression`节点可能出现逻辑短路的情况，所以你需要思考如何新增`Branch`指令来进行分支跳转，可以参考[短路求值](short_circuit.md)进行学习。
- 最后将当前基本块改为`next_bb`。
- 例：
    ```C
    int main(){
        int a = 0;
        while(a < 10){
            if(a == 5){
                a = 10;
                break;
            }
            a = a + 1;
        }
        return a;
    }
    ```
    生成的AST可能如下：
    ```
    ```
    上述代码转化为IR后可能如下：
    ```asm
    i32 main() {
    _B0:
        alloca i32* _T0 = 4
        i32 _T1 = 0
        store *(i32* _T0 + 0) = i32 _T1
        load i32 _T2 = *(i32* _T0 + 0)
        i32 _T3 = 10
        i32 _T4 = i32 _T2 < i32 _T3
        if i32 _T4 == 0 jump _B3 else jump _B1
    _B1:
        load i32 _T5 = *(i32* _T0 + 0)
        i32 _T6 = 5
        i32 _T7 = i32 _T5 == i32 _T6
        if i32 _T7 == 0 jump _B5 else jump _B4
    _B2:
        load i32 _T12 = *(i32* _T0 + 0)
        i32 _T13 = 10
        i32 _T14 = i32 _T12 < i32 _T13
        if i32 _T14 == 0 jump _B3 else jump _B1
    _B3:
        load i32 _T15 = *(i32* _T0 + 0)
        return i32 _T15
    _B4:
        i32 _T8 = 10
        store *(i32* _T0 + 0) = i32 _T8
        jump _B3
    _B5:
        load i32 _T9 = *(i32* _T0 + 0)
        i32 _T10 = 1
        i32 _T11 = i32 _T9 + i32 _T10
        store *(i32* _T0 + 0) = i32 _T11
        jump _B2
    _B6:
        jump _B5
    }
    ``` 
    在本例中，`_B0`的最后是第一个`while`语句的条件部分，`while`语句还生成了`_B1`, `_B2`, `_B3`三个基本块，分别表示`while`语句的循环体入口、第二个`while`语句的条件部分和`while`之后的基本块。`if`语句生成了`_B4`, `_B5`两个基本块。多出来的`_B6`是个不可达基本块，可以在之后生成目标代码时消掉。（思考一下，为什么要生成`_B6`？提示：如果`break;`语句后面加上`a = 1;`语句，IR会如何改变？）

## 预期目标

完成这部分内容后，你的编译器应该能将 MiniDecaf 程序翻译成满足 SSA 形式的 IR，并能够输出 IR。进一步地，如果你希望参加性能评测，你还需要实现一些中端优化。

