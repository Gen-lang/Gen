from token import TokenType, Token

# for checking if a character is a digit or not
DIGITS = "0123456789"

class Lexer:
	def __init__(self, text):
		self.text = text
		self.position = -1
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.position += 1
		self.current_char = self.text[self.position] if self.position < len(self.text) else None
	
	def make_tokens(self):
		tokens = []

		while self.current_char is not None:
			if self.current_char in " \t": # ignore tabs and spaces
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char == "+":
				tokens.append(TokenType.PLUS)
				self.advance()
			elif self.current_char == "*":
				tokens.append(TokenType.MULT)
				self.advance()
			elif self.current_char == "/":
				tokens.append(TokenType.DIV)
				self.advance()
			elif self.current_char == "(":
				tokens.append(TokenType.L_PAREN)
				self.advance()
			elif self.current_char == ")":
				tokens.append(TokenType.R_PAREN)
				self.advance()
			else:
				# return some error
				pass
		return tokens
	
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
		
		return Token(TokenType.INT, int(number_str)) if dot is False else Token(TokenType.FLOAT, float(number_str))
