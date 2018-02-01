from rply import LexerGenerator, Token
from collections import OrderedDict

reserved = ["true", "false", "and", "or", "not", "kek", "lol"]#["if", "else", "int", "end", "decls", "has"]

operators = OrderedDict([
    # ("COMMA", ","),
    ("PAREN_L", r"\("),
    ("PAREN_R", r"\)"),
    # ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"\/"),
    ("MOD", r"%"),
    ("CURLY_L", r"\{"),
    ("CURLY_R", r"\}")
    # ("SPACE", r" "),
    ])

lg = LexerGenerator()

lg.add("NUM", r"\d+")
lg.add("ID", r"[a-zA-Z_][a-zA-Z0-9_]*")

for key, value in operators.items():
    lg.add(key, value)

def id_reserved(token):
    if token.value.lower() in reserved:
        return Token(token.value, token.value)
    return token

callbacks = {
    "ID":(id_reserved, )
}

lg.ignore(r"\s+")
lg.ignore(r"#.*")
lexer = lg.build()

token_names = [rule.name for rule in lg.rules] + [name for name in reserved]

def lex(buf):
    for token in lexer.lex(buf):
        for callback in callbacks.get(token.name, []):
            token = callback(token)
        yield token

if __name__ == "__main__":
    from pprint import pprint
    from sys import stdin
    for token in lex(stdin.read()):
        pprint(token)







