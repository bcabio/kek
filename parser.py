from rply import ParserGenerator

from lexer import token_names, lex
import ast


pg = ParserGenerator(
	token_names,
	precedence=[
		('left', ['PLUS', 'MINUS']),
		('left', ['MULTIPLY', 'DIVIDE', ]),
		# ('left', ['PAREN_L, PAREN_R'])
	])

# Whole program
@pg.production("program : statements")
def program(p):
	return ast.Program(p)

@pg.production("statements : statement")
def statementlist_statement(p):
	return [p[0]]

@pg.production("statements : statements statement")
def statementlist_statementliststatement(p):
	# print(p[0] + [p[1]])
	return p[0] + [p[1]]

@pg.production("statement : ID kek assignment")
def assign(p):
	assert p[0].gettokentype() == "ID"
	return ast.Assignment(ast.IdentifierReference(p[0].getstr()), p[2])

@pg.production("assignment : exp")
def assignment_exp(p):
	return p[0]

# Expression definition
@pg.production("exp : math_exp")
def assignment_expression(p):
	return p[0]

@pg.production("exp : boolean_expression")
def boolean_expression_assignment(p):
	return p[0]

# Numeric expression
@pg.production("math_exp : term")
def exp_term(p):
    return p[0]

@pg.production("math_exp : math_exp PLUS math_exp ")
@pg.production("math_exp : math_exp MINUS math_exp")
@pg.production("math_exp : math_exp MULTIPLY math_exp")
@pg.production("math_exp : math_exp DIVIDE math_exp")
@pg.production("math_exp : math_exp MOD math_exp")
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

@pg.production("factor : PAREN_L math_exp PAREN_R")
def factor_parens(p):
	return p[1]

# Boolean expressions
@pg.production("boolean_expression : booleans")
def boolean_expression(p):
	return p[0]

@pg.production("booleans : bool_factor")
def booleans_to_boolean(p):
	return p[0]

@pg.production("booleans : booleans and bool_factor")
@pg.production("booleans : booleans or bool_factor")
def boolean_operations(p):
	token_type, left, right = p[1].gettokentype(), p[0], p[2]
	if token_type == "and":
		return ast.And(left, right)
	elif token_type == "or":
		return ast.Or(left, right)
	else:
		assert False, "Something went wrong"

@pg.production("bool_factor : bool_term")
def boolean_to_boolean_factor(p):
	return p[0]

@pg.production("bool_term : true")
@pg.production("bool_term : false")
def boolean(p):
	boolean = p[0]
	if boolean.gettokentype() == "true":
		return ast.Boolean(True)
	elif boolean.gettokentype() == "false":
		return ast.Boolean(False)
	else:
		assert False, "Something went wrong"

@pg.production("bool_term : not bool_term")
def not_boolean(p):
	return ast.Boolean(not p[1].value)

@pg.production("booleans : PAREN_L boolean_expression PAREN_R")
def paren_boolean(p):
	return p[1]

# Parenthesis precedence

# Implicit Printing
@pg.production("statement : PAREN_L math_exp PAREN_R")
def print_id(p):
	return ast.WriteStatement(p[1])

@pg.error
def error_handler(token):
    raise ValueError('Ran into a %s where it wasn\'t expected' % token)

parser = pg.build()

if __name__ == "__main__":
	from pprint import pprint
	from sys import argv
	with open(argv[1], "r") as f:
		p = parser.parse(lex(f.read()))
		# pprint(p.__dict__)
		pprint(p.eval({}))
		# pprint(p.body[0][0].value)
		# pprint(p.body[0][0].identifier.name)
		# pprint(p.__dict__)
		# pprint(p.eval({}))
		# print(p)
