require "./Position"

class Context
	def initialize(display_name : String, parent : Context = nil, parent_entry_pos : Position = nil)
		@display_name = display_name
		@parent = parent
		@parent_entry_pos = parent_entry_pos
		@symbol_table = None
	end
end