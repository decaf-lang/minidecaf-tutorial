# 实验框架环境配置

## Python 实验框架环境配置

关于操作系统，助教推荐使用 Linux 环境（如 Ubuntu，Debain 或 Windows 下的 WSL 等），当然你也可以在类 Unix 系统环境（Mac OS）中进行开发。助教不推荐直接在 Window 中搭建开发环境。你需要安装或保证如下软件满足我们的要求：

1. python >= 3.10

   助教**强烈建议**使用类似 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或venv的系统管理不同的Python环境。你可以方便地使用miniconda安装最新的Python版本，安装好之后使用pip安装依赖即可。

   框架本身在 python 3.10 下进行开发，使用了 python 3.10 的新特性，请保证你所使用的 python 版本高于此版本。

   如果你**没有**使用虚拟环境，可以参考下面的指导。Linux 环境下安装 Python 3 可以尝试如下命令：
   ```bash
   > sudo add-apt-repository ppa:deadsnakes/ppa
   > sudo apt update
   > sudo apt install python3
   ```

   此外，如果安装了多个版本的 python，可以通过 `update-alternatives` 命令修改 python 版本使用的优先级，对所有服务器用户都有效，具体用法可参见[这里]( https://medium.com/analytics-vidhya/how-to-install-and-switch-between-different-python-versions-in-ubuntu-16-04-dc1726796b9b)。你可以通过此命令来检查当前优先的 Python3 版本：
   ```
   > python3 --version
   ```

   框架里已经提供了需要的 python 包列表文件 requirements.txt，你可以通过 pip 命令安装下文提到的 python 依赖包 ply 和 argparse：

   ```bash
   $ python3 -m pip install -r ./requirements.txt 
   ```

2. argparse

   框架使用了 [argparse](https://docs.python.org/zh-cn/3/library/argparse.html) 以处理命令行参数。官方文档中提供了它的[教程](https://docs.python.org/zh-cn/3/howto/argparse.html)。

3. ply

   ply是一个自动生成词法分析器和语法分析器的工具，其中ply.lex为词法分析相关的模块而ply.yacc为语法分析相关。可以参考 ply 的[文档](https://www.dabeaz.com/ply/ply.html)。

助教在项目中使用 [type hints](https://www.python.org/dev/peps/pep-0483/)，如果你习惯在 vscode 中进行开发的话同时推荐使用 [pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) 这一插件。

由于 python 的跨平台性，理论上也可以在 Windows 下进行开发。但**不保证Windows和在线测试环境下程序行为的一致性**。
