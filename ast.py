import sys

from exceptions import *

try:
	raw_input
except:
	raw_input = input

# Root Class
class ASTNode(object):
	def eval(self, context):
		raise NotImplementedError(self.__class__)

# Types
class Number(ASTNode):
	def __init__(self, value):
		self.value = value

	def eval(self, context):
		return self.value

class Boolean(ASTNode):
	def __init__(self, value):
		self.value = value

	def eval(self, context):
		return self.value

class String(ASTNode):
	def __init__(self, value):
		self.value = value

	def eval(self, context):
		return self.value

# Placeholders
class Identifier(ASTNode):
	def __init__(self, value, name=None):
		self.name = name
		self.value = value

class IdentifierReference(ASTNode):
	def __init__(self, name):
		self.name = name

	def eval(self, context):
		return context[self.name]

class Block(ASTNode):
	def __init__(self, body):
		self.body = body

	def eval(self, context):
		for instruction in self.body[0]:
			instruction.eval(context)

class Assignment(ASTNode):
	def __init__(self, identifier, value):
		self.identifier = identifier
		self.value = value

	def eval(self, context):
		context[self.identifier.name] = self.value.eval(context)

# Number
class BinaryOperation(ASTNode):
	def __init__(self, left, right):
		self.left = left
		self.right = right

class Add(BinaryOperation):
	def eval(self, context):
		return self.left.eval(context) + self.right.eval(context)

class Subtract(BinaryOperation):
	def eval(self, context):
		return self.left.eval(context) - self.right.eval(context)

class Multiply(BinaryOperation):
	def eval(self, context):
		return self.left.eval(context) * self.right.eval(context)

class Divide(BinaryOperation):
	def eval(self, context):
		return self.left.eval(context) / self.right.eval(context)

class Modulus(BinaryOperation):
	def eval(self, context):
		return self.left.eval(context) % self.right.eval(context)


# Boolean
class BooleanOperation(ASTNode):
	def __init__(self, left, right):
		self.left = left
		self.right = right

class And(BooleanOperation):
	def eval(self, context):
		return self.left.eval(context) and self.right.eval(context)

class Or(BooleanOperation):
	def eval(self, context):
		return self.left.eval(context) or self.right.eval(context)

# Functions
class FunctionDeclaration(ASTNode):
	def __init__(self, function_id, function_param_names, function_body):
		self.function_id = function_id
		self.function_param_names = function_param_names
		self.function_body = function_body

	def eval(self, context):
		if self.function_id in context:
			raise FunctionAlreadyDeclaredException(self.function_id)
		context[self.function_id] = [self.function_param_names, self.function_body]

class FunctionBody(ASTNode):
	def __init__(self, function_body):
		self.function_body = function_body

class FunctionCall(ASTNode):
	def __init__(self, function_id, function_param_values):
		self.function_id = function_id
		self.function_param_values = function_param_values

	def eval(self, context):
		if self.function_id not in context:
			raise FunctionNotDeclaredException(self.function_id)

		# Names of the parameters given by function declaration
		param_names = context[self.function_id][0]
		function_body = context[self.function_id][1].function_body
		# Dict to save variables that are overridden by the internal 
		saved_outside_scope_variables = dict()

		# Iterate over param name value pairs
		# and if they're to be overridden, save them
		# then over write them
		for param_name, param_value in zip(param_names, self.function_param_values):
			if param_name in context:
				saved_outside_scope_variables[param_name] = context[param_name] 
			context[param_name] = param_value.eval(context) 			
		
		# Execute the function body
		for instruction in function_body:
			instruction.eval(context)

		# Delete the function parameters from the context
		for param_name in param_names:
			if param_name in saved_outside_scope_variables:
				continue
			elif param_name in context:
				del context[param_name]

		# Add the saved variables back to the context
		for saved_var in saved_outside_scope_variables:
			context[saved_var] = saved_outside_scope_variables[saved_var]


class ReadStatement(ASTNode):
	def __init__(self, target):
		self.target = target

	def eval(self, context):
		assert self.target.name in context
		context[self.target.name] = (
			Number(raw_input("Value for %s: " % self.target.name))
			.eval(context))

class WriteStatement(ASTNode):
	def __init__(self, value, newline=True):
		self.value = value
		self.newline = newline

	def eval(self, context):
		sys.stdout.write(str(self.value.eval(context)) + ("\n" if self.newline else ""))
