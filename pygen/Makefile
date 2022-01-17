# Usage
# Just type 'make' or 'make install'

install:
ifeq ($(OS),Windows_NT)
# I'm not using Windows, so I don't know
# Windows commands to achieve the same thing for Linux-based systems.
# Need help here!!
	@echo "Currently, Windows is not supported."
else
	@pip install pyinstaller
	@pyinstaller ./main.py --onefile
	@cp ./dist/main /usr/local/bin/gen
	@cp ../editor/gen.vim ~/.vim/syntax
	@echo "autocmd BufRead,BufNewFile *.gen set filetype=gen" >> ~/.vimrc
	@echo "\033[0;32mPyGen Compilation Succeeded"
	@echo "\033[0;32mType 'pygen'"
endif
