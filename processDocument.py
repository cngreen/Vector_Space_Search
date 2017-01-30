# Kari Green
# cngreen
# preprocess.py
#----------------------------------------

import sys
import os
import re
import operator

from porterStemmer import *

#----------------------------------------------------------------------------------------------------------------------------------------
def removeSGML(input):
	#print("input: ", input)
	if '<' in input and '>' in input: #if there are tag characters find the tags
		strlist = []
		for c in input:
			strlist.append(c)

		firstndx = -1
		secondndx = -1
		# find the first < of the line
		for i in range(len(strlist)):
			if strlist[i] == '<':
				firstndx = i
				break

		# find the first > of the line
		for i in range(len(strlist)):
			if strlist[i] == '>':
				secondndx = i
				break


		quotendx = -1
		temp = firstndx
		# check if there is attribute quotations in tag (risk for extra >)
		while temp <= secondndx:
			if strlist[temp] == '"':
				quotendx = temp
				break
			temp += 1

		if quotendx != -1: #there is a quotation in the tag
			quotendx2 = -1
			temp = quotendx + 1
			# make sure the quotation ends
			while temp <= secondndx: #check from just after the quote to the end of the tag
				if strlist[temp] == '"':
					quotendx2 = temp
					break
				temp += 1

			print("quotendx2", quotendx2)

			if quotendx2 != -1: #the quote ended, remove quoted content:
				while quotendx <= quotendx2:
					strlist[quotendx] = ''
					quotendx += 1
				input = ''.join(strlist)
				return(removeSGML(input)) #rerun the remove SGML without the quote
			
			else: #find end of quote:
				temp = quotendx + 1
				while temp <= len(strlist):
					if strlist[temp] == '"':
						quotendx2 = temp
						break
					temp += 1

				if quotendx2 != -1: #the quote ended, remove quoted content:
					while quotendx <= quotendx2:
						strlist[quotendx] = ''
						quotendx += 1
					input = ''.join(strlist)
					return(removeSGML(input)) #rerun the remove SGML without the quote

				else: #the quote doesn't end on this line
					sys.exit("ERROR: improper SGML tag, quotation in SGML tag does not end")

	# remove all chars between first < and first > of the line
		#print("remove from: ", firstndx, " to: ", secondndx)
		while firstndx <= secondndx:
			strlist[firstndx] = ''
			firstndx += 1
		input = ''.join(strlist) #check if there are more remaining
		return(removeSGML(input))

	#otherwise output the input
	return input
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------

