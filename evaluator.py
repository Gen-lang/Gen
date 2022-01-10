class Evaluator:
	def visit(self, node):
		method_to_be_called = f"visit_{type(node).__name__}"
		method = getattr(self, method_to_be_called, self.no_visit_method)
		return method(node)
	
	def no_visit_method(self, node):
		raise Exception(f"No visit_{type(node).__name__} method defined.")

	def visit_NumberNode(self, node):
		print("number node")
	
	def visit_BinOpNode(self, node):
		print("binary operator")
		self.visit(node.left_node)
		self.visit(node.right_node)
	
	def visit_UnaryOpNode(self, node):
		print("unray operator")
		self.visit(node.node)

