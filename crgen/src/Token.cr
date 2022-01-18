require "./Position"


TT_INT	 		= "INT" # int
TT_FLOAT 		= "FLOAT" # float
TT_STRING		= "STRING" # string
TT_L_SQ			= "L_SQ" # [
TT_R_SQ			= "R_SQ" # ]
TT_L_BRACE		= "L_BRACE" # {
TT_R_BRACE		= "R_BRACE" # }
TT_RIGHT		= "RIGHT>" # >
TT_PLUS			= "PLUS" # plus
TT_MINUS		= "MINUS" # minus
TT_MULT			= "MULT" # multiplication
TT_DIV			= "DIV" # division
TT_POWER		= "POWER" # power
TT_MODULO		= "MODULO" # modulo %
TT_L_PAREN		= "L_PAREN" # left parenthesis
TT_R_PAREN		= "R_PAREN" # right parenthesis
TT_IDENTIFIER	= "IDENTIFIER" # identifier
TT_KEYWORD 		= "KEYWORD" # keyword
TT_EQUALS		= "EQUALS" # =
TT_DEQUALS		= "DOUBLE_EQUALS" # ==
TT_NEQUALS		= "NOT_EQUALS" # !=
TT_LTHAN		= "L_THAN" # <
TT_GTHAN		= "G_THAN" # >
TT_LTEQUALS		= "LT_EQUALS" # <=
TT_GTEQUALS		= "GT_EQUALS" # >=
TT_COMMA		= "COMMA" # ,
TT_ARROW		= "ARROW" # ->
TT_AT			= "AT" # @
TT_NL			= "NEW_LINE" # \n
TT_EOF			= "EOF" # End Of File

KEYWORDS = [
	"or",
	"and",
	"not",
	"if",
	"elseif",
	"then",
	"else",
	"for",
	"through",
	"step",
	"while",
	"defunc",
	"end",
	"return",
	"continue",
	"break"
]


class Token
	def initialize(type : String, value : String = nil, pos_start : Position = nil, pos_end : Position = nil)
		@type = type
		@value = value
		if pos_start != nil
			@pos_start = pos_start.copy()
			@pos_end = pos_start.copy()
			@pos_end.advance()
		end

		if pos_end != nil
			@pos_end = pos_end.copy()
		end
	end

	def as_string()
		return if @value != nil ? "#{@type}:#{@value}" : "#{@type}"
	end

	def matches(type : String, value : String)
		return @type == type && @value == value
	end
end