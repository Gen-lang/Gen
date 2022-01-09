from lexer import Lexer

def run(filename, text):
	lexer = Lexer(filename, text)
	tokens, err = lexer.make_tokens()

	return tokens, err

def main():
	while True:
		t = input("gen>> ")
		result, err = run("<stdin>", t)
		if err is not None: print(err.as_string)
		else: print(result)

if __name__ == "__main__":
	main()