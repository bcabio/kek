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
	def __init__(self, name, value):


