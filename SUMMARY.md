# MiniDecaf 教学实验文档
* [实验简介](README.md)
* [待完善](step0/todo.md)

## 零：前置准备
* 配环境、跑测试
  * [RISC-V环境配置](docs/step0/riscv_env.md)
  * [RISC-V 的工具链使用](docs/step0/riscv.md)
  * [实验框架环境配置](docs/step0/env.md)
  * [运行实验框架](docs/step0/testing.md)
  * [常见问题](docs/step0/faq.md)


## 第一个编译器
* step1：仅一个 return 的 main 函数
  * [从零开始的 lexer、parser 以及汇编生成](docs/step1/part1.md)
  * [词法语法分析工具](docs/step1/part2.md)
  * [使用中间码](docs/step1/part3.md)
  * 其他
    * [ANTLR 使用](docs/step1/antlr.md)
    * [Visitor 模式](docs/step1/visitor.md)
    * [IR 简明介绍](docs/step1/ir.md)
    * [手写简单 parser](docs/step1/manual-parser.md)
  * [规范](docs/step1/spec.md)

## 常量表达式
* step2：一元操作
  * [任务概述](docs/step2/intro.md)
  * [实验指导](docs/step2/guide.md)
  * 其他
    * [手写简单 parser](docs/step2/manual-parser.md)
  * [规范](docs/step2/spec.md)

* step3：加减乘除模
  * [任务概述](docs/step3/intro.md)
  * [实验指导](docs/step3/guide.md)
  * 其他
    * [优先级和结合性](docs/step3/precedence.md)
    * [手写简单 parser](docs/step3/manual-parser.md)
  * [规范](docs/step3/spec.md)

* step4：比较和逻辑表达式
  * [任务概述](docs/step4/intro.md)
  * [实验指导](docs/step4/guide.md)
  * [规范](docs/step4/spec.md)

## 变量和语句
* step5：局部变量和赋值
  * [任务概述](docs/step5/intro.md)
  * [实验指导](docs/step5/guide.md)
  * 其他
    * [栈帧](docs/step5/stackframe.md)
    * [手写简单 parser](docs/step5/manual-parser.md)
  * [规范](docs/step5/spec.md)

* step6：if 语句和条件表达式
  * [任务概述](docs/step6/intro.md)
  * [实验指导](docs/step6/guide.md)
  * 其他
    * [手写简单 parser](docs/step6/manual-parser.md)
  * [规范](docs/step6/spec.md)

## 块语句和作用域和更多语句
* step7：作用域和块语句
  * [任务概述](docs/step7/intro.md)
  * [实验指导](docs/step7/guide.md)
  * 其他
    * [手写简单 parser](docs/step7/manual-parser.md)
  * [规范](docs/step7/spec.md)

* step8：循环语句
  * [任务概述](docs/step8/intro.md)
  * [实验指导](docs/step8/guide.md)
  * [规范](docs/step8/spec.md)

## 函数和全局变量
* step9：函数
  * [任务概述](docs/step9/intro.md)
  * [实验指导](docs/step9/guide.md)
  * 其他
    * [函数调用](docs/step9/calling.md)
    * [手写简单 parser](docs/step9/manual-parser.md)
  * [规范](docs/step9/spec.md)

* step10：全局变量
  * [任务概述](docs/step10/intro.md)
  * [实验指导](docs/step10/guide.md)
  * 其他
    * [手写简单 parser](docs/step10/manual-parser.md)
  * [规范](docs/step10/spec.md)

## 数组和指针
* step11：数组
  * [任务概述](docs/step11/intro.md)
  * [实验指导](docs/step11/guide.md)
  * 其他
    * [手写简单 parser](docs/step11/manual-parser.md)
  * [规范](docs/step11/spec.md)

* step12：指针
  * [任务概述](docs/step12/intro.md)
  * [实验指导](docs/step12/guide.md)
  * 其他
    * [左值](docs/step12/lvalue.md)
    * [类型检查](docs/step12/typeck.md)
    * [手写简单 parser](docs/step12/manual-parser.md)
  * [规范](docs/step12/spec.md)

## 参考资料
* [参考资料](REFERENCE.md)
