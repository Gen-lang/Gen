import readline # this is necessary: DO NOT REMOVE
import sys
from src.lexer import Lexer
from src.parser import Parser
from src.value import Number
from src.builtin_func import BuiltinFunction
from src.evaluator import Evaluator
from src.context import Context
from src.symbol_table import SymbolTable

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
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
global_symbol_table.set("size", BuiltinFunction.size)

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

def shell():
	while True:
		t = input("gen>> ")
		if t.strip() == "": continue
		result, err = run("<stdin>", t)
		if err is not None:
			print(err)
		elif result:
			if len(result.elements) == 1:
				print(result.elements[0])
			else:
				print(result.__repr__())

def file(filename):
	try:
		with open(filename, "r") as fobj:
			code = fobj.read()
			_, error = run(filename, code)
			if error: print(error)
	except Exception:
		print(f"Could not open file '{filename}'.")
		exit()
	

if __name__ == "__main__":
	if len(sys.argv) < 1 or sys.argv[-1].endswith(".py"):
		shell()
	else:
		filename = sys.argv[-1]
		if filename.endswith(".gen"):
			file(filename)
		else:
			print("Specify a file with .gen extension.")