# 说明

我们提供了一系列完整的 step1~step12 的参考实现，分别使用了不同的编程语言或词法语法分析工具，如下所示：
> 参考实现仅供参考，不是标准答案！

> git.tsinghua 上有[镜像](https://git.tsinghua.edu.cn/decaf-lang/minidecaf)

## [Python-ANTLR](./python-dzy.md)
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-dzy
* clone 命令：`git clone https://github.com/decaf-lang/minidecaf.git -b md-dzy`
* 演示网址：https://hoblovski.github.io/minidecaf-web/
  - 请耐心加载，可能要一分钟，加载好以后第一次编译要十秒，之后就快了
  - 因为要动态把 py 翻译成 js 然后执行，三重的缓慢

## Rust-lalr1
* 地址 https://github.com/decaf-lang/minidecaf/tree/mashplant
* clone 命令：`git clone https://github.com/decaf-lang/minidecaf.git -b mashplant`
* 演示网址：https://mashplant.online/minidecaf-frontend/
  - 除了加载可能因为网络原因稍慢，之后的运行都非常快。原理是Rust编译到[WASM](http://webassembly.org.cn/)在网页中执行，感兴趣的同学可以自行了解

## [TypeScript-ANTLR](./typescript-jyk.md)
* 地址 https://github.com/equation314/minidecaf
* clone 命令：`git clone https://github.com/equation314/minidecaf.git --recursive`
* 演示网址：https://equation314.github.io/minidecaf

## [Java-ANTLR](./java-xxy.md)
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-xxy
* clone 命令：`git clone https://github.com/decaf-lang/minidecaf.git -b md-xxy`

## C++-ANTLR
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-zj
* clone 命令：`git clone https://github.com/decaf-lang/minidecaf.git -b md-zj`

## C++-manual
* 地址 https://github.com/decaf-lang/minidecaf/tree/md-zyr
* clone 命令：`git clone https://github.com/decaf-lang/minidecaf.git -b md-zyr`

