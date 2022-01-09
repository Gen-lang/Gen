class Error:
	def __init__(self, error_name, details):
		self.error_name = error_name
		self.details = details
	
	@property
	def as_string(self):
		return f"Gen::{self.error_name}: {self.details}"

class TypeCharError(Error):
	def __init__(self, details):
		super().__init__("TypeCharError", details)