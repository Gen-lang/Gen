from src.utils import string_with_arrows

class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details

	def __str__(self):
		string = f"File {self.pos_start.filename}, line {self.pos_start.lnum+1}\n"
		string += f"Gen::{self.error_name}: {self.details}"
		string += f"\n\n" + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
		return string


class TypeCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, "TypeCharError", details)


class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=""):
		super().__init__(pos_start, pos_end, "InvalidSyntaxError", details)


class RuntimeError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, "RuntimeError", details)
		self.context = context

	def __str__(self):
		string = self.generate_traceback()
		string += f"Gen::{self.error_name}: {self.details}"
		string += f"\n\n" + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
		return string
	
	def generate_traceback(self):
		result = ""
		position = self.pos_start
		context = self.context
		while context:
			result = f"	File {position.filename}, line {position.lnum+1}, in {context.display_name}\n" + result
			position = context.parent_entry_pos
			context = context.parent
		
		return "Traceback (most recent call last):\n" + result
