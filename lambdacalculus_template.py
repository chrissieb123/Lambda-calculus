#!/usr/bin/env python3
lam = chr(955)
print(lam)

class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self, string):
        raise NotImplementedError

    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rules):
        raise NotImplementedError

    def reduce(self, rules):
        raise NotImplementedError


class Variable(LambdaTerm):
    """Represents a variable."""
    # a variable must always be denoted by a string
    def __init__(self, symbol):
        self.var = str(symbol)

    def __repr__(self):
        return self.var

    def __str__(self):
        str(self.var)

    def substitute(self, rule):
        if self.var in rule.keys():
            self.var = rule[self.var]


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.head = variable
        self.body = body

    def __repr__(self):
        return str(lam) + str(self.head) + "." + str(self.body)

    def __str__(self):
        str(lam) + str(self.head) + "." + str(self.body)

    def __call__(self, argument):
        self.betareduction(str(self), argument)

    def substitute(self, rules):
        self.body.substitute()

    def reduce(self, rules):
        self.body.reduce(self.argument)




class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""
    # We assume lambdaterm and argument are strings
    def __init__(self, lambdaterm, argument):
        self.M = lambdaterm
        self.N = argument
        self.reduce

    def __repr__(self):
        return "(" + str(self.M) + str("") + str(self.N) + ")"

    def __str__(self):
        "(" + str(self.M) + str("") + str(self.N) + ")"

    def substitute(self, rules):
        raise NotImplementedError

    def reduce(self, rules): # We can assume the lambdaterms aren't applications
        self.M.reduce(self.argument)
