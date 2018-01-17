from rply import ParserGenerator

from lexer import lexer

# This is a list of the token names. precedence is an optional list of
# tuples which specifies order of operation for avoiding ambiguity.
# precedence must be one of "left", "right", "nonassoc".
# cache_id is an optional string which specifies an ID to use for
# caching. It should *always* be safe to use caching,
# RPly will automatically detect when your grammar is
# changed and refresh the cache for you.
pg = ParserGenerator(["NUMBER", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MOD"],
        precedence=[
            ("left", ['PLUS', 'MINUS']),
            ("left", ['MULTIPLY', 'DIVIDE', 'MOD'])
        ], cache_id="myparser")

@pg.production("main : expr")
def main(p):
    # p is a list, of each of the pieces on the right hand side of the
    # grammar rule
    return p[0]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
@pg.production("expr : expr MULTIPLY expr")
@pg.production("expr : expr DIVIDE expr")
@pg.production("expr : expr MOD expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    elif p[1].gettokentype() == "MULTIPLY":
        return BoxInt(lhs * rhs)
    elif p[1].gettokentype() == "DIVIDE":
        return BoxInt(lhs / rhs)
    elif p[1].gettokentype() == "MOD":
        return BoxInt(lhs % rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

@pg.error
def error_handler(token):
    raise ValueError('Ran into a %s where it wasn\'t expected' % token)

parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

# print(parser.parse(lexer.lex("1 + 3 - 2+12-32")).value)   
print(parser.parse(lexer.lex("5%3+3")).value)
# print(parser.parse(lexer.lex("5 3")).eval())