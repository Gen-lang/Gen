import token as tk
from error import InvalidSyntaxError

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
		self.current_token = None
		self.advance()
	
	def advance(self):
		self.token_index += 1
		if self.token_index < len(self.tokens):
			self.current_token = self.tokens[self.token_index]
		return self.current_token
	
	def factor(self):
		res = ParseResult()
		token = self.current_token
		if token.type in (tk.TT_INT, tk.TT_FLOAT):
			res.register(self.advance()) # it does nothing for now.
			return res.success(NumberNode(token))
		return res.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end, f"Expected INT or FLOAT"
		))

	def term(self):
		return self.bin_op(self.factor, (tk.TT_MULT, tk.TT_DIV))
	
	def expr(self):
		return self.bin_op(self.term, (tk.TT_PLUS, tk.TT_MINUS))
	
	def bin_op(self, func, ops):
		res = ParseResult()
		left = res.register(func())
		if res.error: return res
		while self.current_token in ops:
			op_token = self.current_token
			res.register(self.advance())
			right = res.register(func())
			if res.error: return res
			left = BinOpNode(left, op_token, right)
		return res.success(left)
	
	def parse(self):
		result = self.expr()
		return result


class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
	
	def register(self, result):
		if isinstance(result, ParseResult):
			self.error = result.error if result.error else None
			return result.node
		return result
	
	def success(self, node):
		self.node = node
		return
	
	def failure(self, error):
		self.error = error
		return