def string_with_arrows(text, pos_start, pos_end):
	result = ""
	
	index_start = max(text.rfind("\n", 0, pos_start.index), 0)
	index_end = text.find("\n", index_start+1)
	if index_end < 0: index_end = len(text)

	line_count = pos_end.lnum - pos_start.lnum + 1
	for i in range(line_count):
		line = text[index_start:index_end]
		column_start = pos_start.col if i == 0 else 0
		column_end = pos_end.col if i == line_count - 1 else len(line) - 1
		result += line + "\n"
		result += " " * column_start + "^" * (column_end - column_start)

		index_start = index_end
		index_end = text.find("\n", index_start+1)
		if index_end < 0: index_end = len(text)
	
	return result.replace("\t", "")