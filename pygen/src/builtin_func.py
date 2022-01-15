from src.value import BaseFunction, Number, String
from src.evaluator import RuntimeResult, RuntimeError

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
			example: println("Hello World")
		"""
		# add try-except later
		print(str(context.symbol_table.get("value")))
		return RuntimeResult().success(Number.null)
	execute_println.arg_names = ["value"]

	def execute_print(self, context):
		"""
			print the value passed in without a new line at the end
			example: print("Hello World!")
		"""
		# add try-except later
		print(str(context.symbol_table.get("value")), end="")
		return RuntimeResult().success(Number.null)
	execute_print.arg_names = ["value"]

	def execute_input(self, context):
		"""
			read a line from input, convert it to String, and return it
			example 1: value = input("Enter your name: ")
			example 2: value = input()
		"""
		text = ""
		try:
			text = str(context.symbol_table.get("text"))
		except:
			pass
		input_value = input(text)
		return RuntimeResult().success(String(input_value))
	execute_input.arg_names = ["text"]

	def execute_int_input(self, context):
		"""
			read a line from input, try to convert it to Number, and return it
			example 1: value = int_input("Enter a value: ")
			example 2: value = int_input("Enter something: ", "Please enter an integer.")
		"""
		text = ""
		try:
			text = str(context.symbol_table.get("text"))
		except:
			return RuntimeResult().RuntimeError(
				self.pos_start, self.pos_end, "'int_input' needs at least one argument"
			)
		error_text = "Input value must be an integer."
		try:
			error_text = str(context.symbol_table.get("error_text"))
		except:
			pass
		input_value = input(text)
		while True:
			try:
				input_value = int(input_value)
				break
			except ValueError:
				print(error_text)
		return RuntimeResult().success(Number(input_value))
	execute_int_input.arg_names = ["text", "error_text"]

	def execute_absolute_number_of(self, context):
		"""
			try to return the absolute number of the value passed in
			example: abs_num = absolute_number_of(-9)
		"""
		# add try-except later
		value = context.symbol_table.get("value")
		try:
			value = int(context.symbol_table.get("value"))
		except ValueError:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value} does not have an absolute number"
			))
		return RuntimeResult().success(Number(abs(value)))
	execute_absolute_number_of.arg_names = ["value"]

	def execute_is_number(self, context):
		"""
			check if the value passed in is a number
		"""
		try:
			value = context.symbol_table.get("value")
		except:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"'is_number' needs at least one argument"
			))
		is_number = int(isinstance(value, Number))
		return RuntimeResult().success(Number(is_number))
	execute_is_number.arg_names = ["value"]

		