from rply import ParserGenerator

from lexer import token_names, lex
import ast


pg = ParserGenerator(
	token_names,
	precedence=[
		('left', ['AND', 'OR']),
		('left', ['NOT',]),
		('left', ['PLUS', 'MINUS']),
		('left', ['MULTIPLY', 'DIVIDE', ]),
		# ('left', ['PAREN_L, PAREN_R'])
	])

# Whole program
@pg.production("program : statements")
def program(p):
	return ast.Block(p)

@pg.production("statements : statement")
def statementlist_statement(p):
	return [p[0]]

@pg.production("statements : statements statement")
def statementlist_statementliststatement(p):
	return p[0] + [p[1]]

@pg.production("statement : ID kek assignment")
def assign(p):
	assert p[0].gettokentype() == "ID"
	return ast.Assignment(ast.IdentifierReference(p[0].getstr()), p[2])

@pg.production("assignment : exp")
def assignment_exp(p):
	return p[0]



"""
	EXPRESSION DEFINITION
"""	
@pg.production("exp : math_exp")
def math_expression(p):
	return p[0]

@pg.production("exp : boolean_exp")
def boolean_expression(p):
	return p[0]

@pg.production("exp : string_exp")
def string_expression(p):
	return p[0]




"""
	NUMERIC EXPRESSION DEFINITION
"""
@pg.production("math_exp : term")
def exp_term(p):
    return p[0]

@pg.production("math_exp : math_exp PLUS term ")
@pg.production("math_exp : math_exp MINUS term")
@pg.production("math_exp : math_exp MULTIPLY term")
@pg.production("math_exp : math_exp DIVIDE term")
@pg.production("math_exp : math_exp MOD term")
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



"""
	BOOLEAN EXPRESSIONS
"""	
@pg.production("boolean_exp : booleans")
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

@pg.production("bool_term : PAREN_L booleans PAREN_R")
def paren_boolean(p):
	return p[1]



"""
	STRING EPRESSIONS
"""
@pg.production("string_exp : ID ")
@pg.production("string_exp : STRING")
@pg.production("string_exp : string_exp BRACKET_L NUM COMMA NUM BRACKET_R")
def string_exp_to_string(p):
	token_type = p[0].gettokentype()
	
	if token_type == "ID":
		return ast.IdentifierReference(p[0].getstr())
	# FIX. String has no prop gettokentype
	elif token_type == "STRING":
		return ast.String(p[0].getstr()[1:-1])
	elif token_type == "string_exp":
		return ast.String(p[0].getstr()[1 + int(p[2].value) : 1 + int(p[4].value)])

"""
	FUNCTION DECLARATION
"""	
@pg.production("statement : func_dec")
def function_dec(p):
	return p[0]

@pg.production("func_dec : lol function_name PAREN_L func_params PAREN_R CURLY_L func_body CURLY_R")
def function_dec_syn(p):
	return ast.FunctionDeclaration(p[1].value, p[3], p[6])

@pg.production("func_dec : lol function_name PAREN_L func_params PAREN_R CURLY_L CURLY_R")
def function_dec_empty(p):
	return ast.FunctionDeclaration(p[1].value, p[3], [])

@pg.production("func_params : func_params COMMA func_param")
def function_params(p):
	return [p[0]] + [p[2].value]

@pg.production("func_params : func_param")
def function_param(p):
	return p[0].value

@pg.production("func_param : ID")
def func_param(p):
	return p[0]

@pg.production("function_name : ID")
def function_name(p):
	return p[0]

@pg.production("func_body : statements")
def func_body(p):
	return ast.FunctionBody(p[0])



"""
	FUNCTION EXECUTION
"""
@pg.production("statement : func_call")
def function_call(p):
	return p[0]

@pg.production("func_call : function_name PAREN_L func_call_params PAREN_R")
def function_call_syn(p):
	return ast.FunctionCall(p[0].value, p[2])

@pg.production("func_call_params : func_call_params COMMA func_call_param")
def func_call_params(p):
	return [p[0]] + [p[2]]

@pg.production("func_call_params : func_call_param")
def func_call_param(p):
	return p[0]

@pg.production("func_call_param : exp")
def func_call_param_type(p):
	return p[0]



"""
	PRINTING (TO BE CHANGED)
"""
@pg.production("statement : PAREN_L math_exp PAREN_R")
def print_id(p):
	return ast.WriteStatement(p[1])



"""
	GENERIC PG ERROR HANDLING
"""
@pg.error
def error_handler(token):
    raise ValueError('Ran into a %s where it wasn\'t expected' % token)

parser = pg.build()

if __name__ == "__main__":
	from pprint import pprint
	from sys import argv
	with open(argv[1], "r") as f:
		p = parser.parse(lex(f.read()))

		(p.eval({}))
	