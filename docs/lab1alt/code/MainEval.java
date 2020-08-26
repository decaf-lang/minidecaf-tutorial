import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.IOException;
import java.util.List;
import java.util.Iterator;

public class MainEval {
    public static void main(String[] args) throws IOException {
        CharStream  input   = CharStreams.fromStream(System.in);
        Lexer       lexer   = new ExprLexer(input);
        TokenStream tokens  = new CommonTokenStream(lexer);
        ExprParser  parser  = new ExprParser(tokens);
        ParseTree   tree    = parser.expr(); // 取得一颗以 expr 为根的 AST
        EvalVisitor visitor = new EvalVisitor();
        System.out.println(tree.accept(visitor));
    }
}


class EvalVisitor extends ExprBaseVisitor<Integer> {
    @Override public Integer visitAdd(ExprParser.AddContext ctx) {
        // ctx.add() 返回 add 子结点。
        if (ctx.add() == null)
            // 这个结点是 add: mul;
            return visitChildren(ctx);
        // 这个结点是 add: add op=(Add|Sub) mul;
        int lhs = ctx.add().accept(this);
        int rhs = ctx.mul().accept(this);
        // 访问 op 子结点不是 ctx.op() 而是 ctx.op.
        // 用 .getText() 取得字符串
        switch (ctx.op.getText()) {
            case "+": return lhs + rhs;
            case "-": return lhs - rhs;
        }
        return 0; // unreachable
    }

    @Override public Integer visitMul(ExprParser.MulContext ctx) {
        // 包含所有 atom 子结点
        List<ExprParser.AtomContext> atoms = ctx.atom();
        List<ExprParser.MulOpContext> ops = ctx.mulOp();
        int s = atoms.get(0).accept(this);
        Iterator<ExprParser.AtomContext> itAtom = atoms.iterator();
        Iterator<ExprParser.MulOpContext> itOps = ops.iterator();
        for (itAtom.next(); itAtom.hasNext();) {
            // 使用 .getText() 取得字符串
            if (itOps.next().getText().equals("*"))
                s *= itAtom.next().accept(this);
            else
                s /= itAtom.next().accept(this);
        }
        return s;
    }

    @Override public Integer visitAtomParen(ExprParser.AtomParenContext ctx) {
        // visitChilren 返回的是 ctx.Rparen().accept(this)
        return ctx.expr().accept(this);
    }

    @Override public Integer visitAtomInteger(ExprParser.AtomIntegerContext ctx) {
        return Integer.parseInt(ctx.Integer().getText());
    }
}
