# Kari Green
# cngreen
# vectorspace.py
#----------------------------------------

import sys
import os
import re

from math import *
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
			inverted_index[tokens[index]][docID] = 1.0
		else:
			if docID not in inverted_index[tokens[index]].keys():
				inverted_index[tokens[index]][docID] = 1.0
			else:
				inverted_index[tokens[index]][docID] += 1.0
	
	return inverted_index

def normalize_term_frequency(inverted_index, max_f):
	#normalizes the term frequency for each doc: tf = f/max{f}
	for token in inverted_index.keys():
		for doc in inverted_index[token].keys():
			inverted_index[token][doc] = (inverted_index[token][doc]/max_f[token])

	return inverted_index

def calc_inverse_document_frequency(inverted_index, NDocs):
	#idf = log10(N/df)
	# N = total number of documents
	# df = dft is the document frequency of t: the number of documents that contain t
	inverse_doc_freq = {}
	for term in inverted_index.keys():
		inverse_doc_freq[term] = log10(NDocs/len(inverted_index[term]))
	return inverse_doc_freq

def find_max_term_frequency(inverted_index):
	max_f = {}

	for key in inverted_index.keys():
		max = 0
		for doc in inverted_index[key]:
			if max < inverted_index[key][doc]:
				max = inverted_index[key][doc]
		
		max_f[key] = max

	return max_f

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():
	input = "here is a sentence i am trying to import"
	input2 = "here is a secondary sentence sentence sentence sentence with changes changes changes i am trying to import"

	inverted_index = {}

	inverted_index = indexDocument(input, 69, inverted_index)
	inverted_index = indexDocument(input2, 1738, inverted_index)

	print(inverted_index)

	term_frequency = {}

	term_frequency = find_max_term_frequency(inverted_index)

	print('***\n')
	print(term_frequency)

	print('+++\n')
	inverted_index = normalize_term_frequency(inverted_index, term_frequency)
	print(inverted_index)

	print('kkkk\n')
	idf = calc_inverse_document_frequency(inverted_index, 2)

	print(idf)




if __name__ == "__main__": 
	main()