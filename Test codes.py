lam = '(λx.(λy.(λz.xyz)))'
"((a b) c)"
'([(λx.(λy.(λz.xyz))) M] N)'

lamba = chr(955)


def betareduction(lambdaterm, application):
    # first we have to lambda convert the term if necessary

    # separate body and head
    separate = list(lambdaterm.partition("."))
    head = separate[0]
    body = list(separate[2])

    # find variable in expression λx.M
    variable = list(head.partition("λ"))[2]

    # substitution in the body for the variable
    for i in range(0, len(body)):
        if body[i] == variable:
            body[i] = application

    # return body as a list
    return ''.join(body)


print(betareduction(betareduction(lam, "m"),"k"))

def alphaconvert(lambdaterm, application):
    # initialise list of bound variables with indices
    BV = []

    # initialise lists of convertables in the application with indices
    CA = []

    # search for bound variables in the lambdaterm and add them with indices to BV
    for i in range(0, len(str(lambdaterm))-1):
        if str(lambdaterm)[i] == lamba:
            BV.append([str(lambdaterm)[i+1], i+1])

    # search for convertables in the application and add to CA
    for j in range(0, len(str(application))):
        if str(application)[j] in BV:
            CA.append(str(application)[j])


# previous fromstring    
    '''
    # find most right bracket after removing outer brackets
    string.strip(r)
    nextr = string.rfind(r)
    # application if space after bracket
    if string[nextr+1] == ' ':
        lamdbdat = Application.frstring(string)
    # 
    else:
        # the corresponding left bracket
        nextl = string[len(string)-nextr-1]
        # abstraction if (λ follows bracket
        if string[nextl+1] == l and string[nextl+2] == lam:
            lambdat = Abstraction.frstring()
    # variabele als alle karakters correct zijn
    else: # Correct variable if all the characters in it are correct characters
            for i in range(len(string)):
                if string[i] not in varchars: # if there is an incorrect character, stop and raise exception
                    raise NameError
            lambdat = Variable(string)
    return lambdat
    '''

 # previous frstring Application
     '''
     s1, s2 = string.split(' ')
     self.M = Utility.fromstring(s1)
     self.N = Utility.fromstring(s2)
     '''

 # previous frstring Abstraction
     '''
     s1,s2 = string.split('.')
     self.head = s1.lstrip(LambdaTerm.lam) # the head is what is between the lambda and the dot
     self.body = Utility.fromstring(s2) # body after the dot
     '''
      
   
        
