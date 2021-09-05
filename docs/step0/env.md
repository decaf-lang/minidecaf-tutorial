# 实验框架环境配置

## C++ 实验框架环境配置

关于操作系统，助教推荐使用 Linux 环境（如 Ubuntu，Debain 或 Windows 下的 WSL 等），当然你也可以在类 Unix 系统环境（Mac OS）中进行开发。助教不推荐直接在 Window 中搭建开发环境。对于 C++ 实验框架，你需要安装或保证如下软件满足我们的要求：

> TODO：详细介绍一下Mac中各种工具安装的细节。

1. Flex

   Flex 是一个自动生成词法分析器的工具，它生成的词法分析器可以和 Bison 生成的语法分析器配合使用。我们推荐从 [Github](https://github.com/westes/flex/releases) 下载安装最新版本(在2021.9.1, 最新版本是2.6.4,不推荐使用低于2.6的版本)。

   在ubuntu下，`apt-get install flex` 安装的flex版本为2.6,是可用的。

2. Bison

   Bison是一个自动生成语法分析器的工具,它生成的语法分析器可以和Flex生成的词法分析器配合使用。我们推荐从[官网](http://ftp.gnu.org/gnu/bison/)下载安装最新版本（在2021.9.1, 最新版本是3.7.6，不推荐使用低于3.7的版本,如ubuntu apt-get install安装的3.0.4版本是不可用的）。
   
   下载解压tar.gz文件后， 在路径下执行`./configure && make && make install`, 就应该能正确安装。如果发生失败，就尝试`sudo ./configure` `sudo make`, `sudo make install`, 然后`bison --version`检查一下版本是否为3.7.6就可以了。

3. Boehmgc

   C++ 语言的实验框架中，为了简化内存分配的处理，使用了一个第三方垃圾回收库，简单来说，使用这个垃圾回收库提供垃圾回收功能后，我们在框架里可以new了之后不用delete也不会出问题。
   
   在ubuntu下,通过 `apt-get install libgc-dev`安装的boehmgc库是可用的。


4. gcc

   助教推荐的 gcc 版本为 8.5.0。

   > 需要注意的是，如果你使用 Mac OS 进行开发，Mac 自带的 g++ 命令极有可能软链接到了 clang，我们的实验框架在某些版本的 clang 下无法编译通过，因此推荐你使用如下方法安装特定版本的 gcc。安装完成之后，你需要使用 gcc-8，g++-8 来调用特定版本的 gcc，g++，同时你需要修改我们提供的 Makefile 中的 CC 与 CXX 选项。

   ```bash
   # Mac OS
   $ brew install gcc@8
   # Ubuntu
   $ sudo apt-get install gcc-8
   ```

## python 实验框架环境配置

关于操作系统，类似 C++，但由于 python 的跨平台性，理论上也可以在 Windows 下进行开发。但**不保证Windows和在线测试环境下程序行为的一致性**。由于 python 自带的包管理系统 pip，安装推荐的依赖只需执行如下命令。

```bash
$ pip install -r ./requirements.txt 
```

1. python 3.9

   框架本身在 python 3.9 下进行开发，使用了 python 3.9 的新特性并仅在这一版本下经过测试。请保证你所使用的 python 版本高于此版本。

2. argparse

   框架使用了 [argparse](https://docs.python.org/zh-cn/3/library/argparse.html) 以处理命令行参数。官方文档中提供了它的[教程](https://docs.python.org/zh-cn/3/howto/argparse.html)。

3. ply

   ply是一个自动生成词法分析器和语法分析器的工具，其中ply.lex为词法分析相关的模块而ply.yacc为语法分析相关。我们提供了 ply 的[文档](https://www.dabeaz.com/ply/ply.html)。

助教推荐使用类似 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 的系统以最小化出现奇怪依赖问题的风险。助教推荐在项目中使用 [type hints](https://www.python.org/dev/peps/pep-0483/)，如果你习惯在 vscode 中进行开发的话同时推荐使用 [pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) 这一插件。


## 必做：测试你是否正确配置好了环境
### C++ 实验框架

1. 确定各工具的版本

   ```bash
   # g++
   $ g++-8 -v
   # Flex
   $ flex --version
   # Bison
   $ bison --version
   ```

