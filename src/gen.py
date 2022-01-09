from lexer import Lexer

def run(text):
	lexer = Lexer(text)
	tokens, err = lexer.make_tokens()

	return tokens, err

def main():
	while True:
		t = input("gen>> ")
		result, err = run(t)
		if err is not None: print(err.as_string)
		else: print(result)

if __name__ == "__main__":
	main()