class FunctionNotDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {} not declared".format(func_name))

class FunctionAlreadyDeclaredException(Exception):
	def __init__(self, func_name):
		Exception.__init__(self, "Function {} already declared".format(func_name))

class MissingAttribute(Exception):
	def __init__(self, object, attribute):
		Exception.__init__(self, "Object {} does not have attribute {}".format(object, attribute))