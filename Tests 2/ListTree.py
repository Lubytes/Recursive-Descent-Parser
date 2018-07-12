# File:     ListTree.py
# Authors:  Brandon Poole
# Date:     June 29th, 2018
# Purpose:  A shortform tree implementation using lists

#!/usr/bin/env python

class Tree:

    tree = []
    treeStack = []
    currList = tree

    def __init__(self):
        self.tree = []
        self.treeStack.append(self.tree)
        self.currList = self.tree

    def getHead(self):
        return self.tree

    def addItem(self, thing):
        self.currList.append(thing)
    
    def addNewList(self):
        tmp = []
        self.treeStack.append(tmp)
        self.currList.append(tmp)
        self.currList = tmp

    def finishList(self):
        #self.treeStack.pop
        del self.treeStack[-1]
        self.currList = self.treeStack[-1]




