from Application import Application
from Abstraction import Abstraction
from Variable import Variable

# we use less cumbersome notation as defined in the report

# we first inititialise a few many used functions and a list of workable variables
(q,w,e,r,t,y,u,i,s,x,z,a,b,c,p) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"),Variable("s"),Variable("x"),Variable("z"),Variable("a"),Variable("b"),Variable("c"), Variable("p"))
zidentity = Abstraction(z, z)
absxy = Abstraction(x, y)
absyz = Abstraction(y,z)

# the following implements the lambdaterm zero: (λsz.z)
abs1 = Abstraction(z,z)
zero = Abstraction(s,abs1)

# the following implements the successor function (the +1 operator): (λxyz.y(xyz))
sapp1 = Application(x, y)
sapp2 = Application(sapp1, z)
sapp3 = Application(y, sapp2)

sabs1 = Abstraction(z, sapp3)
sabs2 = Abstraction(y, sabs1)
successor = Abstraction(x, sabs2)

# the following implements the multiplication operator: (λxyz.x(yz))
mapp1 = Application(b,c)
mapp2 = Application(a,mapp1)

mabs1 = Abstraction(c,mapp2)
mabs2 = Abstraction(b,mabs1)
multiplication = Abstraction(a,mabs2)


# the following implements the True operator, (λxy.x))
tabs1 = Abstraction(y,x)
lambTrue = Abstraction(x,tabs1)
# the following implements the False operator, (λxy.y))
fabs1 = Abstraction(y,y)
lambFalse = Abstraction(x,fabs1)


#  the following implements the And operator, λxy.xy(λuv.v) or with eta-equivalence, λxy.xyF
aapp1 = Application(x,y)
aapp2 = Application(aapp1,lambFalse)
aabs1 = Abstraction(y,aapp2)
lambAnd = Abstraction(x,aabs1)

#  the following implements the Or operator, λxy.x(λuv.u)y or with eta-equivalence, λxy.xTy
oapp1 = Application(x,lambTrue)
oapp2 = Application(oapp1,y)
oabs1 = Abstraction(y,oapp2)
lambOr = Abstraction(x,oabs1)

#  the following implements the Not operator, λx.x(λuv.v)(λab.a) or with eta-equivalence, λxy.xFT
napp1 = Application(x,lambFalse)
napp2 = Application(napp1,lambTrue)
nabs1 = Abstraction(y,napp2)
lambNot = Abstraction(x,nabs1)


class lambnumber(Abstraction):
    """These are numbers in lambda calculus representation, with their operators."""

    def lambnumbers(self, n, k=zero): # n is amount extra to add, k is starting value
        if n != 0:
            k = successor(k)
            return self.lambnumbers(n - 1, k)
        elif n == 0:
            return k.fullreduce()

    def __init__(self, number, begin = zero):
        # lamb is the lambdaterm that indicates a number
        lamb = self.lambnumbers(number, begin)
        self.head = lamb.head
        self.body = lamb.body
        self.number = number

    def __repr__(self):
        return self.number

    def __add__(self, other):
        return lambnumber(self.number, other)

    def __mul__(self, other):
        d = Application(multiplication, self)
        d = Application(d, other)
        d = d.fullreduce()

        dummy = lambnumber(0)
        dummy.head = d.head
        dummy.body = d.body
        dummy.number = self.number * other.number
        return dummy



zero = lambnumber(0)
een = lambnumber(1)
