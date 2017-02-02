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
def indexDocument(input, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index):
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
#---------------------------------------------------------------------------
def retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query):
	relevant_docs = {}
	return relevant_docs
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	inverted_index = {}

	weighting_scheme_docs = ''
	weighting_scheme_query = ''
	input_folder = ''
	query_file = ''

	print 'Argument List:', str(sys.argv)
	
	try: 
		weighting_scheme_docs = str(sys.argv[1])
		weighting_scheme_query = str(sys.argv[2])
		input_folder = str(sys.argv[3])
		query_folder = str(sys.argv[4])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [query weighting] [document weighting] [input folder] [query file]")

	path = os.path.join(os.getcwd(), input_folder) #specified folder

	for filename in os.listdir(path): #for all files in specified folder
		docID = str(filename)
		path2file = os.path.join(path, filename)
		lines = [line.rstrip('\n') for line in open(path2file)] #get all the text lines from the file
		for line in lines:
			inverted_index = indexDocument(line, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index)

	
	for key in inverted_index.keys():
		max = 0
		for doc in inverted_index[key]:
			max += inverted_index[key][doc]
		print key, max

	output_filename = 'cranfield.' + weighting_scheme_docs + '.' + weighting_scheme_query + '.output'
	#print(output_filename)
	targetFile = open(output_filename, 'w+')

	output = "my output" + '\n'
	targetFile.write(output)



if __name__ == "__main__": 
	main()