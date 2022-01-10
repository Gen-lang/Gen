
TT_INT	 	= "INT"
TT_FLOAT 	= "FLOAT"
TT_PLUS		= "PLUS"
TT_MINUS	= "MINUS"
TT_MULT		= "MULT"
TT_DIV		= "DIV"
TT_L_PAREN	= "L_PAREN"
TT_R_PAREN	= "R_PAREN"


class Token:
	def __init__(self, type, value=None):
		self.type = type
		self.value = value
	
	def __repr__(self):
		return f"{self.type}:{self.value}" if self.value is not None else self.type