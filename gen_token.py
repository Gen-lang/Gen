
TT_INT	 		= "INT"
TT_FLOAT 		= "FLOAT"
TT_PLUS			= "PLUS"
TT_MINUS		= "MINUS"
TT_MULT			= "MULT"
TT_DIV			= "DIV"
TT_POWER		= "POWER"
TT_L_PAREN		= "L_PAREN"
TT_R_PAREN		= "R_PAREN"
TT_IDENTIFIER	= "IDENTIFIER"
TT_KEYWORD 		= "KEYWORD"
TT_EQUALS		= "EQUALS"
TT_EOF			= "EOF"

KEYWORDS = [
	"var"
]

class Token:
	def __init__(self, type, value=None, pos_start=None, pos_end=None):
		self.type = type
		self.value = value
		if pos_start is not None:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()
	
	def __repr__(self):
		return f"{self.type}:{self.value}" if self.value is not None else self.type