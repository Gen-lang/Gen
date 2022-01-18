class Position
	def initialize(index : Int32, lnum : Int32, col : Int32, filename : String, filetext : String)
		@index = index
		@lnum = lnum
		@col = col
		@filename = filename
		@filetext = filetext
	end

	def advance(current_char=nil)
		@index += 1
		@col += 1
		if current_char == "\n"
			@lnum += 1
			@col = 0
		end
	end

	def copy()
		return Position.new(@index, @lnum, @col, @filename, @filetext)
	end
end