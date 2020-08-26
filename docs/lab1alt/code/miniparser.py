import minilexer


# 大写字母。parser 语法里面，首字母大写的是终结符，小写的是非终结符。
BIG_LETTERS = { chr(x) for x in range(65, 91) }


class Node:
    """语法树结点。叶子结点是终结符、内部结点是非终结符。"""
    def __init__(self, label:str, text:str=None, children:list=[]):
        """如果是叶子结点（即 token），那 text 是这个 token 的字符串，并且 children 为空。
        如果是内部结点，那 text 为 None，children 是它的产生式的右手边。"""
        self.label = label
        self.text = text
        self.children = children

    def __str__(self):
        if self.text is None:
            return f"{self.label}({', '.join([str(x) for x in self.children])})"
        if len(self.text) == 0: # 终结符没文字，没必要加括号
            return f"{self.label}"
        return f"{self.label}({self.text})"


class Parser:
    def __init__(self, rules:dict):
        self.rules = rules # str 产生式左手边 -> list 右手边

    def setInput(self, lexer):
        self.lex = lexer.lex()
        self.tree = []

    def parse(self, nonterm:str):
        """nonterm 是一个非终结符。分析输入，返回一个以 nonterm 为根的语法树。
        你不需要看懂这个算法，即使它不是很难！"""
        children = []
        for child in self.rules[nonterm]:
            if child[0] in BIG_LETTERS:
                # 按需返回 token
                typ, text = next(self.lex)
                if typ.name != child: raise Exception("syntax error")
                text = text if typ.keepText else ""
                children.append(Node(typ.name, text=text))
            else:
                children.append(self.parse(child))
        return Node(nonterm, children=children)

    def fromRules(s):
        rules = [line.split() for line in s.strip().split('\n')]
        rules = { r[0] : r[2:] for r in rules } # r[1] 是 ':'
        return Parser(rules)


def default():
    # 描述我们 step1 的语法
    rules = """
    prog : func
    func : ty Ident Lparen Rparen Lbrace stmt Rbrace
    ty   : Int
    stmt : Return expr Semicolon
    expr : Integer
    """

    parser = Parser.fromRules(rules)
    # lexer 的输出喂给 parser 当输入
    parser.setInput(minilexer.default())
    return parser


if __name__ == "__main__":
    print(default().parse("prog"))

