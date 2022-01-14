import readline # this is necessary: DO NOT REMOVE
from src.lexer import Lexer
from src.parser import Parser
from src.value import Number
from src.evaluator import Evaluator
from src.context import Context
from src.symbol_table import SymbolTable

global_symbol_table = SymbolTable()
global_symbol_table.set("nothing", Number(0))
global_symbol_table.set("true", Number(1))
global_symbol_table.set("false", Number(0))

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
			print(result)

if __name__ == "__main__":
	main()