from rply import ParserGenerator

from lexer import token_names, lex
import ast


pg = ParserGenerator(token_names)

# Whole program
@pg.production("program : statements")
def program(p):
	return ast.Program(p)

@pg.production("statements : statement")
def statementlist_statement(p):
	return p[0]

@pg.production("statements : statements statement")
def statementlist_statementliststatement(p):
	return p[0]

@pg.production("statement : ID ASSIGN exp SEMICOLON")
def assign(p):
	assert p[0].gettokentype() == "ID"
	return ast.Assignment(ast.IdentifierReference(p[0].getstr()), p[2])

@pg.production("exp : term")
def exp_term(p):
    return p[0]

@pg.production("exp : exp PLUS term ")
@pg.production("exp : exp MINUS term")
@pg.production("exp : exp MULTIPLY term")
@pg.production("exp : exp DIVIDE term")
@pg.production("exp : exp MOD term")
def exp_binary_term(p):
	token_type, left, right = p[1].gettokentype(), p[0], p[2]
	if token_type == "PLUS":
		return ast.Add(left, right)
	elif token_type == "MINUS":
		return ast.Subtract(left, right)
	elif token_type == "MULTIPLY":
		return ast.Multiply(left, right)
	elif token_type == "DIVIDE":
		return ast.Divide(left, right)
	elif token_type == "MOD":
		return ast.Modulus(left, right)
	else:
		assert False, "Something went wrong"

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
		pprint(p.eval({}))
		# pprint(p.eval({}))
		# print(p)
