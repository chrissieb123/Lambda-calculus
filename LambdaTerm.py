class LambdaTerm:
    lam = chr(955)
    varchar = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

    """Abstract Base Class for lambda terms."""

    # define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rule):
        raise NotImplementedError

    # bèta-reduce (Application level reduce)
    def reduce(self, rule=[]):
        raise NotImplementedError

    def frstring(self, string):
        raise NotImplementedError

    # alpha-conversion
    def alphaconv(self, rule=[], first=True):
        raise NotImplementedError

    # returns the completely reduced version of this lambda term
    def fullreduce(self):
        lambdaterm = self
        # when a lambda term is not completely reduced a reduction will have an effect
        # in other words, the term and reduced term are not the same
        while str(lambdaterm.reduce()) != str(lambdaterm):
            lambdaterm = lambdaterm.reduce() # keep reducing until they are the sam
        return lambdaterm

    # find bound variables in the lambda term
    def findbound(self, boundvar, freevar, headlist):
        raise NotImplementedError