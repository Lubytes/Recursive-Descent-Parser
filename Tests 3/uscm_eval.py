#!/local/bin/python

import sys, string, tokenize, re
tokens = iter( sys.stdin.read().split() )
cur_token = None
frames = []
print(tokens)

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


def add( a, b ):
  return a + b

def sub( a, b ):
  return a - b

def mul( a, b ):
  return a * b

def div( a, b ):
  return a / b


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

#Handles the define value
def do_define(l):
  global frames
  if(len(frames) == 0):
    frames.append({})
  var = l[0]
  result = replace_eval_vars(l[1:],frames)
  frames[0][var] = result
  print(var)

def do_let(l):
  global frames
  frames.insert(0,{})
  # Assign varialbes
  for i in l[0]:
    var = i[0]
    result = replace_eval_vars(i[1:], frames[1:])
    frames[0][var] = result
  # Execute Functions
  if(len(l) > 1):
    for j in l[1:]:
      do_eval(j)
  del frames[0]

def do_letstar(l):
  global frames
  frames.insert(0,{})
  # Assign varialbes
  for i in l[0]:
    var = i[0]
    result = replace_eval_vars(i[1:], frames)
    frames[0][var] = result
  # Execute Functions
  if(len(l) > 1):
    for j in l[1:]:
      do_eval(j)
  del frames[0]

#Replace values in the list with their frame values
def replace_eval_vars(l, frames):
  for i in l:
    if(not re.match(r"(|)|+|-|*\/|car|cdr|list|cons|'",i) or str(i).isdigit()):
      for j in frames:
        if(i in j):
          l = [w.replace('i',j[i]) for w in l]

  return do_eval(l)

def do_eval( a ):
  if isinstance( a, list ): # list  
    if len( a ) < 1:
      raise EvalError( '( )' )

    op = do_eval( a[0] )

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
      do_define(f[1:])
    elif op == "let":
      do_let(f[1:])
    elif op =="let*":
      do_letstar(f[1:])
    else:
      raise EvalError( 'unknown proc: ' + str( op ) ) 

    if a == None:
      raise EvalError( op )

    return a
  elif str(a).isdigit():   # int
    return a
  else:                    # id
    global frames
    return replace_eval_vars(a, frames)
    


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


