import gen_token as tk
from error import RuntimeError

class RuntimeResult:
	def __init__(self):
		self.value = None
		self.error = None
	
	def register(self, result):
		if result.error: self.error = result.error
		return result.value
	
	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self


class Number:
	def __init__(self, value):
		self.value = value
		self.set_position()
	
	def set_position(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self
	
	def added_to(self, other):
		# This language will have strings and arrays, so check
		# if the other is Number or not is necessary later
		if isinstance(other, Number):
			return Number(self.value + other.value), None
	
	def subtracted_by(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value), None
	
	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value), None
	
	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0: return None, RuntimeError(
				other.pos_start, other.pos_end, "Division by zero is not allowed"
			)
			else:
				return Number(self.value / other.value), None
		
	def __repr__(self):
		return f"{self.value}"


class Evaluator:
	def visit(self, node):
		method_to_be_called = f"visit_{type(node).__name__}"
		method = getattr(self, method_to_be_called, self.no_visit_method)
		return method(node)
	
	def no_visit_method(self, node):
		raise Exception(f"No visit_{type(node).__name__} method defined.")

	def visit_NumberNode(self, node):
		return RuntimeResult().success(Number(node.token.value).set_position(node.pos_start, node.pos_end))
	
	def visit_BinOpNode(self, node):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node))
		if res.error: return res
		right = self.visit(node.right_node)
		# check the operator type
		if node.op_token.type == tk.TT_PLUS:
			result, err = left.added_to(right)
		elif node.op_token.type == tk.TT_MINUS:
			result, err = left.subtracted_by(right)
		elif node.op_token.type == tk.TT_MULT:
			result, err = left.multiplied_by(right)
		elif node.op_token.type == tk.TT_DIV:
			result, err = left.divided_by(right)
		
		return res.failure(err) if err is not None else res.success(result.set_position(node.pos_start, node.pos_end))
	
	def visit_UnaryOpNode(self, node):
		res = RuntimeResult()
		num = res.register(self.visit(node.node))
		if res.error: return res
		err = None
		if node.op_token.type == tk.TT_MINUS:
			num, err = num.multiplied_by(Number(-1))

		return res.failure(err)	if err is not None else res.success(num.set_position(node.pos_start, node.pos_end))

