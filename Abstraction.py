from LambdaTerm import LambdaTerm
from Variable import Variable
import Utility

class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    # list of bound variables
    boundvar = []

    # create an abstraction using a variable for the head and a lambda term for the body
    def __init__(self, var, body):
        # check if the body is a lambda term
        if isinstance(body, LambdaTerm) \
                and isinstance(var, Variable):
            self.head = var
            self.body = body

    def __repr__(self):
        return "(" + str(LambdaTerm.lam) + str(self.head) + "." + str(self.body) + ")"

    def __str__(self):
        return "(" + str(LambdaTerm.lam) + str(self.head) + "." + str(self.body) + ")"

    """# apply beta reduction when applying a lambda term to a lambda abstraction
    def __call__(self, argument):
        forcall = Application(self, argument)
        forcall.reduce()"""

    # substitute lambda terms when it does not mean alpha conversion
    def substitute(self, rule):
        if self.head.var != rule[0]: # we should also check if this is a legitimate substitution
            return Abstraction(self.head, self.body.substitute(rule))

    def reduce(self, rule=[]):
        return Abstraction(self.head, self.body.reduce(rule))

    def frstring(self, string):
        s1,s2 = string.split('.')
        self.head = s1.lstrip(LambdaTerm.lam) # the head is what is between the lambda and the dot
        self.body = Utility.fromstring(s2) # body after the dot
        return self

    def alphaconv(self, rule=[]):
        boundvar = [] # search for bound variables
        self.findbound(boundvar)
        # to do, replace condition below with: "intersection between FV(rule[1]) and boundvar = empty"
        if rule[1] not in boundvar: # only convert if var to substitute it with is not bound
            return Abstraction(self.head.alphaconv(rule), self.body.alphaconv(rule))
        else:
            return (Utility.error())

    def findbound(self, boundvar):
        boundvar.append(self.head) # head is bound

        if not isinstance(self.body, Variable): # add bound variables until body is variable
            self.body.findbound(boundvar)