# Kari Green
# cngreen
# vectorspace.py
#----------------------------------------

import sys
import os
import re
from processDocument import *
from porterStemmer import *

#---------------------------------------------------------------------------
def prepareString(input):
	tokens = []

	line = removeSGML(input) #step one: remove SGML
	line.strip()
	# print 'step one (SGML): ', line
	if line != '':
		tokens = tokenizeText(line) #step two: tokenize text
		# print 'step two (tokens): ', temp
		tokens = removeStopwords(tokens) #step three: remove stop words
		# print 'step three (stop words): ', temp
		tokens = stemWords(tokens) #step four: step vocab
		# print 'step four (stem): ', temp

	return tokens
#---------------------------------------------------------------------------
def indexDocument(input, docID, inverted_index):
	tokens = prepareString(input)

	for index in range(len(tokens)):
		if tokens[index] not in inverted_index.keys():
			inverted_index[tokens[index]] = {}
			inverted_index[tokens[index]][docID] = 1
		else:
			if docID not in inverted_index[tokens[index]].keys():
				inverted_index[tokens[index]][docID] = 1
			else:
				inverted_index[tokens[index]][docID] += 1
	
	return inverted_index

def identifyFormattedNumbers(input):
	#finds formatted numbers
	tokens = []
	if '.' not in input and ',' not in input:
		return input, tokens

	match = re.findall(r'\s*\d+[[,\d+]*[.\d+]*]*\s*', input)
	if match != None:
		for m in match:
			m = m.strip()
			m = m.replace(',','')
			tokens.append(m)
		input = re.sub(r'\s*\d+[[,\d+]*[.\d+]*]*\s*', '', input)

	match = re.findall(r'\s*\d+[,.]', input)
	if match != None:
		for m in match:
			m = m.strip()
			tokens.append(m)

	return input, tokens

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():
	# input = "here is a sentence i am trying to import"
	# input2 = "here is a secondary sentence sentence sentence with changes i am trying to import"

	# inverted_index = {}

	# inverted_index = indexDocument(input, 69, inverted_index)
	# print(inverted_index)
	# inverted_index = indexDocument(input2, 1738, inverted_index)
	# print(inverted_index)

	formatted = "1,000  1000 a777 b9 100.0 777,787,787788, 67,873,292  67874292 100. 100, 10,000,"

	formatted, tokens = identifyFormattedNumbers(formatted)

	print(formatted)
	print(tokens)


if __name__ == "__main__": 
	main()