class Context
	def initialize(display_name, parent=Nil, parent_entry_pos=Nil)
		@display_name = display_name
		@parent = parent
		@parent_entry_pos = parent_entry_pos
		@symbol_table = None
	end
end