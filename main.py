#!/usr/bin/env python3
from Application import Application
from Abstraction import Abstraction
from Variable import Variable

# create lambda terms

print("-------------------------")
print("Bèta-Reduction")
print("------------------------- ")

# create variables
(q,w,e,r,t,y,u,i,s,x,z) = (Variable("q"), Variable("w"), Variable("e"), Variable("r"), Variable("t"), Variable("y"), Variable("u"), Variable("i"),Variable("s"),Variable("x"),Variable("z"))

# handy lambda terms
identity = Abstraction(x, x)
absuz = Abstraction(u, z)
absyx = Abstraction(y, x)

print("------------------------- abstraction as body of an abstraction")

# the following implements the lambda term:  (((λx.(λy.x) z) u)
abs1 = Abstraction(y, x)
abs2 = Abstraction(x, abs1)

app1 = Application(abs2, z)
app2 = Application(app1, u)

print(app1)

print("Reduce method on application: ", app1.reduce())
print("Call method on abstraction: ", abs2(z))

# this implements ((λx.x) u)
print("------------------------- identity function")

appliopid = Application(identity, u)

print(appliopid)
print(appliopid.reduce())


# this implements ((λx.x) (λu.z))
print("------------------------- two lambda abstractions in an application")

appliopconst = Application(identity, absuz)

print(absuz)
print(appliopconst)

print(appliopconst.reduce())

# this implements ((λx.((λq.q) (λi.x)) (λu.z)), should print to (λi.(λu.z))
print("------------------------- complicated example (application as body of abstraction)")

VB1abs = Abstraction(q,q)
VB2abs = Abstraction(i,x)
VB3abs = absuz

VB1app = Application(VB1abs,VB2abs)

VB4abs = Abstraction(x,VB1app)
VB2app = Application(VB4abs, VB3abs)

print(VB2app)
print(VB2app.fullreduce()) # (reduced twice)

print("------------------------- abstraction reduce")
print(VB4abs)
print(VB4abs.reduce())

print("-------------------------")
print("Alpha-Conversion")
print("------------------------- ")

print("------------------------- identity")
print(identity)
print(identity.alphaconv([identity.head,z]))

# the following implements ((λx.λy.x) y), this should be reduced to (λz.y) or some other variable than z (but not y)
print("------------------------- exception")
abs1 = Abstraction(y,x)
abs2 = Abstraction(x, abs1)

print(abs2)
print(abs2.alphaconv([abs2.head,y]))

# We implement the lambda abstraction : (λx.(λx.x)), alphaconversion x -> y on outer lambda we get (λy.(λx.x))
print("------------------------- multiple same heads")
abs = Abstraction(x,identity)

print(abs)
print(abs.alphaconv([abs.head, y]))

# We implement the lambda abstraction : (λx.((λx.x) (λy.x)), alphaconversion x -> z on outer lambda we get (λz.((λx.x) (λy.z))
print("------------------------- variable bound in application")
app = Application(identity,absyx)
abs = Abstraction(x,app)

print(abs)
print(abs.alphaconv([abs.head, z]))

print("------------------------- ")
print("Alpha-conversion for bad substitution (rule 5)")
print("------------------------- ")

# Implements the application: ((λx.(λy.(x y))) (x y)), alpha-converts the x's in identity to a random variable and then reduces to: (λq.((x y) q))
print("------------------------- reduction with variable bound in application")
app = Application(Abstraction(x,Abstraction(y,Application(x,y))),Application(x,y))
print(app)
print(app.fullreduce())

print("------------------------- multiple layers")
abs = Abstraction(x,identity)
app = Application(Abstraction(y,abs),x)
print(app)
print(Application(Abstraction(y,abs),x).fullreduce())

print("------------------------- advanced example (using substitution)")
h = Variable("h")
abs = Abstraction(x,Abstraction(y,Application(Abstraction(x,Application(x,q)),h)))
print(abs, "[h:= (x y)]")
print(abs.substitute([h,Application(x,y)]))

print("------------------------- last example fully reduced")
app = Application(Abstraction(h,abs),Application(x,y))
print(app)
print(app.fullreduce())