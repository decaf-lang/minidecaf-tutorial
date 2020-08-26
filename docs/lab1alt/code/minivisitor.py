import miniparser



def accept(self, visitor):
    if self.label == "prog": return visitor.visitProg(self)
    if self.label == "func": return visitor.visitFunc(self)
    if self.label == "ty":   return visitor.visitTy(self)
    if self.label == "stmt": return visitor.visitStmt(self)
    if self.label == "expr": return visitor.visitExpr(self)
    raise Exception("bad node")

# 给 Node 实现 accept 方法，一种不太好的写法
miniparser.Node.accept = accept


class Visitor:
    """默认行为是遍历、但什么也不做"""
    def visitProg(self, node:miniparser.Node):
        node.children[0].accept(self) # func

    def visitFunc(self, node:miniparser.Node):
        node.children[0].accept(self) # ty
        node.children[5].accept(self) # stmt

    def visitTy(self, node:miniparser.Node):
        pass

    def visitStmt(self, node:miniparser.Node):
        node.children[1].accept(self) # expr

    def visitExpr(self, node:miniparser.Node):
        pass


class TargetCodeEmission(Visitor):
    def visitStmt(self, node:miniparser.Node):
        expr = node.children[1]
        Integer = expr.children[0]
        value = int(Integer.text)
        # 下面的就是汇编模板
        print(f""".text
	.globl	main
main:
	li	a0,{value}
	ret""")


def default():
    parser = miniparser.default()
    ast = parser.parse("prog")
    visitor = TargetCodeEmission()
    ast.accept(visitor)


if __name__ == "__main__":
    default()
