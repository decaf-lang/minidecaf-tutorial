import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        CharStream  input  = CharStreams.fromStream(System.in);
        Lexer       lexer  = new ExprLexer(input);
        TokenStream tokens = new CommonTokenStream(lexer);
        ExprParser  parser = new ExprParser(tokens);
        ParseTree   tree   = parser.expr(); // 取得一颗以 expr 为根的 AST
        System.out.println(tree.toStringTree(parser));
    }
}
