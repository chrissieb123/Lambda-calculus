from LambdaTerm import LambdaTerm
from Abstraction import Abstraction
import Utility
from copy import copy

class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    # create new application from two lambda terms
    def __init__(self, lambdaterm1, lambdaterm2):
        if isinstance(lambdaterm1, LambdaTerm) and isinstance(lambdaterm2, LambdaTerm):
            self.M = lambdaterm1
            self.N = lambdaterm2
        else:
            raise TypeError

    def __repr__(self):
        return "(" + str(self.M) + str(" ") + str(self.N) + ")"

    def __str__(self):
        return "(" + str(self.M) + str(" ") + str(self.N) + ")"

    def substitute(self, rule):
        return Application(self.M.substitute(rule), self.N.substitute(rule))

    def reduce(self, rule=[]):
        # assume M is a lambda abstraction and N is a lambda term
        if isinstance(self.M, Abstraction):
            return self.M(self.N)
        # reduce M and N independently
        else:
            return Application(self.M.reduce(), self.N.reduce())

    def frstring(self, string):
        # separate M and N at the last space
        separated = list(string.rpartition(" "))
        s1 = separated[0][1:] # remove the first bracket
        s2 = separated[2][:-1] # remove the last bracket
        
        self.M = Utility.fromstring(s1) # recursion on M
        self.N = Utility.fromstring(s2) # recursion on N

        return self

    # alpha conversion is conversion on components
    def alphaconv(self,rule=[],first=True):
        return Application(self.M.alphaconv(rule,first),self.N.alphaconv(rule,first))

    def freevar(self, headlist):
        hl = copy(headlist) # headlist should be the same for both sides (head in M doesn't affect N)
        return self.M.freevar(hl) + self.M.freevar(headlist)

    def tryalpha(self, rule, first=True):
        return Application(self.M.tryalpha(rule,first),self.N.tryalpha(rule,first))


