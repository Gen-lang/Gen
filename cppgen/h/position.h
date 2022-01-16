#pragma once
#include <string>
#include <memory>

using namespace std;

class Position {
	int index;
	int lnum;
	int col;
	string filename;
	string filetext;

	Position(int _index, int _lnum, int _col, string _filename, string _filetext) {
		index = _index;
		lnum = _lnum;
		col = _col;
		filename = _filename;
		filetext = _filetext;
	}

	void advance(char current_char=' ') {
		index++;
		col++;
		if (current_char == '\n') {
			lnum++;
			col = 0;
		}
	}

	Position copy() {
		return Position(index, lnum, col, filename, filetext);
	}
};