from LambdaTerm import LambdaTerm
from Abstraction import Abstraction
import Utility

class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    # create new application from two lambda terms
    def __init__(self, lambdaterm1, lambdaterm2):
        if isinstance(lambdaterm1, LambdaTerm) and isinstance(lambdaterm2, LambdaTerm):
            self.M = lambdaterm1
            self.N = lambdaterm2

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
            return Application(self.M.reduce, self.N.reduce)

    def frstring(self, string):
        s1, s2 = string.split(' ')
        self.M = Utility.fromstring(s1)
        self.N = Utility.fromstring(s2)
        return self

    # alpha conversion is conversion on components
    def alphaconv(self,rule=[],first=True):
        return Application(self.M.alphaconv(rule,first),self.N.alphaconv(rule,first))