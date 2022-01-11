class Position:
	def __init__(self, index, lnum, col, filename, filetext):
		self.index = index
		self.lnum = lnum
		self.col = col
		self.filename = filename
		self.filetext = filetext
	
	def advance(self, current_char=None):
		self.index += 1
		self.col += 1
		
		if current_char == "\n":
			self.lnum += 1
			self.col = 0
	
	def copy(self):
		return Position(self.index, self.lnum, self.col, self.filename, self.filetext)