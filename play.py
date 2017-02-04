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
def indexDocument(input, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index):
	#inverted_index is a dictionary of dictionaries
	#the key is the token, the value is a dictionary with:
	#the key as the DOCID and the value as the frequency (the number of t in d)

	# *** STEP ONE:----------------------------------------------------------------
	# preprocess the content provided as input
	tokens = prepareString(input)

	# *** STEP TWO:----------------------------------------------------------------
	# add the tokens to the inverted index provided as input and calculate the numbers necessary to
	# calculate the weights for the given weighting schemes
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
def retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query, NDocs, doc_tfidf):
	relevant_docs = {}

	# *** STEP ONE:----------------------------------------------------------------
	# preprocess the query
	tokens = prepareString(query)

	query_index = {}

	for index in range(len(tokens)):
		if tokens[index] not in query_index.keys():
			query_index[tokens[index]] = 1.0
		else:
			query_index[tokens[index]] += 1.0

	if (weighting_scheme_query.lower() == "tfidf"):
		# tf is not normalized in classic tfidf
		idf = calc_inverse_document_frequency(inverted_index, NDocs)
		query_tfidf = find_query_tfidf(query_index, idf)

	if (weighting_scheme_query.lower() == "test"):
		idf = calc_probabilistic_idf(inverted_index, NDocs)

		# maximum_freq_query = max([i for i in query_index.values()]) 

		# #adjust for repeated words in query
		# for term in query_index.keys():
		# 	query_index[term] = 0.5 + 0.5 * (query_index[term] / maximum_freq_query)

		query_tfidf = find_query_tfidf(query_index, idf)

	# *** STEP TWO:----------------------------------------------------------------
	# determine the set of documents from the inverted index that include at least 
	# one token from the query
	docs_to_search = {}

	for term in query_index.keys():
		if term in inverted_index.keys():
			for doc in inverted_index[term].keys():
				if doc not in docs_to_search.keys():
					docs_to_search[doc] = doc_tfidf[doc]

	# *** STEP THREE:----------------------------------------------------------------
	# calculate the similarity between the query and each of the documents in this set, 
	# using the given weighting schemes to calculate the document and the query term weights.
	relevant_docs = calc_similarity(query_tfidf, docs_to_search)

	sorted_relevant_docs = sorted(relevant_docs.iteritems(), key=operator.itemgetter(1), reverse=True)

	return sorted_relevant_docs

# *** HELPER FUNCTIONS ***
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
def find_max_term_frequency(inverted_index):
	# for each term in the inverted_index:
	# finds the highest number of occurences of the term in a single document within the collection
	# max_f {key = term; value = max occurrences}
	max_f = {}

	for key in inverted_index.keys():
		max = 0
		for doc in inverted_index[key]:
			if max < inverted_index[key][doc]:
				max = inverted_index[key][doc]
		
		max_f[key] = max

	return max_f
#---------------------------------------------------------------------------
def augmented_normalize_term_frequency(inverted_index, max_f):
	#normalizes the term frequency for each doc: tf = (f/max{f})
	for term in inverted_index.keys():
		for doc in inverted_index[term].keys():
			inverted_index[term][doc] = 0.5 + 0.5 * (inverted_index[term][doc]/max_f[term])

	return inverted_index
#---------------------------------------------------------------------------
def calc_inverse_document_frequency(inverted_index, NDocs):
	#idf = log10(N/df)
	# N = total number of documents
	# df = dft is the document frequency of t: the number of documents that contain t
	# this is calculated by the length of the dictionary of documents in the inverted_index
	inverse_doc_freq = {}
	for term in inverted_index.keys():
		inverse_doc_freq[term] = log10(NDocs/len(inverted_index[term]))

	return inverse_doc_freq

