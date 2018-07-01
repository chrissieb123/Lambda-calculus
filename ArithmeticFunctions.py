from Application import Application
from Abstraction import Abstraction
from Variable import Variable

(q,w,e,r,t,y,u,i,s,x,z) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"),Variable("s"),Variable("x"),Variable("z"))

abs1 = Abstraction(z,z)
zero = Abstraction(s,abs1)


app1 = Application(x, y)
app2 = Application(app1, z)
app3 = Application(y, app2)
print(app3)

labs1 = Abstraction(z, app3)
labs2 = Abstraction(y, labs1)
successor = Abstraction(x, labs2)


apppp = Application(successor, zero)

apppp = apppp.reduce()
print(type(apppp))
print(apppp)

apppp2 = apppp.reduce().reduce()
print(apppp2)

# the following implements y((λsz.z)yz)

class lambnumber(Abstraction):
    """These are numbers in lambda calculus representation, with their operators."""

    def lambnumbers(self, n, k=zero):
        if n != 0:
            k = Application(successor, k)
            return self.lambnumbers(n - 1, k)
        elif n == 0:
            return k.fullreduce()

    def __init__(self, number):
        lamb = self.lambnumbers(number)
        self.head = lamb.head
        self.body = lamb.body
        self.number = number

    def __repr__(self):
        return self.number

#appvar = Application(x,y)
#print("(x y) reduced: ", appvar.fullreduce())
twee = lambnumber(1)






print("------------------------- arithmetic")
#0 = (λsz.z)        =(λs.(λz.z)
#S = (λxyz.y(xyz))  =(λx.λy.λz.(y (x (y z)))