#!/usr/bin/env python2.4

def fib():
    x,y = 0,1
    while True:
        yield x
        x,y = y,x+y

def recurse_fib(n):
    if n <= 1: return 1
    else: return recurse_fib(n-1) + recurse_fib(n-2)

if __name__ == '__main__':
    import itertools
    import time

    target = 1000000

    s = time.time()
    x = list(itertools.islice(fib(),target,target+1))
    #print x
    #print float(x[1]) / float(x[0])
    print '%.8f seconds to complete' % (time.time()-s)

    #s = time.time()
    #x = [recurse_fib(target)]
    #print '%.8f' % (time.time()-s)
