require "./utils"
require "./Context"

class Error
	def initialize(pos_start, pos_end, error_name : String, details : String)
		@pos_start = pos_start
		@pos_end = pos_end
		@error_name = error_name
		@details = details
	end

	def as_string()
		string = "File #{@pos_start.filename}, line #{@pos_start.lnum+1}"
		string += "Gen::#{@error_name}: #{@details}"
		string += "\n\n" + string_with_arrows(@pos_start.filetext, @pos_start, @pos_end)
		return string
	end
end


class TypeCharError < Error
	def initialize(pos_start, pos_end, details : String)
		super(pos_start, pos_end, "TypeCharError", details)
	end
end


class InvalidSyntaxError < Error
	def initialize(pos_start, pos_end, details : String, context : Context)
		super(pos_start, pos_end, "InvalidSyntaxError", details)
		@context = context
	end
end


class GenRuntimeError < Error
	def initialize(pos_star,t pos_end, details : String)
		super(pos_start, pos_end, "RuntimeError", details)
	end

	def as_string()
		string = generate_traceback()
		string += "Gen::#{@error_name}: #{@details}"
		string += "\n\n" + string_with_arrows(@pos_start.filetext, @pos_start, @pos_end)
		return string
	end

	def generate_traceback()
		result = ""
		position = @pos_start
		context = @context
		while context
			result = " File #{position.filename}, line #{position.lnum+1}, in #{context.display_name}\n" + result
			position = context.parent_entry_pos
			context = context.parent
		end
		return "Traceback (most recent call last):\n" + result
	end
end