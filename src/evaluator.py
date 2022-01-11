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
		self.set_context()

	def set_context(self, context=None):
		self.context = context
		return self
	
	def set_position(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self
	
	def added_to(self, other):
		# This language will have strings and arrays, so check
		# if the other is Number or not is necessary later
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
	
	def subtracted_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
	
	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
	
	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0: return None, RuntimeError(
				other.pos_start, other.pos_end, "Division by zero is not allowed", self.context
			)
			else:
				return Number(self.value / other.value), None

	def powered_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		
	def __repr__(self):
		return f"{self.value}"


class Evaluator:
	def visit(self, node, context):
		method_to_be_called = f"visit_{type(node).__name__}"
		method = getattr(self, method_to_be_called, self.no_visit_method)
		return method(node, context)
	
	def no_visit_method(self, node, context):
		raise Exception(f"No visit_{type(node).__name__} method defined.")
	
	def visit_VarAccessNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)
		if value is None: return res.failure(RuntimeError(
			node.pos_start, node.pos_end, f"var '{var_name}' is not defined", context
		))
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RuntimeError()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res
		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_NumberNode(self, node, context):
		return RuntimeResult().success(Number(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_BinOpNode(self, node, context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.error: return res
		right = res.register(self.visit(node.right_node, context))
		if res.error: return res
		# check the operator type
		if node.op_token.type == tk.TT_PLUS:
			result, err = left.added_to(right)
		elif node.op_token.type == tk.TT_MINUS:
			result, err = left.subtracted_by(right)
		elif node.op_token.type == tk.TT_MULT:
			result, err = left.multiplied_by(right)
		elif node.op_token.type == tk.TT_DIV:
			result, err = left.divided_by(right)
		elif node.op_token.type == tk.TT_POWER:
			result, err = left.powered_by(right)
		
		return res.failure(err) if err is not None else res.success(result.set_position(node.pos_start, node.pos_end))
	
	def visit_UnaryOpNode(self, node, context):
		res = RuntimeResult()
		num = res.register(self.visit(node.node, context))
		if res.error: return res
		err = None
		if node.op_token.type == tk.TT_MINUS:
			num, err = num.multiplied_by(Number(-1))

		return res.failure(err)	if err is not None else res.success(num.set_position(node.pos_start, node.pos_end))

