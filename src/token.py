from enum import Enum

class TokenType(Enum):
	INT 	= "INT"
	FLOAT 	= "FLOAT"
	PLUS	= "PLUS"
	MINUS	= "MINUS"
	MULT	= "MULT"
	DIV		= "DIV"
	L_PAREN	= "L_PAREN"
	R_PAREN	= "R_PAREN"


class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __repr__(self):
		return f"{self.type}:{self.value}" if self.value is not None else self.type