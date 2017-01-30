# Kari Green
# cngreen
# vectorspace.py
#----------------------------------------

import sys
import os
import re

from processDocument.py import *

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

def indexDocument(input, weighting_scheme_docs, weighting_scheme_query):
	inverted_index = {}
	tokens = prepareString(input)
	
	return inverted_index

def retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query):
	relevant_docs = {}
	return relevant_docs
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	print 'Argument List:', str(sys.argv)
	
	try: 
		foldername = str(sys.argv[1])
	except:
		sys.exit("ERROR: no folder of that name")

	path = os.path.join(os.getcwd(), foldername) #specified folder

	for filename in os.listdir(path): #for all files in specified folder
		#print str(filename)
		path2file = os.path.join(path, filename)
		lines = [line.rstrip('\n') for line in open(path2file)] #get all the text lines from the file


	targetFile = open('cranfield.weightingdocuments.weightingquery.output', 'w+')

	output = "my output" + '\n'
	targetFile.write(output)



if __name__ == "__main__": 
	main()