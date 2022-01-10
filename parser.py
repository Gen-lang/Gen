import gen_token as tk
from error import InvalidSyntaxError

class NumberNode:
	def __init__(self, token):
		self.token = token
		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end

	def __repr__(self):
		return f"{self.token}"


class BinOpNode:
	def __init__(self, left_node, op_token, right_node):
		self.left_node = left_node
		self.op_token = op_token
		self.right_node = right_node
		
		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end
	
	def __repr__(self):
		return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
	def __init__(self, op_token, node):
		self.op_token = op_token
		self.node = node
		self.pos_start = self.op_token.pos_start
		self.pos_end = self.node.pos_end
	
	def __repr__(self):
		return f"({self.op_token}, {self.node})"


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

		if token.type in (tk.TT_PLUS,  tk.TT_MINUS):
			res.register(self.advance())
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(token, factor))
		elif token.type in (tk.TT_INT, tk.TT_FLOAT):
			res.register(self.advance()) # it does nothing for now.
			return res.success(NumberNode(token))
		elif token.type == tk.TT_L_PAREN:
			res.register(self.advance())
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_token.type == tk.TT_R_PAREN:
				res.register(self.advance())
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected a ')'"
				))
		return res.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end, "Expected INT or FLOAT"
		))

	def term(self):
		return self.bin_op(self.factor, (tk.TT_MULT, tk.TT_DIV))
	
	def expr(self):
		return self.bin_op(self.term, (tk.TT_PLUS, tk.TT_MINUS))
	
	def bin_op(self, func, ops):
		res = ParseResult()
		left = res.register(func())
		if res.error: return res
		while self.current_token.type in ops:
			op_token = self.current_token
			res.register(self.advance())
			right = res.register(func())
			if res.error: return res
			left = BinOpNode(left, op_token, right)
		return res.success(left)
	
	def parse(self):
		result = self.expr()
		if not result.error and self.current_token.type != tk.TT_EOF:
			return result.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected +, -, *, or /"
			))
		return result


class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
	
	def register(self, result):
		if isinstance(result, ParseResult):
			if result.error: self.error = result.error
			return result.node
		return result
	
	def success(self, node):
		self.node = node
		return self
	
	def failure(self, error):
		self.error = error
		return self