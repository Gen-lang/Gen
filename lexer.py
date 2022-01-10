from token import *
from error import TypeCharError
from position import Position

# for checking if a character is a digit or not
DIGITS = "0123456789"

class Lexer:
	def __init__(self, filename, text):
		self.filename = filename
		self.text = text
		self.position = Position(-1, 0, -1, self.filename, self.text)
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.position.advance(self.current_char)
		self.current_char = self.text[self.position.index] if self.position.index < len(self.text) else None
	
	def make_tokens(self):
		tokens = []

		while self.current_char is not None:
			if self.current_char in " \t": # ignore tabs and spaces
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char == "+":
				tokens.append(TT_PLUS)
				self.advance()
			elif self.current_char == "*":
				tokens.append(TT_MULT)
				self.advance()
			elif self.current_char == "/":
				tokens.append(TT_DIV)
				self.advance()
			elif self.current_char == "(":
				tokens.append(TT_L_PAREN)
				self.advance()
			elif self.current_char == ")":
				tokens.append(TT_R_PAREN)
				self.advance()
			else:
				# return TypeCharError
				pos_start = self.position.copy()
				char = self.current_char
				self.advance()
				return [], TypeCharError(pos_start, self.position, f"'{char}'")
		return tokens, None
	
	def make_number(self):
		number_str = ""
		dot = False
		while self.current_char is not None and self.current_char in DIGITS + ".":
			if self.current_char == ".":
				if dot is True: break
				dot = True
				number_str += self.current_char
			else:
				number_str += self.current_char
			self.advance()
		
		return Token(TT_INT, int(number_str)) if dot is False else Token(TT_FLOAT, float(number_str))
