import readline # this is necessary: DO NOT REMOVE
from src.lexer import Lexer
from src.parser import Parser
from src.value import Number
from src.builtin_func import BuiltinFunction
from src.evaluator import Evaluator
from src.context import Context
from src.symbol_table import SymbolTable

global_symbol_table = SymbolTable()
global_symbol_table.set("nothing", Number.null)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("Pi", Number.Pi)
# built-in functions
global_symbol_table.set("println", BuiltinFunction.println)
global_symbol_table.set("print", BuiltinFunction.print)
global_symbol_table.set("input", BuiltinFunction.input)
global_symbol_table.set("int_input", BuiltinFunction.int_input)
global_symbol_table.set("absolute_number_of", BuiltinFunction.absolute_number_of)
global_symbol_table.set("is_number", BuiltinFunction.is_number)
global_symbol_table.set("is_string", BuiltinFunction.is_string)
global_symbol_table.set("is_array", BuiltinFunction.is_array)
global_symbol_table.set("is_function", BuiltinFunction.is_function)
global_symbol_table.set("exit_program", BuiltinFunction.exit_program)

def run(filename, text):
	# generate tokens
	lexer = Lexer(filename, text)
	tokens, err = lexer.make_tokens()
	if err is not None: return None, err

	# generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# call evaluator
	evaluator = Evaluator()
	context = Context("<module>")
	context.symbol_table = global_symbol_table
	result = evaluator.visit(ast.node, context)

	return result.value, result.error

def main():
	while True:
		t = input("gen>> ")
		result, err = run("<stdin>", t)
		if err is not None:
			print(err)
		elif result:
			print(result.__repr__())

if __name__ == "__main__":
	main()