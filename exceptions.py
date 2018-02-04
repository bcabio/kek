class FunctionNotDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {0} not declared".format(func_name))

class FunctionAlreadyDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {} already declared".format(func_name))