def string_with_arrows(text : String, pos_start, pos_end) 
	# I know this sucks. I will make it better some day.
	result = text.gsub("\t") {""}
	result += "\n"
	result += ("^" * text.size)
	return result
end