def indentifyDates(input):
	#finds numerical dates with years of 4 or two digits separated by - / . or ,
	#returns dates in a list, removes them from the input string
	matches = []

	months = [] #list of common month abbrev.
	months.extend(['january', 'jan', 'jan.'])
	months.extend(['february', 'feb', 'feb.'])
	months.extend(['march', 'mar', 'mar.'])
	months.extend(['april', 'apr', 'apr.'])
	months.extend(['may', 'may.'])
	months.extend(['june', 'jun', 'jun.'])
	months.extend(['july', 'jul', 'jul.'])
	months.extend(['august', 'aug', 'aug.'])
	months.extend(['september', 'sep', 'sep.', 'sept', 'sept.'])
	months.extend(['october', 'oct', 'oct.'])
	months.extend(['november', 'nov', 'nov.'])
	months.extend(['december', 'dec', 'dec.'])
	#print months
	
	# XXXX-X/X-X/X year(4), month, day sep by - / . or ,
	match = re.findall(r'\d{4}[-/.,]\d{1,2}[-/.,]\d{1,2}', input)
	if match != None:
		for m in match:
			matches.append(m)
		input = re.sub(r'\d{4}[-/.,]\d{1,2}[-/.,]\d{1,2}', '', input)
		
	# X/X-X/X-XXXX day, month, year(4) sep by - / . or ,
	match = re.findall(r'\d{1,2}[-/.,]\d{1,2}[-/.,]\d{4}', input)
	if match != None:
		for m in match:
			matches.append(m)
		input = re.sub(r'\d{1,2}[-/.,]\d{1,2}[-/.,]\d{4}', '', input)

	#XX-X/X-X/X year(2), month, day sep by - / . or ,
	match = re.findall(r'\d{2}[-/.,]\d{1,2}[-/.,]\d{1,2}', input)
	if match != None:
		for m in match:
			matches.append(m)
		input = re.sub(r'\d{2}[-/.,]\d{1,2}[-/.,]\d{1,2}', '', input)
	#X/X-X/X-XX day, month, year(2) sep by - / . or ,
	match = re.findall(r'\d{1,2}[-/.,]\d{1,2}[-/.,]\d{2}', input)
	if match != None:
		for m in match:
			matches.append(m)
		input = re.sub(r'\d{1,2}[-/.,]\d{1,2}[-/.,]\d{2}', '', input)

	#abc-X/X-XX alpha month, day, year(4) 
	match = re.findall(r'[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}[-/.,]*\s*\d{4}', input)
	if match != None:
		input = re.sub(r'[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}[-/.,]*\s*\d{4}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date

	#X/X-abc-XXXX day, month, year(4)
	match = re.findall(r'\d{1,2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{4}', input)
	if match != None:
		input = re.sub(r'\d{1,2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{4}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date

	#year(4), month, day
	match = re.findall(r'\d{4}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}', input)
	if match != None:
		input = re.sub(r'\d{4}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date

	#abc-X/X-XX alpha month, day, year(2) 
	match = re.findall(r'[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}[-/.,]*\s*\d{2}', input)
	if match != None:
		input = re.sub(r'[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}[-/.,]*\s*\d{2}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date

	#X/X-abc-XXXX day, month, year(2)
	match = re.findall(r'\d{1,2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{2}', input)
	if match != None:
		input = re.sub(r'\d{1,2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{2}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date

	#year(2), month, day
	match = re.findall(r'\d{2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}', input)
	if match != None:
		input = re.sub(r'\d{2}[-/.,]*\s*[a-zA-z]{3,9}[.]*\s*[-./,]*\d{1,2}', '', input)
		for m in match:
			month = re.findall(r'[a-zA-z]+', m)
			month = str(month[0]).lower()
			if month in months:
				matches.append(m)
			else:
				input += (' ' + str(m)) #don't remove it if it wasn't a date
				
	return input, matches
#------------------------------------------------------------------------------------------------------------------
def identifyContractions(input):
	#identifies contractions, splits and adds to tokens, removes from input
	tokens = []

	contractions = {} #list of contactions, adapted from https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
	contractions["aren't"] = 'are not'
	contractions["can't"] = 'can not'
	contractions["could've"] = 'could have'
	contractions["couldn't"] = 'could not'
	contractions["didn't"] = 'did not'
	contractions["doesn't"] = 'does not'
	contractions["don't"] = 'do not'
	contractions["hadn't"] = 'had not'
	contractions["hasn't"] = 'has not'
	contractions["he'd"] = 'he had'
	contractions["he'll"] = 'he will'
	contractions["he's"] = 'he is'
	contractions["how'd"] = 'how did'
	contractions["how'll"] = 'how will'
	contractions["how's"] = 'how is'
	contractions["i'd"] = 'i would'
	contractions["i'll"] = 'i will'
	contractions["i'm"] = 'i am'
	contractions["i've"] = 'i have'
	contractions["isn't"] = 'is not'
	contractions["it'll"] = 'it will'
	contractions["it's"] = 'it is'
	contractions["mightn't"] = 'might not'
	contractions["might've"] = 'might have'
	contractions["mustn't"] = 'must not'
	contractions["must've"] = 'must have'
	contractions["she'd"] = 'she had'
	contractions["she'll"] = 'she will'
	contractions["she's"] = 'she is'
	contractions["should've"] = 'should have'
	contractions["shouldn't"] = 'should not'
	contractions["something's"] = 'something has'
	contractions["that'll"] = 'that will'
	contractions["that's"] = 'that is'
	contractions["that'd"] = 'that would'
	contractions["there'd"] = 'there had'
	contractions["there're"] = 'there are'
	contractions["there's"] = 'there is'
	contractions["they'd"] = 'they had'
	contractions["they'll"] = 'they will'
	contractions["they're"] = 'they are'
	contractions["they've"] = 'they have'
	contractions["wasn't"] = 'was not'
	contractions["we'd"] = 'we had'
	contractions["we'll"] = 'we will'
	contractions["we're"] = 'we are'
	contractions["we've"] = 'we have'
	contractions["weren't"] = 'were not'
	contractions["what'd"] = 'what did'
	contractions["what'll"] = 'what will'
	contractions["what're"] = 'what are'
	contractions["what's"] = 'what is'
	contractions["what've"] = 'what have'
	contractions["when's"] = 'when is'
	contractions["where'd"] = 'where did'
	contractions["where's"] = 'where is'
	contractions["where've"] = 'where have'
	contractions["who'd"] = 'who did'
	contractions["who'll"] = 'who will'
	contractions["who're"] = 'who are'
	contractions["who's"] = 'who has'
	contractions["who've"] = 'who have'
	contractions["why'd"] = 'why did'
	contractions["why'll"] = 'why will'
	contractions["why're"] = 'why are'
	contractions["why's"] = 'why is'
	contractions["won't"] = 'will not'
	contractions["would've"] = 'would have'
	contractions["wouldn't"] = 'would not'
	contractions["y'all"] = 'you all'
	contractions["you'd"] = 'you would'
	contractions["you'll"] = 'you will'
	contractions["you're"] = 'you are'
	contractions["you've"] = 'you have'

	if "'" not in input:
		return input, tokens

	input = input.lower()

	match = re.findall(r"[a-zA-Z]+'[a-zA-Z]+", input) #things that look like contractions
	if match != None:
		for m in match:
			if m in contractions.keys():
				tokens.extend(contractions[m].split())
			else:
				a = re.split(r"'", m)
				if a != None and len(a) >= 2:
					if a[1] == 's':
						a[1] = "'s"
					tokens.extend(a)
		input = re.sub(r"[a-zA-Z]+'[a-zA-Z]+", '', input) #remove contractions from input

	#print input, tokens
	return input, tokens
#--------------------------------------------------------------------------------------------------------
def identifyPhrases(input):
	#finds alphanumeric hypenated phrases
	#per spec: tokenization of - (keep phrases separated by - together)
	#I am considering 93-thousand as a phrase rather than '93' and 'thousand'
	tokens = []
	if '-' not in input:
		return input, tokens

	match = re.findall(r'\w+-\w+[-\w+]*', input)
	if match != None:
		for m in match:
			tokens.append(m)
		input = re.sub(r'\w+-\w+[-\w+]*', '', input)

	return input, tokens

def identifyFormattedNumbers(input):
	#finds formatted numbers
	tokens = []
	if '.' not in input and ',' not in input:
		return input, tokens

	match = re.findall(r'\s\d+[[,\d+]*[.\d+]*]*\s', input)
	if match != None:
		for m in match:
			m = m.strip()
			tokens.append(m)
		input = re.sub(r'\s\d+[[,\d+]*[.\d+]*]*\s', '', input)

	return input, tokens

def identifyAcronymsAbbrev(input):
	#finds formatted numbers
	tokens = []
	if '.' not in input:
		return input, tokens

	match = re.findall(r'\w+[.]+\w*[.\w*]*', input)
	if match != None:
		for m in match:
			m = m.strip()
			tokens.append(m)
		input = re.sub(r'\w+[.]+\w*[.\w*]*', '', input)

	return input, tokens
#--------------------------------------------------------------------------------------------------------

def tokenizeText(input):
	tokens = []
	if input == '':
		return tokens

	input, dates = indentifyDates(input)
	tokens.extend(dates)

	input, contractions = identifyContractions(input)
	tokens.extend(contractions)

	input, phrases = identifyPhrases(input)
	tokens.extend(phrases)

	input, numbers = identifyFormattedNumbers(input)
	tokens.extend(numbers)

	input, abbrev = identifyAcronymsAbbrev(input)
	tokens.extend(abbrev)

	words = input.split()
	for w in words:
		w = re.sub(r'\W+', '', w)
		if w != '':
			tokens.append(w)

	return tokens

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------

def getStopwords():
	# read stopwords to list from file
	stopwords = []
	path = os.path.join(os.getcwd(), 'stopwords')
	lines = [line.rstrip('\n') for line in open(path)]
	lines = [line.strip(' ') for line in lines]

	for line in lines:
		stopwords.append(line)

	return stopwords
#---------------------------------------------------------------------------------------------------------------------
def removeStopwords(tokens):
	# remove stopwords from tokens
	stopwords = getStopwords()
	output = []
	for t in tokens:
		if t not in stopwords:
			output.append(t)
	
	return output

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def stemWords(tokens):
	output = []
	p = PorterStemmer()

	for t in tokens:
		if len(t) == 0:
			continue
		output.append(p.stem(t, 0, len(t)-1))

	return output

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():
	words = []
	vocab = {}
	#print 'Argument List:', str(sys.argv)
	try: 
		foldername = str(sys.argv[1])
	except:
		sys.exit("ERROR: no folder of that name")

	path = os.path.join(os.getcwd(), foldername) #specified folder

	for filename in os.listdir(path): #for all files in specified folder
		#print str(filename)
		path2file = os.path.join(path, filename)
		lines = [line.rstrip('\n') for line in open(path2file)] #get all the text lines from the file

		#for each line in the file
		for line in lines:
			line = removeSGML(line) #step one: remove SGML
			line.strip()
			# print 'step one (SGML): ', line
			if line != '':
				temp = []
				temp = tokenizeText(line) #step two: tokenize text
				# print 'step two (tokens): ', temp
				temp = removeStopwords(temp) #step three: remove stop words
				# print 'step three (stop words): ', temp
				temp = stemWords(temp) #step four: step vocab
				# print 'step four (stem): ', temp

				words.extend(temp) #add this to overall words


	targetFile = open('preprocess.output', 'w+')

	output =  "Words " + str(len(words)) + '\n'
	targetFile.write(output)

	for word in words:
		if word not in vocab.keys():
			vocab[word] = 1
		else:
			vocab[word] += 1

	output = "Vocabulary " + str(len(vocab)) + '\n'
	targetFile.write(output)

	top50 = sorted(vocab.iteritems(), key=operator.itemgetter(1), reverse=True)[:50]

	for top in top50:
		output = str(top[0]) + ' ' + str(top[1]) + '\n'
		targetFile.write(output)

	#FIND NUM WORDS TO GET TOP 25%
	# top150 = sorted(vocab.iteritems(), key=operator.itemgetter(1), reverse=True)[:150]

	# total = 0
	# countWords = 0

	# while total < 36643:
	# 	total += top150[countWords][1]
	# 	countWords += 1

	# print countWords, total

	# print top150[60]


if __name__ == "__main__": 
	main()