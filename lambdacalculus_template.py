#!/usr/bin/env python3
lam = chr(955)

class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self, string):
        raise NotImplementedError

    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rule):
        raise NotImplementedError

    def reduce(self, rule=[]):
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
        if self.var in rule.keys():
            self.var = rule[self.var]

    def reduce(self, rule):
        if self.var == rule[0]:
            self.var = rule[1]
        # TODO? use substitute instead or change sub to list, self.substitute(self, rule)
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
        self.reduce(str(self), argument)

    # substitute lambdaterms when it does not mean alpha conversion
    def substitute(self, rule):
        if self.head.var not in rule.keys():
            # we should also check if this is a legitimate substitution
            self.body.substitute(rule)

    # continue reducing by passing on rule tuple or begin substitution
    def reduce(self, rule=[]):
        if len(rule) == 1: # no substitution yet, make a substitution rule from head and application rule
            rule = [self.head.var,rule[0]]
        self.body = self.body.reduce(rule)
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
        raise NotImplementedError

    # (start) bèta-reduce
    def reduce(self, rule=[]):
        rule = [self.N] # pass on second lambdaterm as rule
        self.M = self.M.reduce(rule)
        return self.M # return the reduced first lambdaterm


# create lambdaterms
# the following encodes the lambdaterm:  (((λx.(λy.x) z) u)
x = Variable("x")
print("Is x a variable?", type(x) == Variable)
u = Variable("u")
z = Variable("z")
abs1 = Abstraction("y", x)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(abs1)
print(abs2)

print(app1)
print(app2)

print(app1.reduce())
print(app2.reduce())