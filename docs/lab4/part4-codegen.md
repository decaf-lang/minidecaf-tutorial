## 代码生成

### 基础

对于`>`,`<`，可以用如下指令实现：

```asm
slt t0, t1, t2          #set less than; t0 = (t1 < t2) ? 1 : 0;
sgt t0, t1, t2          #set greater than; t0 = (t1 > t2) ? 1 : 0;
```

`>=`,`<=`，可以通过 `<`，`>` 与 `-` 组合得到。

`==`，`！=`，可以先进行减法操作，将结果与0比较。

t0 = (t1 == t2) :
```asm
sub t0, t1, t2
seqz t0, t0
```

t0 = (t1 != t2) :
```asm
sub t0, t1, t2
snez t0, t0             #set not equal to zero
```

`&&`,`||` 是逻辑运算，比较复杂，没有直接指令，生成方式合理即可

t0 = (t1 || t2) : 
```asm
or t0, t1, t2
snqz t0, t0
```

t0 = (t1 && t2) :

```asm
snez t1, t1
snez t2, t2
and t0, t1, t2
```

### 生成

与 lab3 无区别（对于逻辑运算，可以有不同的生成方式，见思考题）。