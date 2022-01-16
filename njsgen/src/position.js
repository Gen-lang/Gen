class Position {
	constructor(index, lnum, col, filename, filetext) {
		this.index = index
		this.lnum = lnum
		this.col = col
		this.filename = filename
		this.filetext = filetext
	}

	advance(current_char=null) {
		this.index += 1;
		this.col += 1;
		if (current_char == "\n") {
			this.lnum += 1
			this.col += 1
		}
	}

	copy() {
		return Position(this.index, this.lnum, this.col, this.filename, this.filetext)
	}
}