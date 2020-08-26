import re


class TokenType:
    def __init__(self, name:str, ptn:str, action=None, keepText=False):
        """name 比如 Ident, Integer，ptn 是一个正则表达式。
        keepText 是给 parser 用的，让输出漂亮一点；
        action 可以是 "ignore" 或者 "error"，方便忽略空白字符和报错"""
        self.name = name
        self.ptn = re.compile('^' + ptn) # ^ 表示输入开头
        self.action = action
        self.keepText = keepText

    def __call__(self, txt:str):
        m = self.ptn.search(txt)
        if m is not None:
            return m.span()[1]
        return 0



class Lexer:
    def __init__(self, tokens:list):
        self.tokens = tokens # [TokenType]

    def setInput(self, txt:str):
        self.txt = txt
        self.pos = 0

    def lex(self):
        """用 yield 返回一个 generator，表示 token stream，后续阶段按需从 generator 里面拿 token；
        而不是一口气做完所有词法分析，然后返回一个列表，包含了所有的 token。"""
        while len(self.txt) != 0:
            matchResult = [tok(self.txt) for tok in self.tokens]
            # 如果有多个最大值, max 返回第一个
            i, l = max(enumerate(matchResult), key=lambda x:x[1])
            tt = self.tokens[i]
            if tt.action == "skip":
                pass
            elif tt.action == "error":
                raise Exception(f"lex error at input position {self.pos}")
            else:
                yield (tt, self.txt[:l])
            self.txt = self.txt[l:]
            self.pos += l


def dumpLexerTokens(lexer):
    for (typ, text) in lexer.lex():
        print(f"{typ.name:<10} {text:<20}")


def default():
    identLeadChar = "[a-zA-Z_]"
    digitChar = "[0-9]"
    wordChar = "[a-zA-Z0-9_]"
    whitespaceChar = "[ \r\n\t]"

    lexer = Lexer([
        # 关键字。每个关键字用一个单独的 Token 描述。
        TokenType("Int", "int"),
        TokenType("Return", "return"),
        # 标点符号。
        TokenType("Lbrace", "\\{"),
        TokenType("Rbrace", "\\}"),
        TokenType("Lparen", "\\("),
        TokenType("Rparen", "\\)"),
        TokenType("Semicolon", ";"),
        # 标识符。
        TokenType("Ident", f"{identLeadChar}{wordChar}*", keepText=True),
        # 整数。非负，可以有前导零。
        TokenType("Integer", f"{digitChar}+", keepText=True),
        # 空白。所有空白都被忽略。
        TokenType("Whitespace", f"{whitespaceChar}+", action="skip"),
        # 我们不认识的，报错。
        TokenType("Error", f".", action="error"),
    ])

    lexer.setInput("""\
    int main() {
        return 123;
    }
    """)
    return lexer


if __name__ == "__main__":
    dumpLexerTokens(default())
