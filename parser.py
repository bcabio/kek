from rply import ParserGenerator

from lexer import token_names, lex
import ast
# This is a list of the token names. precedence is an optional list of
# tuples which specifies order of operation for avoiding ambiguity.
# precedence must be one of "left", "right", "nonassoc".
# cache_id is an optional string which specifies an ID to use for
# caching. It should *always* be safe to use caching,
# RPly will automatically detect when your grammar is
# changed and refresh the cache for you.
pg = ParserGenerator(token_names)

# @pg.production("declist : INT varlst")
# def declist_int(p):
#     return p[0] + p[2]

# @pg.production("declist : declist INT varlst")
# def declist_list(p):
#     return p[0] + p[2]

# @pg.production("varlst : ID")
# def varlst_id(p):
#     return [ast.Identifier(p[0].getstr())]

@pg.production("statementlist : statement")
def statementlist_statement(p):
	return [p[0]]

@pg.production("statement : statementlist statement")
def statementlist_statementlist(p):
	return p[0] + [p[1]]



@pg.production("statement : ID ASSIGN exp")
def assign(p):
	assert p[0].gettokentype() == "ID"
	return ast.Assignment(ast.IdentifierReference(p[0].getstr()), p[2])

@pg.production("exp : term")
def exp_term(p):
    return p[0]

@pg.production("exp : exp PLUS term ")
@pg.production("exp : exp MINUS term")
def exp_binary_term(p):
	token_type, left, right = p[1].gettokentype(), p[0], p[2]
	if token_type == "PLUS":
		return ast.Add(left, right)
	elif token_type == "MINUS":
		return ast.Subtract(left, right)
	else:
		assert False, "Shouldn't be here"

@pg.production("term : factor")
def exp_factor(p):
	return p[0]

@pg.production("factor : NUM")
def factor_num(p):
	return ast.Number(int(p[0].getstr()))

@pg.production("factor : MINUS NUM")
def factor_negative_num(p):
	return ast.Number(-int(p[1].getstr()))

@pg.production("factor : ID")
def factor_id(p):
	return ast.IdentifierReference(p[0].getstr())

@pg.production("factor : PAREN_L exp PAREN_R")
def factor_parens(p):
	return p[1]


# @pg.production("declist : INT varlst")
# def expr_num(p):
#     return BoxInt(int(p[0].getstr()))



@pg.error
def error_handler(token):
    raise ValueError('Ran into a %s where it wasn\'t expected' % token)

parser = pg.build()


# print(parser.parse(lexer.lex("1 + 3 - 2+12-32")).value)   
# print(parser.parse(lexer.lex("5%3+3")).)
# print(parser.parse(lexer.lex("5 3")).eval())

if __name__ == "__main__":
	from pprint import pprint
	from sys import argv
	with open(argv[1], "r") as f:
		p = parser.parse(lex(f.read()))
		# pprint(p._asdict)
		# pprint(p.eval({}))
		print(p)
