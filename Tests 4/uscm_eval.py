#!/local/bin/python

# File:     uscm_eval.py
# Authors:  Brandon Poole, John Phillips, Aqeb Hamdan
# Date:     July 13th, 2018
# Purpose:  Evaluate scheme parsings with variable definitions 

import sys, string, tokenize

tokens = iter( sys.stdin.read().split() )
cur_token = None
frames = [{'+': '+', '-': '-', '*': '*','/': '/', 'car': 'car','cdr': 'cdr','list': 'list','cons': 'cons',"'": "'",'define': 'define','let': 'let','let*': 'let*', 'set!': 'set!', 'lambda': 'lambda'}]

#Closure Object
class Closure:
  params = []
  function = []
  frameLength = None

  def __init__(self, params, function, frameLength):
    self.params = params
    self.function = function
    self.frameLength = frameLength

  def getParams(self):
    return self.params

  def getFunction(self):
    return self.function

  def getFrameLength(self):
    return self.frameLength


class ParseError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class EvalError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def lookahead():
  global cur_token

  if cur_token == None:
    try:
      cur_token = next(tokens)
    except:
      cur_token = None

  return cur_token


def next_token():
  global cur_token

  n = lookahead()
  cur_token = None
  return n



# ===================
# Evaluation
# ===================

# ===================
# New Methods
# ===================

# Lookup value from key in frames
def lookup(a):
  global frames
  
  value = None
  for frame in frames:
    if(a in frame):
      return frame[a]
      
  
  return False
  

def do_define(l):
  global frames
  var = l[0]
  # do stuff with l[1]
  result = do_eval(l[1:][0])

  # end
  frames[0][var] = result
  return var

def do_let(l):
  global frames
  tmpDict = {}
  for i in l[0]:
    var = i[0]
    result = do_eval(i[1:][0])
    tmpDict[var] = result
  frames.insert(0,tmpDict)
  
  for i in l[1:]:
    result = do_eval(i)
  
  del frames[0]
  return result

def do_letstar(l):
  global frames
  frames.insert(0,{})
  for i in l[0]:
    var = i[0]
    result = do_eval(i[1:][0])
    frames[0][var] = result
  
  for i in l[1:]:
    result = do_eval(i)
  
  del frames[0]
  return result

def do_set(l):
  global frames
  
  for frame in frames:
    if(l[0] in frame):
      tmp = frame[l[0]]
      frame[l[0]] = l[1]
      break

  return tmp

# l[0] list of parameters
# l[l:] list of functions
def do_lambda(l):
  global frames
  return Closure(l[0],l[1:],len(frames))

# TODO: enclose in frame for define (it's cool)
def do_closure(c,l):
  global frames

  # Set up scope
  tmp = []
  while(c.getFrameLength() != len(frames)):
    tmp.append(frames[0])
    del frames[0]

  # New frame
  frames.insert(0,{})
  counter = 0
  for i in c.getParams():
    do_eval(['define',i,l[counter]])
    counter += 1

  # Execute each part of closure
  for i in c.getFunction():
    result = do_eval(i)

  del frames[0]
  for i in tmp:
    frames.insert(0,i)

  return result

    
  

# ===================
# End New Methods
# ===================


def add( a, b ):
  return a + b

def sub( a, b ):
  return a - b

def mul( a, b ):
  return a * b

def div( a, b ):
  return a // b


def do_arith_op( op, l ):
  if len( l ) < 1:
    raise EvalError( op )

  r = do_eval( l[0] )
  if not isinstance( r, int ):
    raise EvalError( op )

  for o in l[1:]:
    i = do_eval( o )
    if isinstance( i, int ):
      r = op( r, i )
    else:
      raise EvalError( op )
 
  return r


def do_eval( a ):
  #print(a)
  if isinstance( a, list ): # list  
    if len( a ) < 1:
      raise EvalError( '( )' )

    op = do_eval(a[0])
    f = a
    a = None

    if op == "+":
      a = do_arith_op( add, f[1:] )
    elif op == "-":
      a = do_arith_op( sub, f[1:] )
    elif op == "*":
      a = do_arith_op( mul, f[1:] )
    elif op == "/":
      a = do_arith_op( div, f[1:] )
    elif op == "'":
      if len( f ) > 1:
        a = f[1]
    elif op == "car":
      if len( f ) > 1:
        l = do_eval( f[1] )
        if isinstance( l, list ) and len( l ) > 0:
          a = l[0]
    elif op == "cdr":
      if len( f ) > 1:
        l = do_eval( f[1] )
        if isinstance( l, list ) and len( l ) > 0:
          a = l[1:]
    elif op == "cons":
      if len( f ) > 2:
        h = do_eval( f[1] )
        t = do_eval( f[2] )
        if isinstance( t, list ):
          a = [ h ] + t
    elif op == "list":
      a = []
      for b in f[1:]:
        a = a + [do_eval( b )]
    elif op == "define":
      a = do_define(f[1:])
    elif op == "let":
      a = do_let(f[1:])
    elif op =="let*":
      a = do_letstar(f[1:])
    elif op == "set!":
      a = do_set(f[1:])
    elif op == "lambda":
      a = do_lambda(f[1:])
    elif(isinstance(op,Closure)):
      # print("found a closure")
      # print(f)
      a = do_closure(lookup(f[0]),f[1:])
    else:
      raise EvalError( 'unknown proc: ' + str( op ) ) 
    if a == None:
      raise EvalError( op )
    return a

  elif str(a).isdigit():   # int
    return a
  else:                    # id
    return lookup(a)







# ===================
# End Evaluation
# ===================





def parseS():
  tok = lookahead()
    
  if tok != ")":
    return parseAtoms()
  else:
    raise ParseError( 'S' )
  

def parseAtoms():
  tok = lookahead()
    
  if tok == None or tok == ")":
    return []
  else:
    return parseAtom() + parseAtoms()
   

def parseAtom():
  tok = lookahead()
    
  if tok == "(":
    l = [ parseList() ]
  elif tok == "'":             # quote
    next_token()
    l = [[tok] + parseAtom()]
  elif( str(tok).isdigit() ):  # integer
    next_token()
    l = [int( tok )]
  elif tok != None:         # identifier
    next_token()
    l = [tok]
  else:
    raise ParseError( 'Atom' )

  return l


def parseList():
  tok = next_token()

  if tok == '(': 
    l = parseListBody()
    tok = next_token()
    if tok != ")":
      raise ParseError( 'List' )
  else:
    raise ParseError( 'List' )

  return l


def parseListBody():
  tok = lookahead()
  l = []

  if tok != None:
    return l + parseAtoms()
  else:
    raise ParseError( 'ListBody' )


def atom2str( l ):
  if isinstance( l, list ):
    if len( l ) < 1: 
      return "( )"
    elif l[0] == "'":
      return "' " + atom2str( l[1] )
    
    s = "("
    for a in l:
      s = s + " " + atom2str( a )
    return s + " )"
  else:
    return str( l )
 
def eval_result( l ):
  for a in l:
    print(atom2str( do_eval( a ) ))
 
try:
  l = parseS()
  if lookahead() != None:
    raise ParseError( 'S' )
  eval_result( l )
except ParseError as p:
  print("Syntax Error while parsing " + str( p ) + " production")
except EvalError as p:
  print("Evaluation Error while evaluating " + str( p ))


