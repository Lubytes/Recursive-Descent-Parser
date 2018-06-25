# File:     RDParse.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     June 21st, 2018
# Purpose:  A recursive descent parser for a specific grammar

import sys

file = sys.argv[1]
fileContents = open(file, "r")
tokens = fileContents.read().split()
#print(tokens)

parse_S(tokens)


def parse_S(stack):
    print("Token /'{0}/' Production: S -> Atoms").format(stack[-1])
    parse_atoms(stack)

def parse_atoms(stack):
    if(stack):
        parse_atom(stack)
        parse_atoms(stack)

def parse_atom(stack):
    if(stack[-1]=='\''):
        print("Token /'{0}/' Production: Atom -> ' Atom").format(stack[-1])
        stack.pop()
        parse_atom(stack)
    elif(stack[-1] == "("):
        print("Token /'{0}/' Production: Atom -> List").format(stack[-1])
        parse_list(stack)
    elif(stack[-1]=="+"):
        print("Token /'{0}/' Production: Atom -> id[{0}]").format(stack[-1])
        stack.pop()
    elif(stack[-1].isdigit()):
        print("Token /'{0}/' Production: Atom -> int[{0}]").format(stack[-1])
        stack.pop()

def parse_list(stack):
    if(stack[-1]!='('):
        print("Syntax Error")
        sys.exit()
    print("Token /'{0}/' Production: List -> ( ListBody )").format(stack[-1])
    stack.pop()
    parse_listBody(stack)

def parse_listBody(tokenList, index):


def parse_id(stack):
    #Impossible state, return error
    if(stack[-1]=='(' or stack[-1] ==')'):
        print("Syntax Error")
        sys.exit()
    print("Token /'{0}/' Production: Atom -> id[{0}]").format(stack[-1])


def parse_int(stack):
    # Check if token is an integer. If not, print error
    if(stack[-1].isdigit()):
        print("Token /'{0}/' Production: Atom -> int[{0}]").format(stack[-1])
        #Because this is a terminal, we don't call a further parse function
    else:
        print("Syntax Error")
        sys.exit()

def parse_eps(stack):
