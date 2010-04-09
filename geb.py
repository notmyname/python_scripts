#!/usr/bin/python

# *I -> *IU
def one(s):
    if s.endswith('I'):
        return s + 'U'
    return s

# M* -> M**
def two(s):
    try:
        i = s.index('M')
    except ValueError:
        return s
    else:
        return 'M' + s[i+1:]*2
    
# *III* -> *U*
def three(s):
    try:
        i = s.index('III')
    except ValueError:
        return s
    else:
        return s[:i] + 'U' + s[i+3:]
    
# *UU* -> **
def four(s):
    try:
        i = s.index('UU')
    except ValueError:
        return s
    else:
        return s[:i] + s[i+2:]


start = 'MI'
print start
for func in (two, # get some stuff to work with
             two,
             two,
             two,
             one, # end with U
             three, # compress first III to U
             two, # duplicate to get MU*UU*U
             four,
             three,
             three,
             three,
             three,
             three,
             three,
             three,
             three,
             four,
             four,
             four,
             four,
             two,
             four,
             two,
             four,
            ):
    start = func(start)
    print start
