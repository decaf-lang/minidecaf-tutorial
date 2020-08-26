import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):
    def visitAdd(self, ctx:ExprParser.AddContext):
        # ctx.add() 返回 add 子结点。
        if ctx.add() is None:
            # 这个结点是 add: mul;
            return self.visitChildren(ctx)
        # 这个结点是 add: add op=(Add|Sub) mul;
        lhs = ctx.add().accept(self)
        rhs = ctx.mul().accept(self)
        # 访问 op 子结点不是 ctx.op() 而是 ctx.op.
        # type(ctx.op) == Token，所以用 .text 取得字符串
        #（这是 Python API 一个不完善的地方, 本来应该用 .getText() 的）
        if ctx.op.text == '+':
            return lhs + rhs
        else:
            return lhs - rhs

    def visitMul(self, ctx:ExprParser.MulContext):
        # 返回一个 list，包含所有 atom 子结点
        atoms = ctx.atom()
        ops = ctx.mulOp()
        s = atoms[0].accept(self)
        for i in range(len(ops)):
            # ops[i] 是非终结符 mulOp，类型是 MulOpContext 继承(ParserRuleContext)
            # 所以用 .getText() 取得字符串
            if ops[i].getText() == '*':
                s *= atoms[i+1].accept(self)
            else:
                s //= atoms[i+1].accept(self)
        return s

    def visitAtomParen(self, ctx:ExprParser.AtomParenContext):
        # visitChilren 返回的是 ctx.Rparen().accept(self)
        return ctx.expr().accept(self)

    def visitAtomInteger(self, ctx:ExprParser.AtomIntegerContext):
        # ctx.Integer() 类型是 TerminalNodeImpl
        # 也用 .getText() 取得字符串
        return int(ctx.Integer().getText())
        # return int(ctx.getText()) # 和上面等价的


def main():
    input   = InputStream(sys.stdin.read())
    lexer   = ExprLexer(input)
    tokens  = CommonTokenStream(lexer)
    parser  = ExprParser(tokens)
    tree    = parser.expr() # 取得一颗以 expr 为根的 AST
    visitor = EvalVisitor()
    print(tree.accept(visitor))


if __name__ == '__main__':
    main()

