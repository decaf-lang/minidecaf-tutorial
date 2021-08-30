# Table of contents

* [实验简介](README.md)

## 零：前置准备

* [配环境、跑测试](ling-qian-zhi-zhun-bei/pei-huan-jing-pao-ce-shi/README.md)
  * [环境配置](ling-qian-zhi-zhun-bei/pei-huan-jing-pao-ce-shi/env.md)
  * [运行测试样例](ling-qian-zhi-zhun-bei/pei-huan-jing-pao-ce-shi/testing.md)
  * [RISC-V 的工具链使用](ling-qian-zhi-zhun-bei/pei-huan-jing-pao-ce-shi/riscv.md)
  * [常见问题](ling-qian-zhi-zhun-bei/pei-huan-jing-pao-ce-shi/faq.md)
* [参考实现](ling-qian-zhi-zhun-bei/can-kao-shi-xian/README.md)
  * [说明](ling-qian-zhi-zhun-bei/can-kao-shi-xian/intro.md)
  * [TypeScript-ANTLR](ling-qian-zhi-zhun-bei/can-kao-shi-xian/typescript-jyk.md)
  * [Python-ANTLR](ling-qian-zhi-zhun-bei/can-kao-shi-xian/python-dzy.md)
  * [Java-ANTLR](ling-qian-zhi-zhun-bei/can-kao-shi-xian/java-xxy.md)

## 第一个编译器

* [step1：仅一个 return 的 main 函数](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/README.md)
  * [从零开始的 lexer、parser 以及汇编生成](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/part1.md)
  * [词法语法分析工具](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/part2.md)
  * [使用中间码](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/part3.md)
  * [其他](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/qi-ta/README.md)
    * [ANTLR 使用](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/qi-ta/antlr.md)
    * [Visitor 模式](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/qi-ta/visitor.md)
    * [IR 简明介绍](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/qi-ta/ir.md)
    * [手写简单 parser](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/qi-ta/manual-parser.md)
  * [规范](di-yi-ge-bian-yi-qi/step1-jin-yi-ge-return-de-main-han-shu/spec.md)

## 常量表达式

* [step2：一元操作](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/README.md)
  * [任务概述](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/intro.md)
  * [实验指导](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/guide.md)
  * [其他](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/qi-ta/README.md)
    * [手写简单 parser](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/qi-ta/manual-parser.md)
  * [规范](chang-liang-biao-da-shi/step2-yi-yuan-cao-zuo/spec.md)
* [step3：加减乘除模](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/README.md)
  * [任务概述](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/intro.md)
  * [实验指导](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/guide.md)
  * [其他](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/qi-ta/README.md)
    * [优先级和结合性](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/qi-ta/precedence.md)
    * [手写简单 parser](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/qi-ta/manual-parser.md)
  * [规范](chang-liang-biao-da-shi/step3-jia-jian-cheng-chu-mo/spec.md)
* [step4：比较和逻辑表达式](chang-liang-biao-da-shi/step4-bi-jiao-he-luo-ji-biao-da-shi/README.md)
  * [任务概述](chang-liang-biao-da-shi/step4-bi-jiao-he-luo-ji-biao-da-shi/intro.md)
  * [实验指导](chang-liang-biao-da-shi/step4-bi-jiao-he-luo-ji-biao-da-shi/guide.md)
  * [规范](chang-liang-biao-da-shi/step4-bi-jiao-he-luo-ji-biao-da-shi/spec.md)

## 变量和语句

* [step5：局部变量和赋值](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/README.md)
  * [任务概述](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/intro.md)
  * [实验指导](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/guide.md)
  * [其他](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/qi-ta/README.md)
    * [栈帧](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/qi-ta/stackframe.md)
    * [手写简单 parser](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/qi-ta/manual-parser.md)
  * [规范](bian-liang-he-yu-ju/step5-ju-bu-bian-liang-he-fu-zhi/spec.md)
* [step6：if 语句和条件表达式](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/README.md)
  * [任务概述](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/intro.md)
  * [实验指导](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/guide.md)
  * [其他](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/qi-ta/README.md)
    * [手写简单 parser](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/qi-ta/manual-parser.md)
  * [规范](bian-liang-he-yu-ju/step6if-yu-ju-he-tiao-jian-biao-da-shi/spec.md)

## 块语句和循环语句

* [step7：作用域和块语句](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/README.md)
  * [任务概述](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/intro.md)
  * [实验指导](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/guide.md)
  * [其他](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/qi-ta/README.md)
    * [手写简单 parser](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/qi-ta/manual-parser.md)
  * [规范](kuai-yu-ju-he-xun-huan-yu-ju/step7-zuo-yong-yu-he-kuai-yu-ju/spec.md)
* [step8：循环语句](kuai-yu-ju-he-xun-huan-yu-ju/step8-xun-huan-yu-ju/README.md)
  * [任务概述](kuai-yu-ju-he-xun-huan-yu-ju/step8-xun-huan-yu-ju/intro.md)
  * [实验指导](kuai-yu-ju-he-xun-huan-yu-ju/step8-xun-huan-yu-ju/guide.md)
  * [规范](kuai-yu-ju-he-xun-huan-yu-ju/step8-xun-huan-yu-ju/spec.md)

## 函数和全局变量

* [step9：函数](han-shu-he-quan-ju-bian-liang/step9-han-shu/README.md)
  * [任务概述](han-shu-he-quan-ju-bian-liang/step9-han-shu/intro.md)
  * [实验指导](han-shu-he-quan-ju-bian-liang/step9-han-shu/guide.md)
  * [其他](han-shu-he-quan-ju-bian-liang/step9-han-shu/qi-ta/README.md)
    * [函数调用](han-shu-he-quan-ju-bian-liang/step9-han-shu/qi-ta/calling.md)
    * [手写简单 parser](han-shu-he-quan-ju-bian-liang/step9-han-shu/qi-ta/manual-parser.md)
  * [规范](han-shu-he-quan-ju-bian-liang/step9-han-shu/spec.md)
* [step10：全局变量](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/README.md)
  * [任务概述](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/intro.md)
  * [实验指导](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/guide.md)
  * [其他](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/qi-ta/README.md)
    * [手写简单 parser](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/qi-ta/manual-parser.md)
  * [规范](han-shu-he-quan-ju-bian-liang/step10-quan-ju-bian-liang/spec.md)

## 扩展：数组

* [step11：数组](kuo-zhan-shu-zu/step11-shu-zu/README.md)
  * [任务概述](kuo-zhan-shu-zu/step11-shu-zu/intro.md)
  * [实验指导](kuo-zhan-shu-zu/step11-shu-zu/guide.md)
  * [其他](kuo-zhan-shu-zu/step11-shu-zu/qi-ta/README.md)
    * [手写简单 parser](kuo-zhan-shu-zu/step11-shu-zu/qi-ta/manual-parser.md)
  * [规范](kuo-zhan-shu-zu/step11-shu-zu/spec.md)

## 参考资料

* [参考资料](can-kao-zi-liao/reference.md)

