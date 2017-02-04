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

#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
def main():

	path = os.path.join(os.getcwd(), 'cranfield.reljudge')

	lines = [line.rstrip('\n') for line in open(path)] #get all the text lines from the file
	for line in lines:
		print line





if __name__ == "__main__": 
	main()