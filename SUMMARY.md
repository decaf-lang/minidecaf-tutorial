* [实验简介](README.md)
* [实验进度安排](docs/misc/schedule.md)
* [勘误表](docs/step0/errate.md)
* [RISC-V 参考资料](docs/ref/riscv.md)

## 前置准备

* 配环境、跑测试
  * [实验环境简介](docs/step0/intro.md)
  * [RISC-V 环境配置](docs/step0/riscv_env.md)
  * [RISC-V 的工具链使用](docs/step0/riscv.md)
  * [实验框架环境配置](docs/step0/env.md)
  * [运行实验框架](docs/step0/testing.md)

## Stage0：第一个编译器

* [MiniDecaf 编译器结构](docs/step1/arch.md)
* [已提供的语法特性](docs/step1/provided.md)

* step1：仅一个 return 的 main 函数
  * [实验要求](docs/step1/intro.md)
  * [通过例子学习](docs/step1/example.md)
  * [Visitor 模式速成](docs/step1/visitor.md)
  * [规范](docs/step1/spec.md)

## Stage1：常量表达式

* step2：一元操作
  * [实验要求](docs/step2/intro.md)
  * [通过例子学习](docs/step2/example.md)
  * [规范](docs/step2/spec.md)

* step3：加减乘除模
  * [实验要求](docs/step3/intro.md)
  * [通过例子学习](docs/step3/example.md)
  * [优先级和结合性](docs/step3/precedence.md)
  * [规范](docs/step3/spec.md)

* step4：比较和逻辑表达式
  * [实验要求](docs/step4/intro.md)
  * [通过例子学习](docs/step4/example.md)
  * [规范](docs/step4/spec.md)

## Stage2：变量

* step5：局部变量和赋值
  * [实验要求](docs/step5/intro.md)
  * [通过例子学习](docs/step5/example.md)
  * [规范](docs/step5/spec.md)

## Stage3：作用域

* step6：作用域和块语句
  * [实验要求](docs/step6/intro.md)
  * [通过例子学习](docs/step6/example.md)
  * [数据流分析](docs/step6/dataflow.md)
  * [规范](docs/step6/spec.md)

## Stage4：条件和循环

* step7：条件语句
  * [实验要求](docs/step7/intro.md)
  * [通过例子学习](docs/step7/example.md)
  * [规范](docs/step7/spec.md)

* step8：循环语句
  * [实验要求](docs/step8/intro.md)
  * [通过例子学习](docs/step8/example.md)
  * [规范](docs/step8/spec.md)

## Stage5：函数

* step9：函数
  * [实验要求](docs/step9/intro.md)
  * [通过例子学习](docs/step9/example.md)
  * [规范](docs/step9/spec.md)

## Stage6（升级）：全局变量和数组

* step10：全局变量
  * [实验要求](docs/step10/intro.md)
  * [通过例子学习](docs/step10/example.md)
  * [规范](docs/step10/spec.md)

* step11：数组
  * [实验要求](docs/step11/intro.md)
  * [通过例子学习](docs/step11/example.md)
  * [规范](docs/step11/spec.md)

* step12：为数组添加更多支持
  * [实验要求](docs/step12/intro.md)
  * [通过例子学习](docs/step12/example.md)
  * [规范](docs/step12/spec.md)

## Stage7（升级）：寄存器分配与代码优化

* [选做二说明](docs/step13/readme.md)

* step13：寄存器分配算法改进
  * [实验要求](docs/step13/intro.md)
  * [实验指导](docs/step13/example.md)

## 大实验参考文档（编写中）

* [大实验简介](docs/contest/intro.md)
* [前端设计](docs/contest/frontend.md)
* [中端设计](docs/contest/midend/midend.md)
  * [中间表示设计](docs/contest/midend/ir.md)
  * [静态单赋值](docs/contest/midend/ssa.md)
  * [常量传播](docs/contest/midend/cp.md)
  * [死代码消除](docs/contest/midend/dce.md)
* [后端设计](docs/contest/backend.md)

## 参考资料

* [参考资料](REFERENCE.md)
