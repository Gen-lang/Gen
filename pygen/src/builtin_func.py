from src.value import BaseFunction, Number, String
from src.evaluator import RuntimeResult

class BuiltinFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)
	
	def execute(self, args):
		res = RuntimeResult()
		context = self.generate_new_context()
		method = getattr(self, f"execute_{self.name}", self.no_visit_method)
		res.register(self.check_and_fill_args(method.arg_names, args, context))
		if res.error: return res
		return_value = res.register(method(context))
		if res.error: return res
		return res.success(return_value)

	def no_visit_method(self, node, context):
		raise Exception(f"execute_{self.name} is not defined")

	def copy(self):
		copy = BuiltinFunction(self.name)
		copy.set_context(self.context)
		copy.set_position(self.pos_start, self.pos_end)
		return copy
	
	def __repr__(self):
		return f"<built-in func {self.name}>"
	
	######################################
	######### BUILT-IN FUNCTIONS #########
	######################################

	def execute_println(self, context):
		"""
			print the value passed in with a new line at the end
		"""
		print(str(context.symbol_table.get("value")))
		return RuntimeResult().success(Number.null)
	execute_println.arg_names = ["value"]

	def execute_print(self, context):
		"""
			print the value passed in without a new line at the end
		"""
		print(str(context.symbol_table.get("value")), end="")
		return RuntimeResult().success(Number.null)
	execute_print.arg_names = ["value"]

	def execute_input(self, context):
		"""
			read a line from input, convert it to String, and return it
		"""
		text = str(context.symbol_table.get("text"))
		input_value = input(text)
		return RuntimeResult().success(String(input_value))
	execute_input.arg_names = ["text"]

	def execute_int_input(self, context):
		"""
			read a line from input, try to convert it to Number, and return it
		"""
		text = str(context.symbol_table.get("text"))
		input_value = input(text)
		while True:
			try:
				input_value = int(input_value)
				break
			except ValueError:
				print(f"Input value must be an integer.")
		return RuntimeResult().success(Number(input_value))
	execute_int_input.arg_names = ["text"]
