# 函数序言（prologue）、尾声（epilogue）和调用

概念 prologue epilogue 和 calling sequence

…… 无论哪个函数 …… 开头和结尾基本固定的一段代码 ……

序言 …… 设立栈帧 …… callee save 

尾声 …… 销毁栈帧 …… callee restore …… jr ra

调用不光是一条 call 代码 …… caller save, 传参, call，保存返回值，caller restore