def calc_probabilistic_idf(inverted_index, NDocs):
	# p-idf = log(N - n/n) where 
	# N = total number of documents, n = the number of documents containing t
	prob_idf = {}

	for term in inverted_index.keys():
		n = len(inverted_index[term])
		to_log = (NDocs - n)/n
		if to_log < 1:
			to_log = 1
		prob_idf[term] = log10(to_log)

	return prob_idf
#---------------------------------------------------------------------------
def find_doc_tfidf(inverted_index, idf):
	# doc_tfidf is a matrix of the document vectors
	# doc_tfidf {key = docID; value = dictionary of terms}
	# in term dictionary {key = term; value = tf-idf}
	doc_tfidf = {}

	for term in inverted_index.keys():
		for doc in inverted_index[term].keys():
			if doc not in doc_tfidf.keys():
				doc_tfidf[doc] =  {}
				doc_tfidf[doc][term] = inverted_index[term][doc] * idf[term]
			else:
				doc_tfidf[doc][term] = inverted_index[term][doc] * idf[term]

	return doc_tfidf

def find_doc_tf(inverted_index):
	doc_tf = {}

	for term in inverted_index.keys():
		for doc in inverted_index[term].keys():
			if doc not in doc_tf.keys():
				doc_tf[doc] = {}
				doc_tf[doc][term] = inverted_index[term][doc]
			else:
				doc_tf[doc][term] = inverted_index[term][doc]

	return doc_tf 

#---------------------------------------------------------------------------
def find_query_tfidf(query_index, idf):
	# query_tfidf = {key = term; value = tf-idf}
	# idf is assumed to be 0 for terms not in the document corpus
	query_tfidf = {}

	for term in query_index.keys():
		if term not in idf.keys():
			query_tfidf[term] = 0
		else:
			query_tfidf[term] = query_index[term] * idf[term]

	return query_tfidf

#---------------------------------------------------------------------------
def calc_similarity(query_tfidf, doc_tfidf):
	# FROM SALTON ARTICLE
	# similarity = sum (w_query * w_doc)

	doc_similarity = {}

	for doc in doc_tfidf.keys():

		for term in query_tfidf.keys():
			dot_product = 0.0
			if term in doc_tfidf[doc].keys():
				dot_product += (query_tfidf[term] * doc_tfidf[doc][term])

		doc_similarity[doc] = dot_product

	return doc_similarity

