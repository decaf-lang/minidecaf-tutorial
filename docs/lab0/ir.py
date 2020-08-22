def run(instrs):
    # instr: (opcode:str, operands:str)
    pc = 0          # program counter，从 0 开始，每条指令长度为 1
    stack = []      # 运算栈
    varstack = {}   # 变量栈，变量名到变量值的映射
    labels = { operands[0]: i
            for i, (op, *operands) in enumerate(instrs) if op == "LABEL" }
                    # 跳转标签名到指令地址的映射

    def push(x):
        stack.append(x)

    def pop(n=1):
        if n == 1: return stack.pop()
        return [stack.pop() for _ in range(n)]

    while pc < len(instrs):
        op, *operands = instrs[pc]
        if op                            == "PUSH":
            push(int(operands[0]))
        elif op                          == "LOAD":
            push(varstack[operands[0]])
        elif op                          == "STORE":
            varstack[operands[0]] = pop()
        elif op                          == "LABEL":
            pass
        elif op                          == "BZ":
            if pop() == 0:
                pc = labels[operands[0]]
                continue
        elif op                          == "B":
            pc = labels[operands[0]]
            continue
        elif op                          == "CMP_LE":
            rhs, lhs = pop(2)
            push(int(lhs <= rhs))
        elif op                          == "ADD":
            rhs, lhs = pop(2)
            push(lhs + rhs)
        else:
            raise Exception(f"invalid opcode {op}")
        pc += 1

    print(varstack["sum"])


def parse(progstr):
    prog = [line.split('#')[0] for line in progstr.strip().split('\n')] # 拿到每行，去掉注释
    return  [line.split() for line in prog if len(line) > 0] # 拆开操作码和操作数

progstr = """
PUSH 0
STORE sum # int sum = 0;
PUSH 1
STORE i # int i = 0;
LABEL loop
LOAD i
PUSH 100
CMP_LE # 计算i <= 100，前两句依次把左操作数i和右操作数100压入栈中
BZ end # 现在栈顶是i <= 100的结果，弹出它，如果它为0，即i <= 100不成立，则循环结束，否则进入循环体(下一条指令)
LOAD sum
LOAD i
ADD # 计算sum + i，前两句依次把左操作数sum和右操作数i压入栈中
STORE sum # 现在栈顶是sum + i的结果，弹出它，并且保存到sum中
LOAD i
PUSH 1
ADD # # 计算i + 1，前两句依次把左操作数i和右操作数1压入栈中
STORE i # 现在栈顶是i + 1的结果，弹出它，并且保存到i中
B loop # 回到loop的位置，又一次判断循环条件，执行循环体
LABEL end
"""

run(parse(progstr))
