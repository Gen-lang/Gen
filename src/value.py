from error import RuntimeError

class Value:
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
		super().__init__(value)
	
	def added_to(self, other):
		# This language will have strings and arrays, so check
		# if the other is Number or not is necessary later
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

