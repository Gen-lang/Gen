class SymbolTable
	def initialize(parent=nil)
		@symbols = {} of String => String
		@parent = parent
	end

	def get(var_name)
		begin
			value = @symbols[var_name]
		rescue
			value = nil
		end
		
		if value == nil && @parent != nil
			return @parent[var_name]
		else
			return value
		end
	end
end