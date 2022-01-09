from token import Token, TokenType

class NumberNode:
	def __init__(self, token):
		self.token = token

	def __repr__(self):
		return f"{self.token}"


class BinOpNode:
	def __init__(self, left_node, op_token, right_node):
		self.left_node = left_node
		self.op_token = op_token
		self.right_node = right_node
	
	def __repr__(self):
		return f"({self.left_node}, {self.op_token}, {self.right_node})"


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.advance()
	
	def advance(self):
		self.token_index += 1
		if self.token_index < len(self.tokens):
			self.current_token = self.tokens[self.token_index]
		return self.current_token
	
	def factor(self):
		token = self.current_token
		if token.type in (TokenType.INT, TokenType.FLOAT):
			self.advance()
			return NumberNode(token)

	def term(self):
		return self.bin_op_node(self.factor, (TokenType.MULT, TokenType.DIV))
	
	def expr(self):
		return self.bin_op_node(self.term, (TokenType.PLUS, TokenType.MINUS))
	
	def bin_op_node(self, func, ops):
		left = func()
		while  self.current_token in ops:
			op_token = self.current_token
			right = func()
			# self.advance()
			left = BinOpNode(left, op_token, right)
		return left
	
	def parse(self):
		result = self.expr()
		return result