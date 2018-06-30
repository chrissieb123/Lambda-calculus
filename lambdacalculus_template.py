#!/usr/bin/env python3
lam = chr(955)


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    # define usable variable names
    varchars = ['u', 'x', 'y', 'z']

    @staticmethod
    def find_parentheses(s):
        """ Find and return the location of the matching parentheses pairs in s.
        Given a string, s, return a dictionary of start: end pairs giving the
        indices of the matching parentheses in s. Suitable exceptions are
        raised if s contains unbalanced parentheses.
        Source: https://scipython.com/blog/parenthesis-matching-in-python/
        """

        # The indices of the open parentheses are stored in a stack, implemented
        # as a list

        stack = []
        parentheses_locs = {}
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
            elif c == ')':
                try:
                    parentheses_locs[stack.pop()] = i
                except IndexError:
                    raise IndexError('Too many close parentheses at index {}'
                                                                    .format(i))
        if stack:
            raise IndexError('No matching close parenthesis to open parenthesis '
                             'at index {}'.format(stack.pop()))
        return parentheses_locs
    
   
    # returns a lambda term created from the string argument
    # categorize lambda terms using brackets, working from outside in
    @staticmethod
    def fromstring(string):
        # define characters for later convenience
        lambdastring = ''
        l = '('
        r = ')'
        
        # collect index pairs for every bracket
        for s in enumerate(string, start=1):
            # find parentheses indices
            try:
                parentheses_locs = LambdaTerm.find_parentheses(s)
                indexpairs = sorted([(k,v) for k, v in parentheses_locs.items()])
            # parentheses do not match
            except IndexError as e:
                print(str(e))
        
        # define indices of the second-to-last right parenthesis and corresponding left parenthesis
        rpair = indexpairs[-2][1]
        lpair = indexpairs[-2][0]
        
        # application if space after second-to-last right bracket
        if string[rpair+1] == ' ':
            lambdastring = Application.frstring(string)
        # abstraction
        elif string[lpair+1] == l and string[lpair+2] == lam:
            lambdastring = Abstraction.frstring()
        # variable if all characters are correct
        else:
            for i in range(len(string)):
                if string[i] not in varchars:
                    raise NameError
        
        return lambdastring
   
        '''
        # find most right bracket after removing outer brackets
        string.strip(r)
        nextr = string.rfind(r)
        
        # application if space after bracket
        if string[nextr+1] == ' ':
            lamdbdat = Application.frstring(string)
        # 
        else:
            # the corresponding left bracket
            nextl = string[len(string)-nextr-1]

            # abstraction if (λ follows bracket
            if string[nextl+1] == l and string[nextl+2] == lam:
                lambdat = Abstraction.frstring()
        # variabele als alle karakters correct zijn
        else: # Correct variable if all the characters in it are correct characters
                for i in range(len(string)):
                    if string[i] not in varchars: # if there is an incorrect character, stop and raise exception
                        raise NameError
                lambdat = Variable(string)

        return lambdat
        '''
     
    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rule):
        raise NotImplementedError

    def reduce(self, rule=[]):
        raise NotImplementedError

    def frstring(self,string):
        raise NotImplementedError

    def alphaconv(self,rule=[]):
        raise NotImplementedError

    def error():
        return "Wrong input."

class Variable(LambdaTerm):
    """Represents a variable."""
    # a variable must always be denoted by a string
    def __init__(self, symbol):
        self.var = str(symbol)

    def __repr__(self):
        return self.var

    def __str__(self):
        return self.var

    def substitute(self, rule):
        if self.var == rule[0].var:
            return rule[1]
        else:
            return self

    def reduce(self, rule=[]):
        return self

    def alphaconv(self, rule=[]):
        return self.substitute(rule)


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    # list of bound variables
    boundvar = []

    # create an abstraction using a variable for the head and a lambda term for the body
    def __init__(self, var, body):
        # check if the body is a lambda term
        if isinstance(body, (LambdaTerm, Variable, Application, Abstraction)) \
                and isinstance(var, Variable):
            self.head = var
            self.body = body

    def __repr__(self):
        return "(" + str(lam) + str(self.head) + "." + str(self.body) + ")"

    def __str__(self):
        return "(" + str(lam) + str(self.head) + "." + str(self.body) + ")"

    # apply beta reduction when applying a lambda term to a lambda abstraction
    def __call__(self, argument):
        forcall = Application(self, argument)
        forcall.reduce()

    # substitute lambda terms when it does not mean alpha conversion
    def substitute(self, rule):
        if self.head.var != rule[0]: # we should also check if this is a legitimate substitution
            return Abstraction(self.head, self.body.substitute(rule))

    def reduce(self, rule=[]):
        return Abstraction(self.head, self.body.reduce(rule))

    def frstring(self, string):
        s1,s2 = string.split('.')
        self.head = s1.lstrip(lam) # the head is what is between the lambda and the dot
        self.body = self.body.fromstring(s2) # body after the dot
        return self

    def alphaconv(self, rule=[]):
        boundvar = [] # search for bound variables
        self.findbound(boundvar)
        # to do, replace condition below with: "intersection between FV(rule[1]) and boundvar = empty"
        if rule[1] not in boundvar: # only convert if var to substitute it with is not bound
            return Abstraction(self.head.alphaconv(rule), self.body.alphaconv(rule))
        else:
            return (LambdaTerm.error())

    def findbound(self, boundvar):
        boundvar.append(self.head) # head is bound

        if not isinstance(self.body, Variable): # add bound variables until body is variable
            self.body.findbound(boundvar)

