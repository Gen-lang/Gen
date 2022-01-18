require "./Token"
require "./Error"
require "./Node"

class Parser
	def initialize(tokens)
		@tokens = tokens
		@token_index = -1
		@current_token = nil
		advance()
	end

	def advance()
		@token_index += 1
		update_current_token()
		return @current_token
	end

	def update_current_token()
		if @token_index < @tokens.size && @token_index >= 0
			@current_token = @tokens[@token_index]
		end
	end

	def reverse(amount : Int16 = 1)
		@token_index -= amount
		update_current_token()
		return @current_token
	end
end