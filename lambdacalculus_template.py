#!/usr/bin/env python3
lam = chr(955)
print(lam)

class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self, string):
        """Construct a lambda term from a string."""
        """# if string contains space: then self = lambdappl(before space, after space)
        if 4==5:
            print("lol")

        # if string no space but has lambda: then self = lambaabs(first after lambda, all after dot)
        elif string[1] == "l":
            self = Abstraction(string[1], string[3::])

        # if string begins with alphabet and no lambda or space: then self = var(string)
        elif string[1] == "z":
            self = Variable(string[1::-2])

        # else this string is no lambda expression at all, return kan niet
        else:
            print("This is no Lambaterm, please repair any defects")"""
        raise NotImplementedError

    # Define a substitution function, which receives a lambda term and a dictionary of replacements
    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        # lambdaterms dont have .get function (yet) so we use the string representation
        listsubstitute = list(str(self))

        # we substitute occurrences for keys in listsutbstitute for their values
        for i in range(0, len(listsubstitute)):
            if rules.get(listsubstitute[i]) is not None:
                listsubstitute[i] = rules[listsubstitute[i]]
        return ''.join(listsubstitute)

    def betareduction(self, lambdaterm, application):
        # our input will be in string representation, which is usefull for iterables

        # Firstly we have to lambda convert the term if neccessary

        # seperate body and head
        seperate = list(lambdaterm.partition("."))

        head = seperate[0]
        body = list(seperate[2])

        # find variable in expression λx.M
        variable = list(head.partition("λ"))[2]

        # substitution in the body for the variable
        for i in range(0, len(body)):
            if body[i] == variable:
                body[i] = application

        # return body as a list
        return ''.join(body)


class Variable(LambdaTerm):
    """Represents a variable."""
    # a variable must always be denoted by a string
    def __init__(self, symbol):
        self.var = str(symbol)

    def __repr__(self):
        return self.var

    def __str__(self):
        str(self.var)

    def substitute(self, rule):
        if self.var in rule.keys():
            self.var = rule[self.var]


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.head = variable
        self.body = body

    def __repr__(self):
        return str(lam) + str(self.head) + "." + str(self.body)

    def __str__(self):
        str(lam) + str(self.head) + "." + str(self.body)

    def __call__(self, argument):
        self.betareduction(str(self), argument)

    def substitute(self, rules):
        self.body.substitute()


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""
    # We assume lambdaterm and argument are strings
    def __init__(self, lambdaterm, argument):
        self.M = lambdaterm
        self.N = argument

    def __repr__(self):
        return "(" + str(self.M) + str("") + str(self.N) + ")"

    def __str__(self):
        "(" + str(self.M) + str("") + str(self.N) + ")"

    def substitute(self, rules):
        raise NotImplementedError

    def reduce(self):
        self.function.substitute(self.argument)
