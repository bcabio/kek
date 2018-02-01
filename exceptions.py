class FunctionNotDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {0} not declared", func_name)

class FunctionAlreadyDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {0} already declared", func_name)