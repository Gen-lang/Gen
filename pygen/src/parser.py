import src.gen_token as tk
from src.error import InvalidSyntaxError
from src.node import *

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.current_token = None
		self.advance()
	
	def advance(self):
		self.token_index += 1
		self.update_current_token()
		return self.current_token
	
	def update_current_token(self):
		if self.token_index < len(self.tokens) and self.token_index >= 0:
			self.current_token = self.tokens[self.token_index]
	
	def reverse(self, amount=1):
		self.token_index -= amount
		self.update_current_token()
		return self.current_token

	def atom(self):
		res = ParseResult()
		token = self.current_token

		if token.type in (tk.TT_INT, tk.TT_FLOAT):
			res.register_advance()
			self.advance()
			return res.success(NumberNode(token))
		elif token.type == tk.TT_STRING:
			res.register_advance()
			self.advance()
			return res.success(StringNode(token))
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
		elif token.type == tk.TT_L_SQ:
			array_expression = res.register(self.array_expr())
			if res.error: return res
			return res.success(array_expression)
		elif token.matches(tk.TT_KEYWORD, "if"):
			if_expression = res.register(self.if_expr())
			if res.error: return res
			return res.success(if_expression)
		elif token.matches(tk.TT_KEYWORD, "for"):
			for_expression = res.register(self.for_expr())
			if res.error: return res
			return res.success(for_expression)
		elif token.matches(tk.TT_KEYWORD, "while"):
			while_expression = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expression)
		elif token.matches(tk.TT_KEYWORD, "defunc"):
			defunc = res.register(self.defunc())
			if res.error: return res
			return res.success(defunc)
		else:
			return res.failure(InvalidSyntaxError(
				token.pos_start, token.pos_end, "Expected int, float, identifier, +, -, '(', '[', 'if', 'for', 'while', or 'defunc'"
			))

	def power(self):
		return self.bin_op(self.call, (tk.TT_POWER,), self.factor)
	
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
		return self.bin_op(self.factor, (tk.TT_MULT, tk.TT_DIV, tk.TT_AT))

	def array_expr(self):
		res = ParseResult()
		elements = []
		pos_start = self.current_token.pos_start.copy()
		res.register_advance()
		self.advance()
		if self.current_token.type == tk.TT_R_SQ:
			res.register_advance()
			self.advance()
		else:
			elements.append(res.register(self.expr()))
			if res.error: return res.failure(InvalidSyntaxError(
								self.current_token.pos_start, self.current_token.pos_end, "Expected ']', '[', 'if', 'for', 'while', 'defunc', int, float, identifier"
							))
			while self.current_token.type == tk.TT_COMMA:
				res.register_advance()
				self.advance()
				elements.append(res.register(self.expr()))
				if res.error: return res
			if self.current_token.type != tk.TT_R_SQ:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected ',' or ']'"
				))
			else:
				res.register_advance()
				self.advance()
		return res.success(ArrayNode(elements, pos_start, self.current_token.pos_end.copy()))
	
	def expr(self):
		res = ParseResult()
		# checking variable assignment
		if self.current_token.type == tk.TT_IDENTIFIER:
			var_name = self.current_token
			res.register_advance()
			self.advance()
			if self.current_token.type == tk.TT_EQUALS:
				res.register_advance()
				self.advance()
				expression = res.register(self.expr())
				if res.error: return res
				return res.success(VarAssignNode(var_name, expression))
			else:
				res.deregister_advance()
				self.reverse(amount=1)

		node = res.register(self.bin_op(self.comp_expr, ((tk.TT_KEYWORD, "and"), (tk.TT_KEYWORD, "or"))))
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected int, float, identifier, +, -, '(', '[', 'if', 'for', 'while', or 'defunc'"
			))
		return res.success(node)
	
	def if_expr(self):
		res = ParseResult()
		all_cases = res.register(self.if_expr_cases("if"))
		if res.error: res
		cases, else_case = all_cases
		return res.success(IfNode(cases, else_case))
	
	def if_expr_elseif(self):
		return self.if_expr_cases("elseif")
	
	def if_expr_else(self):
		res = ParseResult()
		else_case = None
		if self.current_token.matches(tk.TT_KEYWORD, "else"):
			res.register_advance()
			self.advance()
			if self.current_token.type == tk.TT_NL:
				res.register_advance()
				self.advance()
				statements = res.register(self.statements())
				if res.error: return res
				else_case = (statements, True)
				if self.current_token.matches(tk.TT_KEYWORD, "end"):
					res.register_advance()
					self.advance()
				else:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected 'end'"
					))
			else:
				expr = res.register(self.expr())
				if res.error: return res
				else_case = (expr, False)
		return res.success(else_case)
	
	def if_expr_elseif_or_else(self):
		res = ParseResult()
		cases = []
		else_case = None
		if self.current_token.mathces(tk.TT_KEYWORD, "elseif"):
			all_cases = res.register(self.if_expr_elseif())
			if res.error: return res
			cases, else_case = all_cases
		else:
			else_case = res.register(self.if_expr_else())
			if res.error: return res
		return res.success((cases, else_case))
	
	def if_expr_cases(self, keyword):
		res = ParseResult()
		cases = []
		else_case = None
		if self.current_token.matches(tk.KEYWORDS, keyword) is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, f"Expected '{keyword}'"
			))
		res.register_advance()
		self.advance()
		condition = res.register(self.expr())
		if res.error: return res
		if self.current_token.matches(tk.KEYWORDS, "then") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'then'"
			))
		res.register_advance()
		self.advance()
		if self.current_token.type == tk.TT_NL:
			res.register_advance()
			self.advance()
			statements = res.register(self.statements())
			if res.error: return res
			else: cases.append((condition, statements, True))
			if self.current_token.matches(tk.KEYWORDS, "end"):
				res.register_advance()
				self.advance()
			else:
				all_cases = res.register(self.if_expr_elseif_or_else())
				if res.error: return res
				new_cases, else_case = all_cases
				cases.extend(new_cases)
		else:
			expr = res.register(self.expr())
			if res.error: return res
			cases.append((condition, expr, False))
			all_cases = res.register(self.if_expr_elseif_or_else())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)
		return res.success((cases, else_case))

	
	def for_expr(self):
		res = ParseResult()
		if self.current_token.matches(tk.TT_KEYWORD, "for") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'for'"
			))
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
				self.current_token.pos_start, self.current_token.pos_end, "Expected '='"
			))
		res.register_advance()
		self.advance()
		start_value = res.register(self.expr())
		if res.error: return res
		if self.current_token.matches(tk.TT_KEYWORD, "through") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'through'"
			))
		res.register_advance()
		self.advance()
		end_value = res.register(self.expr())
		if res.error: return res
		if self.current_token.matches(tk.TT_KEYWORD, "step"):
			res.register_advance()
			self.advance()
			step_value = res.register(self.expr())
			if res.error: return res
		else:
			step_value = None
		if self.current_token.matches(tk.TT_KEYWORD, "then") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'then'"
			))
		res.register_advance()
		self.advance()
		body = res.register(self.expr())
		if res.error: return res
		return res.success(ForNode(var_name, start_value, end_value, step_value, body))
	
	def while_expr(self):
		res = ParseResult()
		if self.current_token.matches(tk.TT_KEYWORD, "while") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'while'"
			))
		res.register_advance()
		self.advance()
		condition = res.register(self.expr())
		if res.error: return res
		if self.current_token.matches(tk.TT_KEYWORD, "then") is False:
			return res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'then'"
			))
		res.register_advance()
		self.advance()
		body = res.register(self.expr())
		if res.error: return res
		return res.success(WhileNode(condition, body))

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
				self.current_token.pos_start, self.current_token.pos_end, "Expected int, float, not, identifier, +, -, '[', or '('"
			))
			return res.success(node)
	
	def arithmatic_expr(self):
		return self.bin_op(self.term, (tk.TT_PLUS, tk.TT_MINUS))
	
	def defunc(self):
		res = ParseResult()
		if self.current_token.matches(tk.TT_KEYWORD, "defunc") is False:
			res.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected 'defunc'"
			))
		else:
			self.advance()
			# get function name if possible
			if self.current_token.type == tk.TT_IDENTIFIER:
				func_var_name_token = self.current_token
				self.advance()
				# check for left paren
				if self.current_token.type != tk.TT_L_PAREN:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected '('"
					))
			else: # annonymous function
				func_var_name_token = None
				# check for left paren
				if self.current_token.type != tk.TT_L_PAREN:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected '(' or an identifier"
					))
			res.register_advance()
			self.advance()
			# get arguments if any is present
			arg_name_tokens = []
			if self.current_token.type == tk.TT_IDENTIFIER:
				arg_name_tokens.append(self.current_token)
				res.register_advance()
				self.advance()
				while self.current_token.type == tk.TT_COMMA:
					res.register_advance()
					self.advance()
					if self.current_token.type != tk.TT_IDENTIFIER:
						return res.failure(InvalidSyntaxError(
							self.current_token.pos_start, self.current_token.pos_end, "Expected an identifier after ','"
						))
					else:
						arg_name_tokens.append(self.current_token)
						res.register_advance()
						self.advance()
				# check for right paren
				if self.current_token.type != tk.TT_R_PAREN:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected ',' or ')'"
					))
			else:
				if self.current_token.type != tk.TT_R_PAREN:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"
					))
			res.register_advance()
			self.advance()
			if self.current_token.type != tk.TT_ARROW:
				return res.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end, "Expected '->'"
				))
			res.register_advance()
			self.advance()
			return_node = res.register(self.expr())
			if res.error: return res
			return res.success(FuncDefNode(
				func_var_name_token, arg_name_tokens, return_node
			))
	
	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())
		if res.error: return res
		if self.current_token.type == tk.TT_L_PAREN:
			res.register_advance()
			self.advance()
			arg_nodes = []
			if self.current_token.type == tk.TT_R_PAREN: # mearning that no arguments are passed
				res.register_advance()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expr()))
				if res.error: return res.failure(InvalidSyntaxError(
								self.current_token.pos_start, self.current_token.pos_end, "Expected ')', ']', 'if', 'for', 'while', 'defunc', int, float, identifier"
							))
				while self.current_token.type == tk.TT_COMMA:
					res.register_advance()
					self.advance()
					arg_nodes.append(res.register(self.expr()))
					if res.error: return res
				if self.current_token.type != tk.TT_R_PAREN:
					return res.failure(InvalidSyntaxError(
						self.current_token.pos_start, self.current_token.pos_end, "Expected ',' or ')'"
					))
				else:
					res.register_advance()
					self.advance()
			return res.success(CallNode(atom, arg_nodes))
		return res.success(atom)
	
	def statements(self):
		res = ParseResult()
		statements = []
		pos_start = self.current_token.pos_start.copy()
		while self.current_token.type == tk.TT_NL:
			res.register_advance()
			self.advance()
		statement = res.register(self.expr())
		if res.error: return res
		statements.append(statement)
		more = True
		while True:
			new_line_count = 0
			while self.current_token.type == tk.TT_NL:
				res.register_advance()
				self.advance()
				new_line_count += 1
			if new_line_count == 0: more = False
			if more is False: break
			statement = res.try_register(self.expr())
			if statement is None:
				self.reverse(res.to_reverse_count)
				more = False
				continue
			statements.append(statement)
		return res.success(ArrayNode(
			statements, pos_start, self.current_token.pos_end.copy()
		))
		
	
	def parse(self):
		result = self.statements()
		if result.error and self.current_token.type != tk.TT_EOF:
			return result.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end, "Expected +, -, *, or /"
			))
		return result


class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.count_advanced = 0
		self.to_reverse_count = 0

	def register_advance(self):
		self.count_advanced += 1
	
	def deregister_advance(self):
		self.count_advanced -= 1
	
	def try_register(self, res):
		if res.error is not None:
			self.to_reverse_count = res.count_advanced
			return None
		else:
			return self.register(res)
	
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