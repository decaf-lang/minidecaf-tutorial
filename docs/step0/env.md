# 实验框架环境配置

## C++ 实验框架环境配置

关于操作系统，助教推荐使用 Linux 环境（如 Ubuntu，Debain 或 Windows 下的 WSL 等），当然你也可以在类 Unix 系统环境（Mac OS）中进行开发。助教不推荐直接在 Window 中搭建开发环境。对于 C++ 实验框架，你需要安装或保证如下软件满足我们的要求：

1. Flex

   Flex 是一个自动生成词法分析器的工具，它生成的词法分析器可以和 Bison 生成的语法分析器配合使用。我们推荐从 [Github](https://github.com/westes/flex/releases) 下载安装最新版本(在 2021.9.1, 最新版本是 2.6.4,不推荐使用低于 2.6 的版本)。

   在 Ubuntu 下，`apt-get install flex` 安装的 Flex 版本为 2.6，是可用的。

   在 Mac OS 下，推荐使用 homebrew 进行安装，`brew install flex` 安装的 Flex 版本为 2.6，是可用的。

2. Bison

   Bison是一个自动生成语法分析器的工具,它生成的语法分析器可以和Flex生成的词法分析器配合使用。

   在 Ubuntu 下，我们推荐从[官网](http://ftp.gnu.org/gnu/bison/)下载安装最新版本（在2021.9.1, 最新版本是3.7.6，不推荐使用低于3.7的版本,如 Ubuntu apt-get install 安装的3.0.4版本是不可用的）。下载解压 tar.gz 文件后， 在路径下执行`./configure && make && make install`, 就应该能正确安装。如果发生失败，就尝试`sudo ./configure` `sudo make`, `sudo make install`, 然后`bison --version`检查一下版本是否为3.7.6就可以了。

   在 Mac OS 下，推荐使用 homebrew 进行安装，`brew install bison` 安装的 Bison 版本为 3.7.6，是可用的。

   > 如果你是 Mac OS 用户，需要注意的是，系统可能已经安装了低版本的 flex 与 bison，安装的新版本工具会被覆盖，需要通过以下命令确认一下二者的版本：

   ```bash
   $ flex --version
   $ bison --version
   ```

   如果版本较低，需要将新安装的工具路径加入环境变量，关于路径，在**助教的电脑**上是：

   ```
   Flex: /usr/local/Cellar/flex/2.6.4_2/bin
   Bison: /usr/local/Cellar/bison/3.7.6/bin
   ```

3. Boehmgc

   C++ 语言的实验框架中，为了简化内存分配的处理，使用了一个第三方垃圾回收库，简单来说，使用这个垃圾回收库提供垃圾回收功能后，我们在框架里可以new了之后不用delete也不会出问题。

   在 Ubuntu 下，通过  `apt-get install libgc-dev ` 安装的 boehmgc 库是可用的。

   在 Mac OS 下，通过 `brew install libgc`  安装的 boehmgc 库是可用的。


4. gcc

   助教推荐的 gcc 大版本号为 8。当然，只要能通过编译且编译器程序能正确运行，其他版本也可以。

   > 需要注意的是，如果你使用 Mac OS 进行开发，Mac 自带的 g++ 命令极有可能软链接到了 clang，我们的实验框架在某些版本的 clang 下无法编译通过，因此推荐你使用如下方法安装特定版本的 gcc。安装完成之后，你需要使用 gcc-8，g++-8 来调用特定版本的 gcc，g++，同时你需要修改我们提供的 Makefile 中的 CC 与 CXX 选项。
   >
   > 另外，由于你使用了自己安装的 g++-8 编译程序，你需要将 boehmgc 的路径加入 g++ 的环境变量：

   ```bash
   # 你需要将以下内容加入你终端的配置文件（zsh->.zshrc; bash->.bash_profile)
   export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/local/include"
   export LIBRARY_PATH="$LIBRARY_PATH:/usr/local/lib"
   export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib
   ```

   ```bash
   # Mac OS
   $ brew install gcc@8
   # Ubuntu
   $ sudo apt-get install gcc-8
   ```


> 需要说明的是，C++ 的环境配置较为复杂，教程可能无法覆盖到所有问题，欢迎随时联系助教。

## python 实验框架环境配置

关于操作系统，类似 C++，但由于 python 的跨平台性，理论上也可以在 Windows 下进行开发。但**不保证Windows和在线测试环境下程序行为的一致性**。由于 python 自带的包管理系统 pip，安装推荐的依赖只需执行如下命令。

```bash
$ pip install -r ./requirements.txt 
```

1. python 3.9

   框架本身在 python 3.9 下进行开发，使用了 python 3.9 的新特性并仅在这一版本下经过测试。请保证你所使用的 python 版本高于此版本。

   

   Linux环境下安装Python 3.9可以尝试如下命令：
```bash
> sudo add-apt-repository ppa:deadsnakes/ppa
> sudo apt update
> sudo apt install python3.9
```
修改~/.bashrc文件，在末尾加上`` alias python='/usr/bin/python3.9' ``。然后运行：
```bash
> source ~/.bashrc
```
此外，也可以通过``update-alternatives``命令修改python版本使用的优先级，对所有服务器用户都有效，具体用法请见 [https://medium.com/analytics-vidhya/how-to-install-and-switch-between-different-python-versions-in-ubuntu-16-04-dc1726796b9b]( https://medium.com/analytics-vidhya/how-to-install-and-switch-between-different-python-versions-in-ubuntu-16-04-dc1726796b9b)。

如果想为指定的Python版本（比如3.9）安装所依赖的包，可以用如下命令：

```bash
> python3.9 -m pip install -r ./requirements.txt
```


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

