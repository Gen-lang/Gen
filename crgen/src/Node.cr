require "./Token"
require "./Position"

class Node
end

class NumberNode < Node
	def initialize(token : Token)
		@token = token
		@pos_start = @token.pos_start
		@pos_end = @token.pos_end
	end
end


class StringNode < Node
	def initialize(token : Token)
		@token = token
		@pos_start = @token.pos_start
		@pos_end = @token.pos_end
	end
end


class ArrayNode < Node
	def initialize(elements, pos_start : Position, pos_end : Position)
		@element_nodes = elements
		@pos_start = pos_start
		@pos_end = pos_end
	end
end


class BinOpNode < Node
	def initialize(left_node, op_token, right_node)
		@left_node = left_node
		@op_token = op_token
		@right_node = right_node
		@pos_start = @left_node.pos_start
		@pos_end = @right_node.pos_end
	end
end


class UnaryOpNode < Node
	def initialize(op_token : Token, node)
		@op_token = op_token
		@node = node
		@pos_start = @op_token.pos_start
		@pos_end = @node.pos_end
	end
end


class VarAccessNode < Node
	def initialize(var_name_token : Token)
		@var_name_token = var_name_token
		@pos_start = @var_name_token.pos_start
		@pos_end = @var_name_token.pos_end
	end
end

class VarAssignNode < Node
	def initialize(var_name_token, value_node)
		@var_name_token = var_name_token
		@value_node = value_node
		@pos_start = @var_name_token.pos_start
		@pos_end = @value_node.pos_end
	end
end


class IfNode < Node
	def initialize(cases, else_case)
		@cases = cases
		@else_case = else_case
		@pos_start = @cases[0][0].pos_start
		if (@else_case != nil || @else_case != false)
			@pos_end = @else_case[0].pos_end
		else
			@pos_end = @cases[-1][0].pos_end
		end
	end
end


class ReturnNode < Node
	def initialize(node_to_return, pos_start : Position, pos_end : Position)
		@node_to_return = node_to_return
		@pos_start = pos_start
		@pos_end = pos_end
	end
end


class ContinueNode < Node
	def initialize(pos_start : Position, pos_end : Position)
		@pos_start = pos_start
		@pos_end = pos_end
	end
end


class BreakNode < Node
	def initialize(pos_start : Position, pos_end : Position)
		@pos_start = pos_start
		@pos_end = pos_end
	end
end


class ForNode < Node
	def initialize(var_name_token : Token, start_value_node, end_value_node, step_value_node, body_node, should_return_null)
		@var_name_token = var_name_token
		@start_value_node = start_value_node
		@end_value_node = end_value_node
		@step_value_node = step_value_node
		@body_node = body_node
		@pos_start = @var_name_token.pos_start
		@pos_end = @body_node.pos_end
		@should_return_null = should_return_null
	end
end


class WhileNode < Node
	def initialize(condition, body_node, should_return_null)
		@condition = condition
		@body_node = body_node
		@pos_start = @condition_node.pos_start
		@pos_end = @body_node.pos_end
		@should_return_null = should_return_null
	end
end


class FuncDefNode < Node
	def initialize(var_name_token, arg_name_tokens, body_node, should_auto_return)
		@var_name_token = var_name_token
		@arg_name_tokens = arg_name_tokens
		@body_node = body_node
		@should_auto_return = should_auto_return
		if @var_name_token
			@pos_start = @var_name_token.pos_start
		elsif @arg_name_tokens.size > 0
			@pos_start = @arg_name_tokens[0].pos_start
		else
			@pos_start = @body_node.pos_start
		end
		@pos_end = @body_node.pos_end
	end
end


class CallNode < Node
	def initialize(node_to_call, arg_nodes)
		@node_to_call = node_to_call
		@arg_nodes = arg_nodes
		@pos_start = @node_to_call.pos_start
		if @arg_nodes.size > 0
			@pos_end = @arg_nodes[-1].pos_end
		else
			@pos_end = @node_to_call.pos_end
		end
	end
end