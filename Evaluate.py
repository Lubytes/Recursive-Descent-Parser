# File:     Evaluate.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     July 4th, 2018
# Purpose:  Evaluation function for a recursive descent parser after the input list has been simplified



# NOTE: THIS IS ALL STILL IN PROGRESS LMAO

def Evaluate(tree):
    result = 0
    for listItem in tree:
        if(listItem == ')'):
            result = 0


    print(result)

# Sum the integers
# eg ( + 1 2 3 ) evaluates to 6
def evalAdd(tree):
    result = 0
    return result

# Subtract the remaining integers from the first
# eg ( - 1 2 3 ) evaluates to -4
def evalSub(tree):
    result = 0
    return result

# Multiply the integers
# eg ( * 2 3 4 ) evaluates to 24
def evalMul(tree):
    result = 0
    return result

# Divide the first integer by each of the remaining integers
# eg ( / 12 2 3 ) evaluates to 2
def evalDiv(tree):
    result = 0
    return result

# Return the head of the list
# eg ( car ' ( a b c ) ) evaluates to 'a'
def evalCar(tree):
    if tree:
        return tree[0]
    else:
        print('Error, list out of index')

# remove the head and return the rest of the list
# eg ( cdr ' ( a b c ) ) evaluates to ( b c )
def evalCdr(tree):
    if tree:
        return tree[1:]
    else:
        print('Error, list out of index')

# Returns a list of the atoms
# eg ( list a b c ) evaluates to ( a b c )
def evalList(tree):
    result = '( '
    if tree:
        for listItem in tree:
            result += listItem
            result += ' '
    result += ') '

# prepend atom to list
# eg ( cons a ' ( b c ) ) evaluates to ( a b c )
def evalCons(tree, atom):
    tree.insert(0, atom)
    return evalList(tree)