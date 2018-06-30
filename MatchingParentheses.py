    def find_parentheses(s):
        """ Find and return the location of the matching parentheses pairs in s.

        Given a string, s, return a dictionary of start: end pairs giving the
        indexes of the matching parentheses in s. Suitable exceptions are
        raised if s contains unbalanced parentheses.
        """

        # The indexes of the open parentheses are stored in a stack, implemented
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
    @staticmethod
    def fromstring(string):
        for s in enumerate(string, start=1):
            # find parentheses indices
            try:
                parentheses_locs = find_parentheses(s)
                sorted([(k,v) for k, v in parentheses_locs.items()])
            # parentheses do not match
            except IndexError as e:
                print(str(e))
        
        https://scipython.com/blog/parenthesis-matching-in-python/
        
        '''
        # define characters for later convenience
        lambdat = ''
        l = '('
        r = ')'
        
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

            else: # Correct variable if all the characters in it are correct characters
                for i in range(len(string)):
                    if string[i] not in varchars: # if there is an incorrect character, stop and raise exception
                        raise NameError
                lambdat = Variable(string)

        return lambdat
        '''
