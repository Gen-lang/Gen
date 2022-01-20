class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent
	
	def get(self, var_name):
		value = self.symbols.get(var_name, None)
		return self.parent.get(var_name) if value is None and self.parent else value
	
	def set(self, var_name, value):
		self.symbols[var_name] = value
	
	def set_arr_or_map(self, var_name, key_or_index, value):
		self.symbols[var_name][key_or_index] = value
	
	def remove(self, var_name):
		del self.symbols[var_name]