#### ☑任务：

#### 词法分析

我们需要添加逗号来分隔函数参数，因此你需要在你的 Token 识别中增加对逗号`,`的支持。

#### 语法分析

更新你的*parse*函数，使其可以为所有有效的[step9测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/testcases/step9)建立正确的AST，并保证之前的测试用例不被影响。