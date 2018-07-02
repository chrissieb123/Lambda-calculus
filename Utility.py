import LambdaTerm, Abstraction, Application

# define usable variable names
varchars = LambdaTerm.LambdaTerm.varchar

class InputError(Exception):
    pass

def find_parentheses(s):
    """ Find and return the location of the matching parentheses pairs in s.
    Given a string, s, return a dictionary of start: end pairs giving the
    indices of the matching parentheses in s. Suitable exceptions are
    raised if s contains unbalanced parentheses.
    Source: https://scipython.com/blog/parenthesis-matching-in-python/
    """

    # The indices of the open parentheses are stored in a stack, implemented
    # as a list

    stack = []
    parentheses_locs = {}
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            try:
                parentheses_locs[stack.pop()] = i
            except IndexError:
                raise IndexError('Too many close parentheses at index {}'
                                 .format(i))
    if stack:
        raise IndexError('No matching close parenthesis to open parenthesis '
                         'at index {}'.format(stack.pop()))
    return parentheses_locs


# returns a lambda term created from the string argument
# categorize lambda terms using brackets, working from outside in
def fromstring(string):
    # define characters for later convenience
    lambdastring = ''
    l = '('
    r = ')'

    # collect index pairs for every bracket or print error if expression is invalid
    for s in enumerate(string, start=1):
        # find parentheses indices
        try:
            parentheses_locs = find_parentheses(s)
            indexpairs = sorted([(k, v) for k, v in parentheses_locs.items()])
        # parentheses do not match
        except IndexError as e:
            print(str(e))

    # define indices of the last pair of parentheses (for the 'N' term)
    rpair = indexpairs[-1][1]
    lpair = indexpairs[-1][0]
    
    # check if the expression is valid
    for i in range(len(string)):
        if string[i] not in varchars:
            raise NameError

    # check if it is a variable
    if len(indexpairs) < 2:
           return lambdastring
    
    # application if there is a space before left bracket paired with second-to-last right bracket
    if string[lpair - 1] == ' ':
        lambdastring = Application.Application.frstring(string)
    # abstraction if there is a lambda right after the left parenthesis
    elif string[lpair + 1] == LambdaTerm.lam:
        lambdastring = Abstraction.Abstraction.frstring(string)
    
    # we have our result
    return lambdastring

