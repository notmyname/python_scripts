#!/usr/bin/env python

import random

def infinite_random():
    random.seed()
    while True:
        yield random.random()

if __name__ == '__main__':
    import itertools
    import time

    target = 10000000

    s = time.time()
    x = list(itertools.islice(infinite_random(),target,target+1))
    print x
    print '%.8f seconds to complete' % (time.time()-s)
