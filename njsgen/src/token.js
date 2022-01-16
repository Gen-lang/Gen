
const TT_INT	 		= "INT" // int
const TT_FLOAT 			= "FLOAT" // float
const TT_STRING			= "STRING" // string
const TT_L_SQ			= "L_SQ" // [
const TT_R_SQ			= "R_SQ" // ]
const TT_L_BRACE		= "L_BRACE" // {
const TT_R_BRACE		= "R_BRACE" // }
const TT_RIGHT			= "RIGHT>" // >
const TT_PLUS			= "PLUS" // plus
const TT_MINUS			= "MINUS" // minus
const TT_MULT			= "MULT" // multiplication
const TT_DIV			= "DIV" // division
const TT_POWER			= "POWER" // power
const TT_MODULO			= "MODULO" // modulo %
const TT_L_PAREN		= "L_PAREN" // left parenthesis
const TT_R_PAREN		= "R_PAREN" // right parenthesis
const TT_IDENTIFIER		= "IDENTIFIER" // identifier
const TT_KEYWORD 		= "KEYWORD" // keyword
const TT_EQUALS			= "EQUALS" // =
const TT_DEQUALS		= "DOUBLE_EQUALS" // ==
const TT_NEQUALS		= "NOT_EQUALS" // !=
const TT_LTHAN			= "L_THAN" // <
const TT_GTHAN			= "G_THAN" // >
const TT_LTEQUALS		= "LT_EQUALS" // <=
const TT_GTEQUALS		= "GT_EQUALS" // >=
const TT_COMMA			= "COMMA" // ,
const TT_ARROW			= "ARROW" // ->
const TT_AT				= "AT" // @
const TT_NL				= "NEW_LINE" // \n
const TT_EOF			= "EOF" // End Of File

const KEYWORDS = [
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

class Token {
	constructor(type, value=null, pos_start=null, pos_end=null) {
		this.type = type
		this.value = value
		if (pos_start != null) {
			this.pos_start = pos_start.copy()
			this.pos_end = pos_start.copy()
			this.pos_end.advance()
		}
		if (pos_end) {
			this.pos_end = pos_end.copy()
		}
	}

	as_string() {
		return (this.value != null) ? `${this.type}:${this.value}` : `${this.type}`
	}

	matches(type, value) {
		return this.type === type && self.value === value
	}
}