from LambdaTerm import LambdaTerm

class Variable(LambdaTerm):
    """Represents a variable."""
    # a variable must always be denoted by a string
    def __init__(self, symbol):
        self.var = str(symbol)

    def __repr__(self):
        return self.var

    def __str__(self):
        return self.var

    # substitute if variable matches rule
    def substitute(self, rule):
        if self.var == rule[0].var:
            return rule[1]
        else:
            return self

    def reduce(self, rule=[]):
        return self

    def alphaconv(self, rule, first=True):
        return self.substitute(rule)

    def freevar(self, headlist):
        strvar = self.var
        if strvar not in headlist:  # a variable is bound if it is in one of the previous head variables
            return [strvar]
        else:
            return []

    def tryalpha(self, rule, first=True):
        return self.alphaconv(rule,first)