class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    # create new application from two lambda terms
    def __init__(self, lambdaterm, argument):
        self.M = lambdaterm
        self.N = argument

    def __repr__(self):
        return "(" + str(self.M) + str(" ") + str(self.N) + ")"

    def __str__(self):
        return "(" + str(self.M) + str(" ") + str(self.N) + ")"

    def substitute(self, rule):
        return Application(self.M.substitute(rule), self.N.substitute(rule))

    def reduce(self, rule=[]):
        # assume M is a lambda abstraction and N is a lambda term
        if isinstance(self.M, Abstraction):
            rule = [self.M.head, self.N]
            return self.M.body.substitute(rule)
        # reduce M and N independently
        else:
            return Application(self.M.reduce, self.N.reduce)

    def frstring(self, string):
        s1, s2 = string.split(' ')
        self.M = self.M.fromstring(s1)
        self.N = self.N.fromstring(s2)
        return self

    def alphaconv(self,rule=[]):
        return self

    def findbound(self,boundvar):
        # assume M is a lambda abstraction and N is a lambda term
        if isinstance(self.M, Abstraction):
            self.M.findbound(boundvar)

# create lambda terms
# the following implements the lambda term:  (((λx.(λy.x) z) u)
print("Bèta Reduction")
(q,w,e,r,t,y,u,i,s) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"),Variable("s"))
x = Variable("x")
#print("Is x a variable?", type(x) == Variable)
z = Variable("z")

abs1 = Abstraction(y, x)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(app1)

print(app1.reduce())

# this implements ((λx.x) u)
print("------------------------- identity function")
identity = Abstraction(x, x)

appliopid = Application(identity, u)

print(identity)
print(appliopid)

print(appliopid.reduce())


# this implements ((λx.x) (λu.z))
print("------------------------- two lambda abstractions in an application")
constant = Abstraction(u, z)

appliopconst = Application(identity, constant)

print(constant)
print(appliopconst)

print(appliopconst.reduce())

# this implements ((λx.((λq.q) (λi.x)) (λu.z)), should print to (λi.(λu.z))
print("------------------------- complicated example (application as body of abstraction)")

VB1abs = Abstraction(q,q)
VB2abs = Abstraction(i,x)
VB3abs = constant

VB1app = Application(VB1abs,VB2abs)

VB4abs = Abstraction(x,VB1app)

VB2app = Application(VB4abs, VB3abs)

print(VB2app)

def reducechecker(lambterm):
    if str(lambterm.reduce()) != str(lambterm):
        return reducechecker(lambterm.reduce())
    else:
        return lambterm


print(reducechecker(VB2app))


# print(LambdaTerm.fromstring("(((λx.(λy.x)) z) u)"))

print("Alpha Conversion")
print("------------------------- identity")
print(identity)
if (isinstance(identity, Abstraction)):
    print(identity.alphaconv([identity.head,z]))

# the following implements ((λx.λy.x) y), this should be reduced to (λz.y) or some other variable than z (but not y)
print("------------------------- exception")
alphabs1 = Abstraction(y,x)
alphabs2 = Abstraction(x, alphabs1)

print(alphabs2)
print(alphabs2.alphaconv([alphabs2.head,y]))

#alphapp1 = Application(vb2abs, y)

#print(alphapp1.reduce())

# We implement the lambda abstraction : (λx.(λx.x)), alphaconversion x -> y on outer lambda we get (λy.(λx.x))
print("------------------------- exception")
alphabs1 = Abstraction(x,x)
alphabs2 = Abstraction(x,alphabs1)

print(alphabs2)

print(alphabs2.alphaconv([alphabs2.head, z])) #TODO

print("------------------------- arithmetic")
#0 = (λsz.z)        =(λs.(λz.z)
#S = (λxyz.y(xyz))  =(λx.λy.λz.(y (x (y z)))


abs1 = Abstraction(z,z)
zero = Abstraction(s,abs1)

app1 = Application(y, z)
app2 = Application(x, app1)
app3 = Application(y, app2)

labs1 = Abstraction(z, app3)
labs2 = Abstraction(y, labs1)
successor = Abstraction(x, labs2)
lijst =[]
def lambnumber(number, n,s=[]):
    if n != 0:
        s = Application(successor, number)
        lambnumber(s, n - 1, s)
    else:
        lijst.append(s)

lambnumber(zero,3)
s = lijst[0]

print(s.reduce())