from lexer import Lexer
from parser import Parser
from evaluator import Evaluator
from context import Context

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
	result = evaluator.visit(ast.node, context)

	return result.value, result.error

def main():
	while True:
		t = input("gen>> ")
		result, err = run("<stdin>", t)
		if err is not None: print(err.as_string)
		else: print(result)

if __name__ == "__main__":
	main()