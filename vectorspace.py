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
	#see processDocument.py
	tokens = []

	line = removeSGML(input) #step one: remove SGML
	line.strip()

	if line != '':
		tokens = tokenizeText(line) #step two: tokenize text
		tokens = removeStopwords(tokens) #step three: remove stop words
		tokens = stemWords(tokens) #step four: stem vocab

	return tokens
#---------------------------------------------------------------------------
def indexDocument(input, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index):
	#inverted_index is a dictionary of dictionaries
	#the key is the token, the value is a dictionary with:
	#the key as the DOCID and the value as the frequency (the number of t in d)
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
#---------------------------------------------------------------------------
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
	# this is calculated by the length of the dictionary of documents in the inverted_index
	inverse_doc_freq = {}
	for term in inverted_index.keys():
		inverse_doc_freq[term] = log10(NDocs/len(inverted_index[term]))
	return inverse_doc_freq

def find_max_term_frequency(inverted_index):
	#finds the highest number of occurences of the term in a single document within the collection
	max_f = {}

	for key in inverted_index.keys():
		max = 0
		for doc in inverted_index[key]:
			if max < inverted_index[key][doc]:
				max = inverted_index[key][doc]
		
		max_f[key] = max

	return max_f

def find_doc_tfidf(inverted_index, NDocs):
	doc_tfidf = {}

	max_f = find_max_term_frequency(inverted_index)

	tf = normalize_term_frequency(inverted_index, max_f)
	idf = calc_inverse_document_frequency(inverted_index, NDocs)

	for term in inverted_index.keys():
		for doc in inverted_index[term].keys():
			if doc not in doc_tfidf.keys():
				doc_tfidf[doc] =  {}
				doc_tfidf[doc][term] = tf[term][doc] * idf[term]
			else:
				doc_tfidf[doc][term] = tf[term][doc] * idf[term]

	return doc_tfidf

def cosine_similarity(query_tfidf, doc_tfidf):
	doc_similarity = {}

	length_q = 0

	for term in query_tfidf.keys():
		# for each term in the query, sum the square of the tf-idf
		# a^2 + b^2 ...
		length_q += pow(query_tfidf[term], 2)

	length_q = sqrt(length_q)

	for doc in doc_tfidf.keys():
		length_doc = 0
		dot_product = 0
		for term in doc_tfidf[doc].keys():
			length_doc += pow(doc_tfidf[doc][term], 2)
		length_doc = sqrt(length_doc)

		for term in query_tfidf.keys():
			if term in doc_tfidf[doc].keys():
				dot_product += (query_tfidf[term] * doc_tfidf[doc][term])

		if (length_q != 0 and length_doc != 0):
			doc_similarity[doc] = dot_product/(length_q * length_doc)
		else:
			doc_similarity[doc] = 0

	return doc_similarity

#---------------------------------------------------------------------------
def retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query, NDocs, doc_tfidf):
	relevant_docs = {}

	#preprocess the query
	tokens = prepareString(query)

	query_index = {}

	for index in range(len(tokens)):
		if tokens[index] not in query_index.keys():
			query_index[tokens[index]] = 1.0
		else:
			query_index[tokens[index]] += 1.0

	maximum_freq_query = max([i for i in query_index.values()]) 

	#adjust for repeated words in query
	for term in query_index.keys():
		query_index[term] = (query_index[term] / maximum_freq_query)

	# # determine metrics:
	# max_f = find_max_term_frequency(inverted_index)

	# tf = normalize_term_frequency(inverted_index, max_f)
	idf = calc_inverse_document_frequency(inverted_index, NDocs)

	query_tfidf = {}

	for term in query_index.keys():
		if term not in idf.keys():
			query_tfidf[term] = 0
		else:
			query_tfidf[term] = query_index[term] * idf[term]

	docs_to_search = {}

	for term in query_index.keys():
		if term in inverted_index.keys():
			for doc in inverted_index[term].keys():
				if doc not in docs_to_search.keys():
					docs_to_search[doc] = doc_tfidf[doc]

	relevant_docs = cosine_similarity(query_tfidf, docs_to_search)

	sorted_relevant_docs = sorted(relevant_docs.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]

	return sorted_relevant_docs
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	inverted_index = {}

	weighting_scheme_docs = ''
	weighting_scheme_query = ''
	input_folder = ''
	query_file = ''

	docCount = 0

	print 'Argument List:', str(sys.argv)
	
	try: 
		weighting_scheme_docs = str(sys.argv[1])
		weighting_scheme_query = str(sys.argv[2])
		input_folder = str(sys.argv[3])
		query_file = str(sys.argv[4])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [query weighting] [document weighting] [input folder] [query file]")

	# *** STEP ONE: ----------------------------------------------------------
	# open the folder containing the data collection, provided as the third argument on the command
	# line (e.g., cranfieldDocs/), and read one file at a time from this folder
	path = os.path.join(os.getcwd(), input_folder) #specified folder

	for filename in os.listdir(path): #for all files in specified folder
		docID = str(filename)
		docCount += 1

		# *** STEP TWO: ----------------------------------------------------------
		# for each file, obtain the content of the file, and add it to the index with indexDocument
		path2file = os.path.join(path, filename)
		lines = [line.rstrip('\n') for line in open(path2file)] #get all the text lines from the file
		for line in lines:
			inverted_index = indexDocument(line, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index)


	# Calculate the term frequency and normalize docs tf -----------------------------------------------
	max_f = find_max_term_frequency(inverted_index)

	tf = normalize_term_frequency(inverted_index, max_f)
	idf = calc_inverse_document_frequency(inverted_index, docCount)


	# *** STEP THREE: ----------------------------------------------------------
	# open the file with queries, provided as the fourth argument on the command line (e.g.,
	# cranfield.queries), and read one query at a time from this file (each line is a query)
	path2query = os.path.join(os.getcwd(), query_file)
	queries = [line.rstrip('\n') for line in open(path2query)] #get all the text lines from the file
	for query in queries:
		# remove queryID from query
		temp = query.split()
		queryID = temp[0] 
		query = "".join(str(i) + " " for i in temp[1:])

		doc_tfidf = find_doc_tfidf(inverted_index, docCount)
		relDocs = retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query, docCount, doc_tfidf)

		print(queryID, relDocs)


	#Prepare and print output --------------------------------------------------------------------
	output_filename = 'cranfield.' + weighting_scheme_docs + '.' + weighting_scheme_query + '.output'
	#print(output_filename)
	targetFile = open(output_filename, 'w+')

	output = "my output" + '\n'
	targetFile.write(output)



if __name__ == "__main__": 
	main()