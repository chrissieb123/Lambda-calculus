#!/usr/bin/env python3
lam = chr(955)

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
        return str(self.var)

    def substitute(self, rule):
        if self.var in rule.keys():
            self.var = rule[self.var]


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        if isinstance(body, (LambdaTerm, Variable, Application, Abstraction)): # we require the body to be lambda term
            self.head = Variable(str(variable))
            self.body = body

    def __repr__(self):
        return str(lam) + str(self.head) + "." + str(self.body)

    def __str__(self):
        return str(lam) + str(self.head) + "." + str(self.body)

    # apply beta reduction when applying a lambda term to a lambda abstraction
    def __call__(self, argument):
        self.betareduction(str(self), argument)

    # substitute lambdaterms when it does not mean alpha conversion
    def substitute(self, rules):
        if self.head.var not in rules.keys():
            # we should also check if this is a legitimate substitution
            self.body.substitute(rules)

    def reduce(self, rules):
        self.body.reduce(self.argument)




class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""
    # We assume lambdaterm and argument are strings
    def __init__(self, lambdaterm, argument):
        self.M = lambdaterm
        self.N = argument

    def __repr__(self):
        return "(" + str(self.M) + str("") + str(self.N) + ")"

    def __str__(self):
        return "(" + str(self.M) + str("") + str(self.N) + ")"

    def substitute(self, rules):
        raise NotImplementedError

    def reduce(self, rules): # We can assume the lambdaterms aren't applications
        self.M.reduce(self.argument)


# the following encodes the lambdaterm:  (((λx.(λy.x) z) u)
x = Variable("x")
print(type(x) == Variable)
u = Variable("y")
z = Variable("z")
abs1 = Abstraction("y", x)
print(abs1)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(abs1)
print(abs2)

print(app1)
print(app2)