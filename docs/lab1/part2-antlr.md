在阅读此文档前，请确保你已了解什么是**语法分析（parsing）**。

[ANTLR](https://www.antlr.org/) 是一个语法分析器的生成器，你只需要写出语法和必要的词法，它便可以帮你自动生成词法解析和语法解析的代码，并未生成的词法解析器和语法解析器提供必要的运行时库环境。

ANTLR 支持多种语言作为代码生成目标，这里以 Java 为例，其他语言比如 Python、C++ 或 JavaScript 可以参阅[这里](https://github.com/antlr/antlr4/blob/master/doc/targets.md) 和我们所提供的参考框架的使用方式。

## 安装

ANTLR 本身是用 Java 写的，所以为了使用 ANTLR，你需要确保你已经安装了 [Java(1.6+)](https://www.java.com/zh_CN/download/)。

下面提供 UNIX 下的安装过程

1. 下载 ANTLR
```bash
$ cd /usr/local/lib
$ curl -O https://www.antlr.org/download/antlr-4.7.1-complete.jar
```
2. 将 ANTLR 添加进 JAVA 的环境变量 `CLASSPATH` 中，并为冗长的使用指令创建别名
```bash
$ export CLASSPATH=".:/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH"
$ alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
$ alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'
```
最好是将上述指令放到你的启动脚本中（比如 `~/.bash_profile`）。

想要了解更多细节或其他 OS 环境的安装方式，建议阅读[官方安装教程](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)。

TODO：上面是直接从官方安装教程里抄过来的，不太清楚这是不是最合适的方式。也许直接用 Gradle 插件更简单？

TODO: 应该还需要写一下测试安装是否成功？

## 语法

TODO: 我其实也不知道 ANTLR 的词法和语法产生式左侧和右侧“该怎么写”，我之前都是抄过来然后直接魔改的，也许我还需要再仔细学习一下……

TODO: 感觉各位助教的文法和语法写得也差别很大呀，tsz 看起来用了好高端的 feature……

```java
grammar Hello; // Define a grammar called Hello
r : 'hello' ID ; // match keyword hello followed by an identifier
ID : [a-z]+ ; // match lower-case identifiers
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines, \r (Windows)
```

TODO: 作为一个额外的功能， alternative 肯定是要介绍一下的QAQ

## Listener 模式和 Visitor 模式

ANTLR 会为你自动生成一棵语法分析树，并提供两种基本的遍历分析树的方式，*listener* 模式和 *visitor* 模式。

Listener 模式提供了先序遍历分析树时进入和退出一个节点的接口。

Visitor 模式则允许你控制遍历树的方式（当然你也可以选择在某一个节点不再向下遍历），如果你还不了解 visitor 模式的话，可以看[这里]()。

TODO: 也许这里应该提供两个实际代码的例子？当然，可以把官方文档直接抄过来……

## 参考资料

如果想要了解关于 ANTLR 的更多细节，建议阅读官方文档 *The definitive ANTLR 4 reference*。

TODO: ANTLR 的官方文档 *The definitive ANTLR 4 reference* 是收费的，也许应该向 ANTLR 团队发邮件请求许可，并提供给学生？