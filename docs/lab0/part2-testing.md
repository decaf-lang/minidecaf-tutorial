## 测试

你可以修改[minidecaf测试](https://github.com/decaf-lang/minidecaf-tests)中的自动批量测试脚本，来测试你的编译器是否正常通过所有[step1测试用例](https://github.com/decaf-lang/minidecaf-tests/tree/master/examples/step1)。它将使用你的编译器编译一组测试程序，执行它们，并确保它们返回正确的值。


为了用脚本自动批量测试一组程序，你写的编译器需要遵循这个规范。

1. 它可以从命令行中调用，只需要一个C源文件作为参数，例如：1: `./YOUR_COMPILER /path/to/program.c`。
2. 当传入`program.c`时，它会在同一目录下生成`program.s`汇编代码文件。
3. 如果解析失败，它不会生成汇编代码文件。

脚本不会检查你的编译器是否输出合理的错误信息。