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
        if str(self.head) != str(rule[0]): # check if this is a legitimate substitution
            # alpha convert until reducible first (substitution rule 5)
            alph = self.tryalpha(rule)
            print("alph: ", alph)
            return Abstraction(alph.head, alph.body.substitute(rule))
        else:
            return self

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

    def alphaconv(self, rule, first=True):
        # ensure only the first bound occurence is converted
        # if this is the first abstraction that binds the to-be-substituted variable, set first to false
        if str(self.head) == str(rule[0]):
            if first:
                first = False
            else: # don't convert other (inner) abstractions that bind the variable
                return Abstraction(self.head,self.body)

        # convert the head (substitute the variable) and body
        return Abstraction(self.head.alphaconv(rule),self.body.alphaconv(rule,first))

    # check if alpha-conversion is ok, do alpha-conversion on the head to a different variable if not the case, return converted abstraction
    def tryalpha(self,rule,first=True):
        newrule0 = rule[0]
        newrule1 = rule[1]

        # do alpha-conversion with the next variable character until it works
        chars = LambdaTerm.varchar
        for j in range (0,len(chars)):
            print("rule: ", [newrule0,newrule1])
            print("alphconv: ", self.alphaconv([newrule0,newrule1]))
            print("varlist: ", self.varlist())

            if newrule1 not in self.varlist():
                if first:
                    first = False
                    newrule0 = self.head
                newrule1 = Variable(chars[j]) # make variable from string and use as new substitute
                continue
            else:
                break

        if first: # nothing wrong with the alpha-conversion
            return self
        else: # return the alpha-equivalent alpha-converted abstraction
            return self.alphaconv([newrule0,newrule1])

    def freevar(self, headlist):
        headlist.append(str(self.head)) # keep up a list with all the head variables
        return self.body.freevar(headlist) # continue in the body

    def varlist(self):
        return self.body.varlist()

    """
        # check if alpha-conversion is ok, do alpha-conversion on the head to a different variable if not the case, return converted abstraction
        def tryalpha(self, rule,first=True):
            newrule0 = rule[0]
            newrule1 = rule[1]
            # do alpha-conversion with the next variable character until it works
            chars = LambdaTerm.varchar
            for j in range (0,len(chars)):
                print("rule: ", [newrule0,newrule1])
                print("alphconv: ", self.alphaconv([newrule0,newrule1]))

                cont = False

                # the input is incorrect if the head is in free variables of the substitute
                if str(self.head) in newrule1.freevar([]):
                    print("Bad input: {} is in {}".format(self.head, newrule1.freevar([])))
                    if first:
                        first = False
                        newrule0 = self.head
                    cont = True

                if (not first) and str(newrule1) in self.body.freevar([]): # new head shouldn't bind variables
                    print("New head binds free var: {} in {}".format(newrule1,self.body.freevar([])))
                    cont = True

                if cont:
                    if first:
                        first = False
                        newrule0 = self.head
                    newrule1 = Variable(chars[j]) # make variable from string and use as new substitute
                    continue
                else:
                    break

            if first: # nothing wrong with the alpha-conversion
                return self
            else: # return the alpha-equivalent alpha-converted abstraction
                return self.alphaconv([newrule0,newrule1])
    """