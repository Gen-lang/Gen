import src.gen_token as tk
from src.error import RuntimeError
from src.context import Context
from src.symbol_table import SymbolTable

class Value:
	def __init__(self):
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
		return None, self.invalid_operation(other)
	
	# make these invalid operations unless overriden by Number class
	def subtracted_by(self, other):
		return None, self.invalid_operation(other)
	
	def multiplied_by(self, other):
		return None, self.invalid_operation(other)
	
	def divided_by(self, other):
		return None, self.invalid_operation(other)

	def powered_by(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_equal(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_not_equal(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_less_than(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_greater_than(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_lt_equals(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_gt_equals(self, other):
		return None, self.invalid_operation(other)
	
	def and_by(self, other):
		return None, self.invalid_operation(other)
	
	def or_by(self, other):
		return None, self.invalid_operation(other)
	
	def notted(self):
		return None, self.invalid_operation()
	
	def is_true(self):
		return False
	
	def invalid_operation(self, other=None):
		if other is None: other = self
		return RuntimeError(
			self.pos_start, other.pos_end, "Invalid operation", self.context
		)
	
	def copy(self):
		pass
		
	def __repr__(self):
		return f"{self.value}"


class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	# make these invalid operations unless overriden by Number class
	def subtracted_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0: return None, RuntimeError(
				other.pos_start, other.pos_end, "Division by zero is not allowed", self.context
			)
			else:
				return Number(self.value / other.value), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)

	def powered_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_equal(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_not_equal(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_less_than(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_greater_than(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_lt_equals(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def get_comparison_gt_equals(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def and_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def or_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None
	
	def is_true(self):
		return self.value != 0
	
	def copy(self):
		copy = Number(self.value)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy


class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def multiplied_by(self, other): # allow "a" * 8
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.invalid_operation(self.pos_start, other.pos_end)
	
	def copy(self):
		copy = String(self.value)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy


class Function(Value):
	def __init__(self, name, body_node, arg_names):
		super().__init__()
		self.name = name if name is not None else "<unnamed>"
		self.body_node = body_node
		self.arg_names = arg_names
	
	def execute_func(self, args):
		res = RuntimeResult()
		evaluator = Evaluator()
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		# check the number of args are correct or not
		if len(args) > len(self.arg_names):
			return res.failure(RuntimeError(
				self.pos_start, self.pos_end, f"Too many arguments are passed to {self.name}", self.context
			))
		elif len(args) < len(self.arg_names):
			return res.failure(RuntimeError(
				self.pos_start, self.pos_end, f"Too few arguments are passed to {self.name}", self.context
			))
		else:
			for i in range(len(args)):
				arg_name = self.arg_names[i]
				arg_value = args[i]
				arg_value.set_context(new_context)
				new_context.symbol_table.set(arg_name, arg_value)
			value = res.register(evaluator.visit(self.body_node, new_context))
			if res.error: return res
			return res.success(value)
		
	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return f"<func {self.name}>"


# -------------------------------------------------------------------

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
		value = value.copy().set_position(node.pos_start, node.pos_end)
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res
		context.symbol_table.set(var_name, value)
		return res.success(value)
	
	def visit_IfNode(self, node, context):
		res = RuntimeResult()
		for condition, expression in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.error: return res
			if condition_value.is_true():
				expr_value = res.register(self.visit(expression, context))
				if res.error: return res
				return res.success(expr_value)
		if node.else_case is not None:
			else_value = res.register(self.visit(node.else_case, context))
			if res.error: return res
			return res.success(else_value)
		return res.success(None)

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
		elif node.op_token.type == tk.TT_DEQUALS:
			result, err = left.get_comparison_equal(right)
		elif node.op_token.type == tk.TT_NEQUALS:
			result, err = left.get_comparison_not_equal(right)
		elif node.op_token.type == tk.TT_LTHAN:
			result, err = left.get_comparison_less_than(right)
		elif node.op_token.type == tk.TT_GTHAN:
			result, err = left.get_comparison_greater_than(right)
		elif node.op_token.type == tk.TT_LTEQUALS:
			result, err = left.get_comparison_lt_equals(right)
		elif node.op_token.type == tk.TT_GTEQUALS:
			result, err = left.get_comparison_gt_equals(right)
		elif node.op_token.matches(tk.TT_KEYWORD, "and"):
			result, err = left.and_by(right)
		elif node.op_token.matches(tk.TT_KEYWORD, "or"):
			result, err = left.or_by(right)
		
		return res.failure(err) if err is not None else res.success(result.set_position(node.pos_start, node.pos_end))
	
	def visit_UnaryOpNode(self, node, context):
		res = RuntimeResult()
		num = res.register(self.visit(node.node, context))
		if res.error: return res
		err = None
		if node.op_token.type == tk.TT_MINUS:
			num, err = num.multiplied_by(Number(-1))
		elif node.op_token.matches(tk.TT_KEYWORD, "not"):
			num, err = num.notted()

		return res.failure(err)	if err is not None else res.success(num.set_position(node.pos_start, node.pos_end))

	def visit_ForNode(self, node, context):
		res = RuntimeResult()
		start_value = res.register(self.visit(node.start_value_node, context))
		if res.error: return res
		end_value = res.register(self.visit(node.end_value_node, context))
		if res.error: return res
		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.error: return res
		else:
			step_value = Number(1)
		sv = start_value.value
		if step_value.value >= 0:
			condition = lambda: sv < end_value.value
		else:
			condition = lambda: sv > end_value.value
		while condition():
			context.symbol_table.set(node.var_name_token.value, Number(sv))
			sv += step_value.value
			res.register(self.visit(node.body_node, context))
			if res.error: return res
		return res.success(None)
	
	def visit_WhileNode(self, node, context):
		res = RuntimeResult()
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.error: return res
			if condition.is_true() is False: break
			res.register(self.visit(node.body_node, context))
			if res.error: return res
		return res.success(None)
	
	def visit_FuncDefNode(self, node, context):
		res = RuntimeResult()
		func_name = node.var_name_token.value if node.var_name_token is not None else None
		body_node = node.body_node
		arg_names = [arg.value for arg in node.arg_name_tokens]
		func_value = Function(func_name, body_node, arg_names).set_context(context).set_position(node.pos_start, node.pos_end)
		if node.var_name_token is not None:
			context.symbol_table.set(func_name, func_value)
		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RuntimeResult()
		args = []
		called_value = res.register(self.visit(node.node_to_call, context))
		if res.error: return res
		called_value = called_value.copy().set_position(node.pos_start, node.pos_end)
		for argnode in node.arg_nodes:
			args.append(res.register(self.visit(argnode, context)))
			if res.error: return res
		
		return_value = res.register(called_value.execute_func(args))
		if res.error: return res
		return res.success(return_value)
	
	def visit_StringNode(self, node, context):
		return RuntimeResult().success(String(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))
