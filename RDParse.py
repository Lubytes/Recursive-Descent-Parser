# File:     RDParse.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     June 21st, 2018
# Purpose:  A recursive descent parser for a specific grammar 

import sys

tokens = []
count = 0
for x in sys.argv:
    if(count == 0):
        count += 1
        continue
    tokens.append(x)

print(tokens)
    