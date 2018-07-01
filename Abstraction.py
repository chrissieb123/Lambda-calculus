from LambdaTerm import LambdaTerm
from Variable import Variable
import Utility

class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    # list of bound variables
    boundvar = []

    # create an abstraction using a variable for the head and a lambda term for the body
    def __init__(self, var, body):
        if isinstance(var, Variable) and isinstance(body, LambdaTerm):
            self.head = var
            self.body = body

    def __repr__(self):
        return "(" + str(LambdaTerm.lam) + str(self.head) + "." + str(self.body) + ")"

    def __str__(self):
        return "(" + str(LambdaTerm.lam) + str(self.head) + "." + str(self.body) + ")"

    # apply beta reduction when applying a lambda term to a lambda abstraction
    def __call__(self, sub):
        rule = [self.head, sub]
        return self.body.substitute(rule)

    # substitute lambda terms when it does not mean alpha conversion
    def substitute(self, rule):
        if str(self.head) != str(rule[0]): # we should also check if this is a legitimate substitution
            return Abstraction(self.head, self.body.substitute(rule))

    def reduce(self, rule=[]):
        return Abstraction(self.head, self.body.reduce(rule))

    def frstring(self, string):
        # separate body and head at the first dot
        separated = list(string.partition("."))
        s1 = separated[0][1:] # remove the first bracket
        s2 = separated[2][:-1] # remove the last bracket
        
        self.head = s1.lstrip(LambdaTerm.lam) # the head is what is between the lambda and the dot
        self.body = Utility.fromstring(s2) # body after the dot
        
        # s1,s2 = string.split('.')
        # self.head = s1.lstrip(LambdaTerm.lam) # the head is what is between the lambda and the dot
        # self.body = Utility.fromstring(s2) # body after the dot
        return self

    def alphaconv(self, rule=[], first=True):
        # the input is incorrect if the substitute variable is ever bound
        if str(self.head) == str(rule[1]):
            print("Bad input.")
            raise NotImplementedError

        # ensure only the first bound occurence is converted
        # if this is the first abstraction that binds the to-be-substituted variable, set first to false
        if str(self.head) == str(rule[0]):
            if first:
                first = False
            else: # don't convert other (inner) abstractions that bind the variable
                return Abstraction(self.head,self.body)

        # convert the head (substitute the variable) and body
        return Abstraction(self.head.alphaconv(rule),self.body.alphaconv(rule,first))
