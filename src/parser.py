from token import TokenType

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


