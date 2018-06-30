#!/usr/bin/env python3
lam = chr(955)


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    varchars = ['u', 'x', 'y', 'z']

    # returns a lambda term created from the string argument
    # categorize lambda terms using brackets, working from outside in
    @staticmethod
    def fromstring(string):
        lambdat = ''
        l = '('
        r = ')'
        # find most right bracket after removing outer brackets
        string.strip(r)
        nextr = string.rfind(r)
        if string[nextr+1] == ' ': # Application if space before bracket
            lamdbdat = Application.frstring(string)

        else:
            nextl = string[len(string)-nextr-1] # The corresponding left bracket

            if string[nextl+1] == l and string[nextl+2] == lam: # Abstraction if (λ follows bracket
                lambdat = Abstraction.frstring()

            else: # Correct variable if all the characters in it are correct characters
                for i in range(len(string)):
                    if string[i] not in varchars: # if there is an incorrect character, stop and raise exception
                        raise NameError
                lambdat = Variable(string)

        return lambdat

    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rule):
        raise NotImplementedError

    def reduce(self, rule=[]):
        raise NotImplementedError

    def frstring(self,string):
        raise NotImplementedError


class Variable(LambdaTerm):
    """Represents a variable."""
    # a variable must always be denoted by a string
    def __init__(self, symbol):
        self.var = str(symbol)

    def __repr__(self):
        return self.var

    def __str__(self):
        return str(self.var)

    def substitute(self, rule):
        if self.var == rule[0]:
            return rule[1]
        else:
            return self

    def reduce(self, rule=[]):
        return self

class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    # create an abstraction using the head variable in string format and the body as a lambda term
    def __init__(self, varstr, body):
        if isinstance(body, (LambdaTerm, Variable, Application, Abstraction)): # we require the body to be lambda term
            self.head = Variable(str(varstr))
            self.body = body

    def __repr__(self):
        return "(" + str(lam) + str(self.head) + "." + str(self.body) + ")"

    def __str__(self):
        return "(" + str(lam) + str(self.head) + "." + str(self.body) + ")"

    # apply beta reduction when applying a lambda term to a lambda abstraction
    def __call__(self, argument):
        forcal = Application(self, argument)
        forcal.reduce()

    # substitute lambdaterms when it does not mean alpha conversion
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


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    # create new application from two lambdaterms
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
        if isinstance(self.M, Abstraction): # assume M is a lambda abstraction and N is a lambdaterm
            rule = [str(self.M.head), self.N]
            return self.M.body.substitute(rule)
        else: # reduce individually M and N
            return Application(self.M.reduce, self.N.reduce)

    def frstring(self, string):
        s1, s2 = string.split(' ')
        self.M = self.M.fromstring(s1)
        self.N = self.N.fromstring(s2)
        return self


# create lambdaterms
# the following implements the lambdaterm:  (((λx.(λy.x) z) u)
print("------------------------- ")
(q,w,e,r,t,y,u,i) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"))
x = Variable("x")
#print("Is x a variable?", type(x) == Variable)
z = Variable("z")

abs1 = Abstraction("y", x)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(app1)

print(app1.reduce())

# print(LambdaTerm.fromstring("((((λx.(λy.x)) z) u)"))

# this implements ((λx.x) u)
print("------------------------- identiteit voorbeeld")
identitity = Abstraction(x, x)

appliopid = Application(identitity, u)

print(identitity)
print(appliopid)

print(appliopid.reduce())


# this implements ((λx.x) (λu.z))
print("------------------------- twee lambda abstracties in een applicatie")
constant = Abstraction(u, z)

appliopconst = Application(identitity, constant)

print(constant)
print(appliopconst)

print(appliopconst.reduce())

# this implements ((λx.((λq.q) (λi.x)) (λu.z)), should print to (λi.(λu.z))
print("------------------------- complex voorbeeld")

VB1abs = Abstraction(q,q)
VB2abs = Abstraction(i,x)
VB3abs = constant

VB1app = Application(VB1abs,VB2abs)

VB4abs = Abstraction(x,VB1app)

VB2app = Application(VB4abs, VB3abs)

print(VB2app)
print(VB2app.reduce().reduce().reduce().reduce())


def reducechecker(lambterm):
    if str(lambterm.reduce()) != str(lambterm):
        return reducechecker(lambterm.reduce())
    else:
        return lambterm


print(reducechecker(VB2app))
