class Evaluator:
	def visit(self, node):
		method_to_be_called = f"visit_{type(node).__name__}"
		method = getattr(self, method_to_be_called, self.no_visit_method)
		return method(node)
	
	def no_visit_method(self, node):
		raise Exception(f"No visit_{type(node).__name__} method defined.")

	def visit_NumberNode(self, node):
		pass
	
	def visit_BinOpNode(self, node):
		pass
	
	def visit_UnaryOpNode(self, node):
		pass

