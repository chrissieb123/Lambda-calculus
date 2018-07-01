#!/usr/bin/env python3
from Application import Application
from Abstraction import Abstraction
from Variable import Variable

# create lambda terms
# the following implements the lambda term:  (((λx.(λy.x) z) u)
print("Bèta Reduction")
(q,w,e,r,t,y,u,i,s,x,z) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"),Variable("s"),Variable("x"),Variable("z"))
#print("Is x a variable?", type(x) == Variable)

abs1 = Abstraction(y, x)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(app1)

print(app1.reduce())

# this implements ((λx.x) u)
print("------------------------- identity function")
identity = Abstraction(x, x)

appliopid = Application(identity, u)

print(identity)
print(appliopid)

print(appliopid.reduce())


# this implements ((λx.x) (λu.z))
print("------------------------- two lambda abstractions in an application")
constant = Abstraction(u, z)

appliopconst = Application(identity, constant)

print(constant)
print(appliopconst)

print(appliopconst.reduce())

# this implements ((λx.((λq.q) (λi.x)) (λu.z)), should print to (λi.(λu.z))
print("------------------------- complicated example (application as body of abstraction)")

VB1abs = Abstraction(q,q)
VB2abs = Abstraction(i,x)
VB3abs = constant

VB1app = Application(VB1abs,VB2abs)

VB4abs = Abstraction(x,VB1app)

VB2app = Application(VB4abs, VB3abs)

print(VB2app)

def reducechecker(lambterm):
    if str(lambterm.reduce()) != str(lambterm):
        return reducechecker(lambterm.reduce())
    else:
        return lambterm


print(reducechecker(VB2app))


# print(LambdaTerm.fromstring("(((λx.(λy.x)) z) u)"))

print("Alpha Conversion")
print("------------------------- identity")
print(identity)
if (isinstance(identity, Abstraction)):
    print(identity.alphaconv([identity.head,z]))

# the following implements ((λx.λy.x) y), this should be reduced to (λz.y) or some other variable than z (but not y)
print("------------------------- exception")
alphabs1 = Abstraction(y,x)
alphabs2 = Abstraction(x, alphabs1)

print(alphabs2)
print(alphabs2.alphaconv([alphabs2.head,y]))

#alphapp1 = Application(vb2abs, y)

#print(alphapp1.reduce())

# We implement the lambda abstraction : (λx.(λx.x)), alphaconversion x -> y on outer lambda we get (λy.(λx.x))
print("------------------------- exception")
alphabs1 = Abstraction(x,x)
alphabs2 = Abstraction(x,alphabs1)

print(alphabs2)

print(alphabs2.alphaconv([alphabs2.head, z])) #TODO

print("------------------------- arithmetic")
#0 = (λsz.z)        =(λs.(λz.z)
#S = (λxyz.y(xyz))  =(λx.λy.λz.(y (x (y z)))


abs1 = Abstraction(z,z)
zero = Abstraction(s,abs1)

app1 = Application(y, z)
app2 = Application(x, app1)
app3 = Application(y, app2)

labs1 = Abstraction(z, app3)
labs2 = Abstraction(y, labs1)
successor = Abstraction(x, labs2)
lijst =[]
def lambnumber(number, n,s=[]):
    if n != 0:
        s = Application(successor, number)
        lambnumber(s, n - 1, s)
    else:
        lijst.append(s)

lambnumber(zero,3)
s = lijst[0]

print(s.reduce())