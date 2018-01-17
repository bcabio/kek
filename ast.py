import sys

try:
	raw_input
except:
	raw_input = input

class ASTNode(object):
	def eval(self, context):
		raise NotImplementedError(self.__class__)

class Number(ASTNode):
	def __init__(self, value):
		self.value = value

	def eval(self, context):
		return self.value

class Identifier(ASTNode):
	def __init__(self, value, name=None):
		self.name = name
		self.value = value

class IdentifierReference(ASTNode):
	def __init__(self, name):
		self.name = name

	def eval(self, context):
		return context[self.name]

class Program(ASTNode):
	def __init__(self, name, decls, body):
		self.name = name
		self.decls = decls
		self.body = body

	def eval(self, context):
		for identifier in self.decls:
			context[identifier.name] = identifier.value
		for instruction in self.body:
			print(instruction)
			instruction.eval(context)
		for identifier in self.decls:
			if context[identifier.name] is None:
				print("Warning: identifier %s not used." % identifier.name)

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

class Assignment(ASTNode):
	def __init__(self, identifier, value):
		self.identifier = identifier
		self.value = value

	def eval(self, context):
		assert self.identifier in context
		context[self.identifier.name] = self.value.eval(context)

class ReadStatement(ASTNode):
	def __init__(self, target):
		self.target = target

	def eval(self, context):
		assert self.target.name in context
		context[self.target.name] = (
			Number(raw_input("Value for %s: " % self.target.name))
			.eval(context))

class WriteStatement(ASTNode):
	def __init__(self, value, newline=False):
		self.value = value
		self.newline = newline

	def eval(self, context):
		sys.stdout.write(str(self.value.eval(context)) + ("\n" if self.newline else ""))
