# 实验指导 step10：全局变量
step10 我们要支持的是全局变量，语法改动非常简单：

<pre id='vimCodeElement'><code></code>
<div class="changed"><span class="SpecRuleStart">program</span>
<span class="SpecRuleIndicator">    :</span> <span class="SpecOperator">(</span><span class="SpecRule">function</span> <span class="SpecOperator">|</span> <span class="SpecRule">declaration</span><span class="SpecOperator">)*</span>
</div></pre>

全局变量和局部变量不同，它不是分配在栈上，而是放在某个固定地址，写在汇编的 .bss 段或 .data 段里。
访问它也不能通过 `fp` 加偏移量，而是需要通过它的符号加载它的地址，通过它的地址访问它。
> 汇编课上应该讲过，实际中（包括 gcc 和 qemu）使用的可执行文件的格式是 ELF（Executable and Linking Format）。
> .text 是其中存放代码的段（section），.bss 和 .data 都是其中存放数据的段，前者零初始化后者须指定初始值。
>
> 对有兴趣的同学：
> 全局变量地址不是被狭义上的编译器（compiler）确定的，也不是被汇编器（assembler）确定的，而是被链接器（linker）或加载器（loader）确定的。
> 简单的说，狭义上的编译器把源代码变成文本汇编，汇编器把文本汇编给编码到二进制代码，然后通过链接器变成可执行文件，运行时由加载器加载到内存中运行。
> 当然，广义上的编译器就囊括了这所有阶段。
