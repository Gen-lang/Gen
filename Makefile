install:
ifeq ($(OS),Windows_NT)
	@echo "Currently, Windows is not supported."
else
	@pip install pyinstaller
	@pyinstaller ./main.py --onefile
	@cp ./dist/main /usr/local/bin/pygen
	@echo "\033[0;32mPyGen Compilation Succeeded"
	@echo "\033[0;32mType 'pygen'"
endif
