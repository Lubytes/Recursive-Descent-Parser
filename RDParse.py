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



#
def parse_S(tokenList):


def parse_atoms(tokenList, index):


def parse_atom(tokenList, index):


def parse_list(tokenList, index):
    if(tokenList[index]!='('):
        print("Syntax Error, impossible state")
        sys.exit()
    print()

def parse_listBody(tokenList, index):


def parse_id(tokenList, index):
    #Impossible state, return error
    if(tokenList[index]=='(' or tokenList[index] ==')'):
        print("Syntax Error, impossible state")
        sys.exit()
    print("Token /'{0}/' Production: Atom -> id[{0}]").format(tokenList[index])
    index = index+1

def parse_int(tokenList, index):
    # Check if token is an integer. If not, print error
    if(tokenList[index].isdigit()):
        print("Token /'{0}/' Production: Atom -> int[{0}]").format(tokenList[index])
        index = index+1
        #Because this is a terminal, we don't call a further parse function
    else:
        print("Syntax Error")
        sys.exit()

def parse_eps(tokenList, index):
