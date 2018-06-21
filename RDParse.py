# File:     RDParse.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     June 21st, 2018
# Purpose:  A recursive descent parser for a specific grammar 

import sys

tokens = []
count = 0
file = sys.argv[1]
fileContents = open(file, "r")
tokens = fileContents.read().split()
print(tokens)
    