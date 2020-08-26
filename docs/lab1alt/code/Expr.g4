grammar Expr;

import ExprLex;

expr
    : add
    ;
add
    : add op=('+'|'-') mul
    | mul
    ;
mul
    : atom (mulOp atom)*
    ;
atom
    : '(' expr ')'      # atomParen
    | Integer           # atomInteger
    ;
mulOp
    : '*' | '/' ;
