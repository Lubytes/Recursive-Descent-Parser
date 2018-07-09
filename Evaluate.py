# File:     Evaluate.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     July 4th, 2018
# Purpose:  Evaluation function for a recursive descent parser after the input list has been simplified


def eval(tree):
    result = ''
    iterator = 0
    if (tree):
        if (len(tree) <= 1):
            for item in tree:
                if (not isinstance(item, list)):
                    print(item)
                    exit()
        for totalTree in tree:
            result += evalInnerList(totalTree, iterator)
    print(result)

def evalInnerList(tree, iterator):
    result = ''
    #print(tree)
    for listItem in tree:
        #print(listItem)
        tempResult = ''
        #print(list(tree[iterator+1:]))
        if (listItem == '+'):
            tempResult, iterator = evalAdd(tree[iterator+1:], iterator)
        elif (listItem == '-'):
            tempResult, iterator = evalSub(tree[iterator+1:], iterator)
        elif (listItem == '*'):
            tempResult, iterator = evalMul(tree[iterator+1:], iterator)
        elif (listItem == '/'):
            tempResult, iterator = evalDiv(tree[iterator+1:], iterator)
        elif (listItem == 'list'):
            tempResult, iterator = evalList(tree[iterator+1:], iterator)
        elif (listItem == 'car'):
            tempResult, iterator = evalCar(tree[iterator+1:], iterator)

        result += tempResult
        iterator += 1
    return result

# Sum the integers
# eg ( + 1 2 3 ) evaluates to 6
def evalAdd(tree, iterator):
    result = 0
    for treeNode in tree:
        if(isinstance(treeNode,list)):
            listResult = evalInnerList(treeNode, iterator)
            result += float(listResult)
        else:
            result += float(treeNode)
        result = int(result)

    return str(result)+'\n', iterator

# Subtract the remaining integers from the first
# eg ( - 1 2 3 ) evaluates to -4
def evalSub(tree, iterator):
    result = float(tree[0])
    iterator += 1
    for treeNode in tree[1:]:

        if (isinstance(treeNode, list)):
            listResult = evalInnerList(treeNode, iterator)
            result -= float(listResult)
        else:
            result -= float(treeNode)
        result = int(result)
    result = int(result)

    return str(result)+'\n', iterator

# Multiply the integers
# eg ( * 2 3 4 ) evaluates to 24
def evalMul(tree, iterator):
    result = float(tree[0])
    iterator += 1
    for treeNode in tree[1:]:

        if (isinstance(treeNode, list)):
            listResult = evalInnerList(treeNode, iterator)
            result = result * float(listResult)
        else:
            result = result * float(treeNode)
        result = int(result)

    return str(result)+'\n', iterator

# Divide the first integer by each of the remaining integers
# eg ( / 12 2 3 ) evaluates to 2
def evalDiv(tree, iterator):
    result = int(tree[0])
    iterator += 1
    for treeNode in tree[1:]:

        if (isinstance(treeNode, list)):
            listResult = evalInnerList(treeNode, iterator)
            result = result / float(listResult)
        else:
            result = result / float(treeNode)
        result = int(result)

    return str(result)+'\n', iterator

# Return the head of the list
# eg ( car ' ( a b c ) ) evaluates to 'a'
def evalCar(tree, iterator):
    if tree:
        print(tree)
        statement = evalInnerList(tree)
        iterator += len(tree)
        return str(tree[0])+'\n', iterator
    else:
        print('Error, list out of index')

# remove the head and return the rest of the list
# eg ( cdr ' ( a b c ) ) evaluates to ( b c )
def evalCdr(tree, iterator):
    if tree:
        return str(tree[1:])+'\n'
    else:
        print('Error, list out of index')

# Returns a list of the atoms
# eg ( list a b c ) evaluates to ( a b c )
def evalList(tree, iterator):
    result = '( '
    if tree:
        for listItem in tree:
            result += listItem
            result += ' '
            iterator = iterator + 1
    result += ') '
    return result, iterator

# prepend atom to list
# eg ( cons a ' ( b c ) ) evaluates to ( a b c )
def evalCons(tree, atom, iterator):
    tree.insert(0, atom)
    return evalList(tree)

def evalId(tree, iterator):
    return 'id'