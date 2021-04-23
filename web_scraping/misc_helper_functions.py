def flatten(S):
    '''
    recursively flattens a list of lists of lists
    input: List of list of lists (and so on)
    source: https://stackoverflow.com/questions/12472338/flattening-a-list-recursively
    '''

    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def remove_dup(S):
    '''
    input: list containing duplicate urls
    output: converts to a set to remove duplicates
    '''
    return set(S)