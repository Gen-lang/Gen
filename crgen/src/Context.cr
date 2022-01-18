class Context
	def initialize(display_name, parent=nil, parent_entry_pos=nil)
		@display_name = display_name
		@parent = parent
		@parent_entry_pos = parent_entry_pos
		@symbol_table = None
	end
end