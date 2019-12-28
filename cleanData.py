#!/usr/bin/env python
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import string
import os

#this method is used to remove all of the punctuation, uppercase, and top 100 common words. It replaces the current text file with the new text file 
def remove_format(file_name): # copied format for this code from https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
	common_words = ['about', 'all', 'also', 'and', 'as', 'at', 'be', 'because', 'but', 'by', 'can', 'come', 'could', 'day', 'do', 'even', 'find', 'first', 'for', 'from', 'get', 'give', 'go', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'I', 'if', 'in', 'into', 'it', 'its', 'just', 'know', 'like', 'look', 'make', 'man', 'many', 'me', 'more', 'my', 'new', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'people', 'say', 'see', 'she', 'so', 'some', 'take', 'tell', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thing', 'think', 'this', 'those', 'time', 'to', 'two', 'up', 'use', 'very', 'want', 'way', 'we', 'well', 'what', 'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']
	file_path = os.path.abspath(file_name)
	#Create temp file
	fh, abs_path = mkstemp()
	with fdopen(fh,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				line = line.replace('\n',' \n')
				#print(line)
				lower_line = line.lower() # making the text file lower case 
				table = str.maketrans({key: None for key in string.punctuation})
				edited_line = lower_line.translate(table) # eliminating all the punctuation from the text file
				line_words = edited_line.split(" ")
				while "" in line_words: line_words.remove("")
				#while "\n" in line_words: line_words.remove("\n")
				resultwords  = [word for word in line_words if word not in common_words] #copied concept from https://stackoverflow.com/questions/25346058/removing-list-of-words-from-a-string
				result = ' '.join(resultwords)
				new_file.write(result)
    #Remove original file
	remove(file_path)
    #Move new file
	move(abs_path, file_path)






def main(args):
	remove_format("test.txt")
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
