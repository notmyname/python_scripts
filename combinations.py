x = [1,2]
y = [1,2,3]
z = [4,5]
q = ['x','y']
e = []

def combine(lists_to_combine):
    def recurse(lists):
        if len(lists) == 1:
            return lists[0]
        res = []
        for val in lists[0]:
            right_combine = recurse(lists[1:])
            if not right_combine:
                res.append((val,None))
            for val2 in right_combine:
                res.append((val,val2))
        return res
    def flatten(i):
        if not isinstance(i,(list,tuple)):
            return [i]
        res = []
        for x in i:
            if not isinstance(x,tuple):
                res.append(x)
            else:
                res.extend(flatten(x))
        return res
    nested_combinations = recurse(lists_to_combine)
    final = []
    for combination in nested_combinations:
        final.append(flatten(combination))
    return final

import itertools

def combinations(*seqs):
    def base_combinations(so_far, seq):
        for x in seq:
            yield so_far + [x]
    def nested_combinations(so_far, seqs):
        if len(seqs) == 1:
            return base_combinations(so_far, seqs[0])
        else:
            iterators = (nested_combinations(so_far + [x], seqs[1:]) for x in seqs[0])
            return itertools.chain(*iterators)
    return nested_combinations([], seqs)

def icombinations(*seqs):
    if len(seqs) > 1:
        for rest in icombinations(*seqs[1:]):
            for i in seqs[0]:
                yield [i] + rest
    else:
        for i in seqs[0]: yield [i]

if __name__ == '__main__':
    print list(sorted(icombinations(x,y,z)))
    print combine([x,y,z])
