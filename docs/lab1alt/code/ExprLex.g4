lexer grammar ExprLex;

// 括号
Lparen: '(';
Rparen: ')';

// 运算符
Add: '+';
Sub: '-';
Mul: '*';
Div: '/';

// 整数
Integer: [0-9]+;

// 空白
fragment WhitespaceChar: [ \t\n\r];
Whitespace: WhitespaceChar+ -> skip;
