from src.error import RuntimeError
from src.context import Context
from src.symbol_table import SymbolTable
from src.evaluator import Evaluator, RuntimeResult

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

	def at(self, other):
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
	
	# make these invalid operations unless overriden
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
	
	def is_true(self):
		return len(self.value) > 0
	
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


class Array(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements
	
	def added_to(self, other):
		new_array = self.copy()
		if isinstance(other, Array):
			new_array.elements.extend(other.elements)
		else:
			new_array.elements.append(other)
		return new_array, None
	
	def subtracted_by(self, other):
		if isinstance(other, Number):
			new_array = self.copy()
			try:
				new_array.elements.pop(other.value)
				return new_array, None
			except IndexError:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at index {other.value} does not exist"
				)
		else:
			return Value.invalid_operation(self, other)

	def at(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at index {other.value} does not exist"
				)
		else:
			return Value.invalid_operation(self, other)

	def copy(self):
		copy = Array(self.elements[:])
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		string = "[" + ', '.join([str(i) for i in self.elements]) + "]"
		return string
	