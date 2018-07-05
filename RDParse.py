# File:     RDParse.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     July 4th, 2018
# Purpose:  A recursive descent parser for a specific grammar

#!/usr/bin/env python

import sys
from ListTree import Tree

file = sys.argv[1]
fileContents = open(file, "r")
tokens = fileContents.read().split()
tokens.reverse()
tree = Tree()


def parse_S(stack, tree):
    if(stack):
        if(stack[-1]==")"):
            print("Syntax Error")
            sys.exit()
        else:
            pass
    else:
        pass
    parse_atoms(stack, tree)

def parse_atoms(stack, tree):
    if(not stack):
        pass
    elif(stack[-1]==")"):
        pass
    else:
        parse_atom(stack, tree)
        parse_atoms(stack, tree)


def parse_atom(stack, tree):
    if(stack[-1]==")"):
        print("Syntax Error")
        sys.exit()
    elif(stack[-1]=='\''):
        tree.addItem("\'")
        parse_atom(stack, tree)
    elif(stack[-1] == "("):
        tree.addNewList()
        parse_list(stack, tree)
    elif(stack[-1].isdigit()):
        tree.addItem(stack[-1])
        stack.pop()
    else:
        tree.addItem(stack[-1])
        stack.pop()

def parse_list(stack, tree):
    if(stack[-1]!='('):
        print("Syntax Error")
        sys.exit()
    stack.pop()
    parse_listBody(stack, tree)

    #check if close bracket
    if(stack):
        if(stack[-1] == ")"):
            tree.finishList()
            stack.pop()
        else:
            print("Syntax Error")
            sys.exit()
    else:
        print("Syntax Error")
        sys.exit()

def parse_listBody(stack, tree):
    if(stack):
        pass
    else:
        print("Token \'epsilon\' Production: ListBody -> Atoms")
        print("Token 'epsilon' Production: Atoms -> epsilon")
        print("Syntax Error")
        sys.exit()
    parse_atoms(stack, tree)
    #print("Token \'{0}\' Production: Atoms -> epsilon".format(stack[-1]))


parse_S(tokens, tree)
print(tree.getHead())