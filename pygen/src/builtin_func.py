from src.value import *
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
		print(str(context.symbol_table.get("value")), end="")
		return RuntimeResult().success(Number.null)
	execute_print.arg_names = ["value"]

	def execute_input(self, context):
		"""
			read a line from input, convert it to String, and return it
			example: value = input("Enter your name: ")
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
		"""
		text = str(context.symbol_table.get("text"))
		error_text = "Input value must be an integer."
		while True:
			input_value = input(text)
			try:
				input_value = int(input_value)
				break
			except ValueError:
				print(error_text)
		return RuntimeResult().success(Number(input_value))
	execute_int_input.arg_names = ["text"]

	def execute_absolute_number_of(self, context):
		"""
			try to return the absolute number of the value passed in
			example: abs_num = absolute_number_of(-9)
		"""
		value = context.symbol_table.get("value")
		try:
			value = int(context.symbol_table.get("value").value)
		except ValueError:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value} does not have an absolute number"
			))
		return RuntimeResult().success(Number(abs(value)))
	execute_absolute_number_of.arg_names = ["value"]

	def execute_is_number(self, context):
		"""
			check if the value passed in is a number
			example: is_number(3)
		"""
		value = context.symbol_table.get("value")
		is_number = isinstance(value, Number)
		return RuntimeResult().success(Number.true if is_number is True else Number.false)
	execute_is_number.arg_names = ["value"]

	def execute_is_string(self, context):
		"""
			check if the value passed in is a string
			example: is_string("Hello World")
		"""
		value = context.symbol_table.get("value")
		is_string = isinstance(value, String)
		return RuntimeResult().success(Number.true if is_string is True else Number.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_array(self, context):
		"""
			check if the value passed in is an array
			example: is_array([1, 2, 3])
		"""
		value = context.symbol_table.get("value")
		is_array = isinstance(value, Array)
		return RuntimeResult().success(Number.true if is_array is True else Number.false)
	execute_is_array.arg_names = ["value"]

	def execute_is_function(self, context):
		"""
			check if the value passed in is a function
			example: is_function(some_func)
		"""
		value = context.symbol_table.get("value")
		is_function = isinstance(value, BaseFunction)
		return RuntimeResult().success(Number.true if is_function is True else Number.false)
	execute_is_function.arg_names = ["value"]

	def execute_exit_program(self, context):
		"""
			exit the program
			example: exit_program()
		"""
		print("Bye bye!")
		exit()
	execute_exit_program.arg_names = []

	def execute_size(self, context):
		"""
			return the size of the value
			example: size([1, 2, 3])
		"""
		value = context.symbol_table.get("value")
		if isinstance(value, Number):
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, "The argument should be string or array", context
			))
		else:
			return RuntimeResult().success(Number(len(value.elements) if isinstance(value, Array) else len(value.value)))
	execute_size.arg_names = ["value"]



BuiltinFunction.println 			= BuiltinFunction("println")
BuiltinFunction.print	 			= BuiltinFunction("print")
BuiltinFunction.input	 			= BuiltinFunction("input")
BuiltinFunction.int_input			= BuiltinFunction("int_input")
BuiltinFunction.absolute_number_of	= BuiltinFunction("absolute_number_of")
BuiltinFunction.is_number			= BuiltinFunction("is_number")
BuiltinFunction.Pi					= BuiltinFunction("Pi")
BuiltinFunction.is_string			= BuiltinFunction("is_string")
BuiltinFunction.is_array			= BuiltinFunction("is_array")
BuiltinFunction.is_function			= BuiltinFunction("is_function")
BuiltinFunction.exit_program		= BuiltinFunction("exit_program")
BuiltinFunction.size				= BuiltinFunction("size")