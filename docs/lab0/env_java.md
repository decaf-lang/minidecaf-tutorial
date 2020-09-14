# java+gradle+antlr环境配置

对于使用java编程语言的同学，我们推荐使用java+gradle的项目维护方法。在参考实现中，我们使用了antlr生成parser代码，下面简单介绍一下相关环境的配置方法。

## java: jdk14

对于使用java的同学，我们推荐使用最新的jdk14版本。[下载地址](https://www.oracle.com/java/technologies/javase-jdk14-downloads.html)

从以上的链接下载最新的jdk版本后，设置环境变量即可。关于设置环境变量的教程，可以参考
* [windows系统安装java](https://www.cnblogs.com/ssrs-wanghao/articles/8994856.html)
* [linux系统安装java](https://blog.csdn.net/sangewuxie/article/details/80958611)
* [macos系统安装java](https://www.jianshu.com/p/7a04658af4f9)

对于linux/macos系统，也可以使用apt、brew等包维护工具进行安装。
安装之后，运行以下命令即可检测是否安装成功：

```
java --version
javac --version
```

## gradle

为了更便捷地维护整个项目，我们推荐使用项目自动化构建工具gradle。

对于linux系统，可以使用apt工具安装：

```
sudo apt install gradle
```

同样地，对于macos系统，可以使用homebrew进行安装：

```
brew install gradle
```

对于Windows用户/不愿意使用包维护工具进行安装的同学，可以使用下载并配置环境变量的方法：

[下载地址](https://gradle.org/releases/)

下载之后，将对应的bin文件夹添加至`PATH`环境变量中即可。安装之后，可以使用如下命令检测是否安装成功：

```
gradle -v
```

如果使用eclipse等IDE进行编程，可能需要在IDE中对gradle的路径进行设置。

[Eclipse配置Gradle](https://blog.csdn.net/forever_insist/article/details/85228930)
[IntelliJ IDEA配置Gradle](https://blog.csdn.net/achenyuan/article/details/80682288)

## antlr4（可选）

在参考实现中，我们使用了antlr生成parser代码，对于希望使用antlr生成parser代码而不是手写parser的同学，我们提供如下的antlr配置方法：

### Eclipse

Eclipse IDE中配置antlr的方法很简单，在Help/Eclipse Marketplace中搜索antlr，安装antlr IDE即可。[参考链接](https://blog.csdn.net/zjq_1314520/article/details/65935718)

### IntelliJ IDEA

在[插件下载链接](https://www.antlr.org/tools.html)中下载插件进行安装即可。

[参考链接](https://www.cnblogs.com/solvit/p/10097453.html)

### VSCode

VSCode中也包含antlr的语法高亮工具，可以搜索后自行安装。

### 直接安装

在[下载链接](https://www.antlr.org/download/antlr-4.8-complete.jar)中下载antlr的jar包，配置环境变量即可。[环境配置参考链接](https://www.crifan.com/build_up_antlr_v4_environment/)