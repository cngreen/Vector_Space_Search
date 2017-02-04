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

def calculate_precision(rel_docs, my_docs, top):
	num_relevant = 0.0

	for doc in rel_docs:
		if doc in my_docs:
			num_relevant += 1.0

	if top > len(my_docs):
		top = len(my_docs)

	precision = num_relevant/top

	return precision

def calculate_recall(rel_docs, my_docs, top):
	num_relevant = 0.0

	for doc in rel_docs:
		if doc in my_docs:
			num_relevant += 1.0

	recall = num_relevant/len(rel_docs)

	return recall

def find_macro_averages(rel_docs, my_docs, x):
	total_precision = 0.0
	total_recall = 0.0

	i = 1
	while (i < 226):
		#print('query', i)
		input_rel = rel_docs[i]
		#print(input_rel)

		index = int(x)
		input_mine = my_docs[i][0:index]
		#print(input_mine)

		precision = calculate_precision(input_rel, input_mine, x)

		total_precision += precision

		#print(precision)

		recall = calculate_recall(input_rel, input_mine, x)

		total_recall += recall
		#print(recall)

		i += 1

	print("macro averages: ")
	print(total_precision/225.0)
	print(total_recall/255.0)

#---------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	rel_docs = {}

	path = os.path.join(os.getcwd(), 'cranfield.reljudge')

	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		line = line.split()
		query_id = int(line[0])
		document = int(line[1])

		if query_id not in rel_docs.keys():
			rel_docs[query_id] = [document]
		else:
			rel_docs[query_id].append(document)

	#print (rel_docs)

# GET DATA FROM MY WEIGHTING SCHEME
	path = os.path.join(os.getcwd(), 'cranfield.enhanced.probabilistic.output')

	my_docs = {}
	
	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		line = line.split()
		query_id = int(line[0])
		document = int(line[1])

		if query_id not in my_docs.keys():
			my_docs[query_id] = [document]
		else:
			my_docs[query_id].append(document)

	#print(my_docs)


# GET DATA FROM TFIDF WEIGHTING SCHEME
	path = os.path.join(os.getcwd(), 'cranfield.tfidf.tfidf.output')

	tfidf_docs = {}
	
	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		line = line.split()
		query_id = int(line[0])
		document = int(line[1])

		if query_id not in tfidf_docs.keys():
			tfidf_docs[query_id] = [document]
		else:
			tfidf_docs[query_id].append(document)


# GET OTHER DATA:
	path = os.path.join(os.getcwd(), 'cranfield.enhanced.tfidf.output')

	enhanced_docs = {}
	
	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		line = line.split()
		query_id = int(line[0])
		document = int(line[1])

		if query_id not in enhanced_docs.keys():
			enhanced_docs[query_id] = [document]
		else:
			enhanced_docs[query_id].append(document)

	path = os.path.join(os.getcwd(), 'cranfield.tfidf.probabilistic.output')

	prob_docs = {}
	
	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		line = line.split()
		query_id = int(line[0])
		document = int(line[1])

		if query_id not in prob_docs.keys():
			prob_docs[query_id] = [document]
		else:
			prob_docs[query_id].append(document)


	#print(tfidf_docs)

	
	print("\nmine 10")
	find_macro_averages(rel_docs, my_docs, 10.0)
	print("tfidf 10")
	find_macro_averages(rel_docs, tfidf_docs, 10.0)
	# print("enhanced 10")
	# find_macro_averages(rel_docs, enhanced_docs, 10.0)
	# print("probabilistic 10")
	# find_macro_averages(rel_docs, prob_docs, 10.0)

	print("\nmine 50")
	find_macro_averages(rel_docs, my_docs, 50.0)
	print("tfidf 50")
	find_macro_averages(rel_docs, tfidf_docs, 50.0)
	# print("enhanced 50")
	# find_macro_averages(rel_docs, enhanced_docs, 50.0)
	# print("probabilistic 50")
	# find_macro_averages(rel_docs, prob_docs, 50.0)

	print("\nmine 100")
	find_macro_averages(rel_docs, my_docs, 100.0)
	print("tfidf 100")
	find_macro_averages(rel_docs, tfidf_docs, 100.0)
	# print("enhanced 100")
	# find_macro_averages(rel_docs, enhanced_docs, 100.0)
	# print("probabilistic 100")
	# find_macro_averages(rel_docs, prob_docs, 100.0)

	print("\nmine 500")
	find_macro_averages(rel_docs, my_docs, 500.0)
	print("tfidf 500")
	find_macro_averages(rel_docs, tfidf_docs, 500.0)
	# print("enhanced 500")
	# find_macro_averages(rel_docs, enhanced_docs, 500.0)
	# print("probabilistic 500")
	# find_macro_averages(rel_docs, prob_docs, 500.0)





if __name__ == "__main__": 
	main()