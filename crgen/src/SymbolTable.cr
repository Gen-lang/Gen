class SymbolTable
	def initialize(parent=Nil)
		@symbols = {} of String => String
		@parent = parent
	end

	def get(var_name)
		begin
			value = @symbols[var_name]
		rescue
			value = Nil
		end
		
		if value == Nil && @parent != Nil
			return @parent[var_name]
		else
			return value
		end
	end
end