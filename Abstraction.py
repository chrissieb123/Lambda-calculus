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
        else:
            print(type(var), type(body))
            raise TypeError

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
        # alpha convert until reducible first (substitution rule 5)
        alph = self.alphreduce(rule)

        if str(self.head) != str(rule[0]): # check if this is a legitimate substitution
            return Abstraction(alph.head, alph.body.substitute(rule))
        else: return self

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

    # check if bèta-reduction can be done, do alpha-conversion if this is not the case, return converted abstraction
    def alphreduce(self, rule):
        boundvar1,freevar1,headlist1 = ([],[],[])
        boundvar2,freevar2,headlist2 = ([],[],[])
        self.findbound(boundvar1,freevar1,headlist1)
        #print("Lambda term: ", self, ", Boundvar: ", boundvar1 )
        rule[1].findbound(boundvar2,freevar2,headlist2)
        #print("Lambda term: ", rule[1], ", Freevar: ", freevar2)

        for i in range (0, len(boundvar1)):
            if boundvar1[i] in freevar2:
                # do alpha-conversion with the next variable character until it works
                j = 0
                while j < len(LambdaTerm.varchar):
                    try:
                        strvar = LambdaTerm.varchar[j]
                    except NotImplementedError:
                        j+=1
                        continue

                    vboundvar1 = Variable(boundvar1[i])
                    tryvar = Variable(strvar)

                    # alpha-convert, substituting the bound variable
                    return Abstraction(self.head.alphaconv([vboundvar1,tryvar]),self.body.alphaconv([vboundvar1,tryvar]))

        return self

    def findbound(self, boundvar, freevar, headlist):
        headlist.append(str(self.head)) # keep up a list with all the head variables

        return self.body.findbound(boundvar,freevar,headlist) # continue in the body