def cosine_similarity(query_tfidf, doc_tfidf):
	# doc_similarity is a dictionary with:
	# {key = doc; value = cosine_similarity}
	doc_similarity = {}
	length_q = 0

	for term in query_tfidf.keys():
		# for each term in the query, sum the square of the tf-idf
		# a^2 + b^2 ...
		length_q += pow(query_tfidf[term], 2)

	for doc in doc_tfidf.keys():
		length_doc = 0
		dot_product = 0
		for term in doc_tfidf[doc].keys():
			# for each term in the document, sum the square of the tf-idf
			# a^2 + b^2 ...
			length_doc += pow(doc_tfidf[doc][term], 2)

		for term in query_tfidf.keys():
			if term in doc_tfidf[doc].keys():
				dot_product += (query_tfidf[term] * doc_tfidf[doc][term])
		# if the term is missing from either, dot_product for that term = 0

		if (length_q != 0 and length_doc != 0):
			#cosine similarity (dot_product/product of the magnitudes)
			doc_similarity[doc] = dot_product/sqrt(length_q * length_doc)
		else:
			doc_similarity[doc] = 0

	return doc_similarity

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	inverted_index = {}

	# VALID WEIGHTING SCHEMES:
	# docs: tfidf, enhanced
	# query: tfidf, probabilistic
	weighting_scheme_docs = ''
	weighting_scheme_query = ''
	input_folder = ''
	query_file = ''

	output = ''

	docCount = 0

	#print 'Argument List:', str(sys.argv)
	
	try: 
		weighting_scheme_docs = str(sys.argv[1])
		weighting_scheme_query = str(sys.argv[2])
		input_folder = str(sys.argv[3])
		query_file = str(sys.argv[4])
	except:
		sys.exit("ERROR: input format not correct, expecting: \n [document weighting] [query weighting] [input folder] [query file]")

	if (weighting_scheme_query.lower() != 'tfidf' and weighting_scheme_query.lower() != 'test'):
		sys.exit("ERROR: invalid query weighting scheme, choose tfidf or test")
	if (weighting_scheme_docs.lower() != 'tfidf' and weighting_scheme_docs.lower() != 'test'):
		sys.exit("ERROR: invalid document weighting scheme, choose tfidf or test")
	# *** STEP ONE: ----------------------------------------------------------
	# open the folder containing the data collection, provided as the third argument on the command
	# line (e.g., cranfieldDocs/), and read one file at a time from this folder
	path = os.path.join(os.getcwd(), input_folder) #specified folder

	for filename in os.listdir(path): #for all files in specified folder
		docID = str(filename)
		docID = re.sub(r'[a-zA-Z]*', '', docID)
		docCount += 1

		# *** STEP TWO: ----------------------------------------------------------
		# for each file, obtain the content of the file, and add it to the index with indexDocument
		path2file = os.path.join(path, filename)
		lines = [line.rstrip('\n') for line in open(path2file)] #get all the text lines from the file
		for line in lines:
			inverted_index = indexDocument(line, weighting_scheme_docs, weighting_scheme_query, docID, inverted_index)


	# *** STEP THREE: ----------------------------------------------------------
	# calculate necessary things for term weighting schemes
	# if necessary for the term weighting schemes, calculate and store the length of each document
	if (weighting_scheme_docs.lower() == "tfidf"):
		idf = calc_inverse_document_frequency(inverted_index, docCount)
		doc_tfidf = find_doc_tfidf(inverted_index, idf)

	elif (weighting_scheme_docs.lower() == "test"):
		print("HELLO THERE")
		# weights the document term frequency using augmented normalized term frequency
		max_f = find_max_term_frequency(inverted_index)
		inverted_index = augmented_normalize_term_frequency(inverted_index, max_f)
		# ntf-idf
		doc_tf = find_doc_tf(inverted_index)

		print('+++++++++++++++++++++++++++++')
		print(doc_tf['0051'])

		for doc in doc_tf.keys():
			norm_factor = 0.0
			for term in doc_tf[doc]:
				norm_factor += doc_tf[doc][term]
			for term in doc_tf[doc]:
				doc_tf[doc][term] = (doc_tf[doc][term]/norm_factor)

		doc_tfidf = doc_tf

		print('***************************************')
		print(doc_tf['0051'])


	# *** STEP FOUR: ----------------------------------------------------------
	# open the file with queries, provided as the fourth argument on the command line (e.g.,
	# cranfield.queries), and read one query at a time from this file (each line is a query)
	path2query = os.path.join(os.getcwd(), query_file)
	queries = [line.rstrip('\n') for line in open(path2query)] #get all the text lines from the file
	for query in queries:
		# remove queryID from query
		temp = query.split()
		queryID = temp[0] 
		query = "".join(str(i) + " " for i in temp[1:])

		# *** STEP FIVE: ----------------------------------------------------------
		# for each query, find the list of documents that are relevant, along with their 
		# similarity scores.
		relDocs = retrieveDocuments(query, inverted_index, weighting_scheme_docs, weighting_scheme_query, docCount, doc_tfidf)

		print(queryID) # used to see progress of running program

		for doc in relDocs:
			output += str(queryID) + ' ' + str(doc[0]) + ' ' + str(doc[1]) + '\n'

	#Prepare and print output --------------------------------------------------------------------
	output_filename = 'cranfield.' + weighting_scheme_docs + '.' + weighting_scheme_query + '.output23'
	#print(output_filename)
	targetFile = open(output_filename, 'w+')

	targetFile.write(output)



if __name__ == "__main__": 
	main()