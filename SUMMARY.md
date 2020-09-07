# minidecaf教学实验文档
* [实验简介](README.md)
* [更新日志](docs/log.md)

## 零：前置准备
* 配环境、跑测试
  * [环境配置](docs/lab0/env.md)
  * [运行测试样例](docs/lab0/testing.md)
  * [RISC-V 的工具链使用](docs/lab0/riscv.md)

## 第一个编译器
* step1：仅一个 return 的 main 函数
  * [从零开始的 lexer、parser 以及汇编生成](docs/lab1/part1.md)
  * [词法语法分析工具](docs/lab1/part2.md)
  * [使用中间码](docs/lab1/part3.md)
  * 其他
    * [ANTLR 使用](docs/lab1/antlr.md)
    * [Visitor 模式](docs/lab1/visitor.md)
    * [IR 简明介绍](docs/lab1/ir.md)
  * [规范](docs/lab1/spec.md)

## 常量表达式
* step2：一元操作
  * [任务概述](docs/lab2/intro.md)
  * [实验指导](docs/lab2/guide.md)
  * [规范](docs/lab2/spec.md)

* step3：加减乘除模
  * [任务概述](docs/lab3/intro.md)
  * [实验指导](docs/lab3/guide.md)
  * [规范](docs/lab3/spec.md)

* step4：比较和逻辑表达式
  * [任务概述](docs/lab4/intro.md)
  * [实验指导](docs/lab4/guide.md)
  * [规范](docs/lab4/spec.md)

## 变量和语句
* step5：局部变量和赋值
  * [任务概述](docs/lab5/intro.md)
  * [实验指导](docs/lab5/guide.md)
  * 其他
    * [栈帧](docs/lab5/stackframe.md)
  * [规范](docs/lab5/spec.md)

* step6：if 语句和条件表达式
  * [任务概述](docs/lab6/intro.md)
  * [实验指导](docs/lab6/guide.md)
  * [规范](docs/lab6/spec.md)

## 块语句和作用域和更多语句
* step7：作用域和块语句
  * [任务概述](docs/lab7/intro.md)
  * [实验指导](docs/lab7/guide.md)
  * [规范](docs/lab7/spec.md)

* step8：循环语句
  * [摘要](docs/lab8/part0-intro.md)
  * [词法语法分析](docs/lab8/part1-parse.md)
  * [任务](docs/lab8/part1-1-task.md)
  * [代码生成](docs/lab8/part4-codegen.md)
  * [任务](docs/lab8/part4-1-task.md)
  * [小结](docs/lab8/summary.md)
  * [规范](docs/lab8/spec.md)

## 函数和全局变量
* step9：函数
  * [摘要](docs/lab9/part0-intro.md)
  * [词法语法分析](docs/lab9/part1-parser.md)
  * [任务](docs/lab9/part1-1-task.md)
  * [调用约定](docs/lab9/part4-1-cconv.md)
  * [代码生成](docs/lab9/part4-2-codegen.md)
  * [任务](docs/lab9/part4-3-task.md)
  * [小结](docs/lab9/summary.md)
  * [规范](docs/lab9/spec.md)

* step10：全局变量
  * [摘要](docs/lab10/part0-intro.md)
  * [词法语法分析](docs/lab10/part1-parser.md)
  * [任务](docs/lab10/part1-1-task.md)
  * [代码生成](docs/lab10/part4-codegen.md)
  * [任务](docs/lab10/part4-1-task.md)
  * [小结](docs/lab10/summary.md)
  * [规范](docs/lab10/spec.md)

## 指针和数组
* step11：指针
  * [摘要](docs/lab11/part0-intro.md)
  * [类型检查](docs/lab11/typeck.md)
  * [代码生成](docs/lab11/part4-codegen.md)
  * [任务](docs/lab11/part4-1-task.md)
  * [小结](docs/lab11/summary.md)
  * [规范](docs/lab11/spec.md)

* step12：数组
  * [摘要](docs/lab12/part0-intro.md)
  * [代码生成](docs/lab12/part4-codegen.md)
  * [任务](docs/lab12/part4-1-task.md)
  * [小结](docs/lab12/summary.md)
  * [规范](docs/lab12/spec.md)

## 参考资料
* [参考资料](REFERENCE.md)
