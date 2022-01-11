import src.gen_token as tk
from src.error import InvalidSyntaxError
from src.node import NumberNode, BinOpNode, UnaryOpNode, VarAccessNode, VarAssignNode

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

	def atom(self):
		res = ParseResult()
		token = self.current_token

		if token.type in (tk.TT_INT, tk.TT_FLOAT):
			res.register_advance()
			self.advance()
			return res.success(NumberNode(token))
		elif token.type == tk.TT_IDENTIFIER:
			res.register_advance()
			self.advance()
			return res.success(VarAccessNode(token))
		elif token.type == tk.TT_L_PAREN:
			res.register_advance()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_token.type == tk.TT_R_PAREN:
				res.register_advance()
				self.advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"
				))
		else:
			return res.failure(InvalidSyntaxError(
				token.pos_start, token.pos_end, "Expected an INT, FLOAT, identifier, +, -, or '('"
			))

	def power(self):
		return self.bin_op(self.atom, (tk.TT_POWER,), self.factor)
	
	def factor(self):
		res = ParseResult()
		token = self.current_token

		if token.type in (tk.TT_PLUS,  tk.TT_MINUS):
			res.register_advance()
			self.advance()
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(token, factor))

		return self.power()

	def term(self):
		return self.bin_op(self.factor, (tk.TT_MULT, tk.TT_DIV))
	
	def expr(self):
		res = ParseResult()
		# checking for a variable assignment
		if self.current_token.matches(tk.TT_KEYWORD, "var"):
			res.register_advance()
			self.advance()
			if self.current_token.type != tk.TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected an identifier"
				))
			var_name = self.current_token
			res.register_advance()
			self.advance()
			if self.current_token.type != tk.TT_EQUALS:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected an '='"
				))
			res.register_advance()
			self.advance()
			expression = res.register(self.expr())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expression))

		node = res.register(self.bin_op(self.comp_expr, ((tk.TT_KEYWORD, "and"), (tk.TT_KEYWORD, "or"))))
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'var', INT, FLOAT, identifier, +, -, or '('"
			))
		return res.success(node)
	
	def bin_op(self, func_a, ops, func_b=None):
		if func_b is None:
			func_b = func_a
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res
		while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
			op_token = self.current_token
			res.register_advance()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_token, right)
		return res.success(left)
	
	def comp_expr(self):
		res = ParseResult()
		if self.current_token.matches(tk.TT_KEYWORD, "not"):
			op_token = self.current_token
			res.register_advance()
			self.advance()
			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(op_token, node))
		else:
			node = res.register(self.bin_op(self.arithmatic_expr, (tk.TT_DEQUALS, tk.TT_NEQUALS, tk.TT_LTHAN, tk.TT_GTHAN, tk.TT_LTEQUALS, tk.TT_GTEQUALS)))
			if res.error: return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected INT, FLOAT, not, identifier, +, -, or '('"
			))
			return res.success(node)
	
	def arithmatic_expr(self):
		return self.bin_op(self.term, (tk.TT_PLUS, tk.TT_MINUS))

	
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
		self.count_advanced = 0

	def register_advance(self):
		self.count_advanced += 1
	
	def register(self, result):
		self.count_advanced += result.count_advanced
		if result.error: self.error = result.error
		return result.node
	
	def success(self, node):
		self.node = node
		return self
	
	def failure(self, error):
		if self.error is None or self.count_advanced == 0:
			self.error = error
		return self