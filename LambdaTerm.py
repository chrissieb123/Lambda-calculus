class LambdaTerm:
    lam = chr(955)
    """Abstract Base Class for lambda terms."""

    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rule):
        raise NotImplementedError

    def reduce(self, rule=[]):
        raise NotImplementedError

    def frstring(self, string):
        raise NotImplementedError

    def alphaconv(self, rule=[], first=True):
        raise NotImplementedError