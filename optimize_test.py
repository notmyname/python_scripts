#!/usr/bin/env python2.4

# not a good test because the function is fast anyway (not a lot of globals to be re-referenced)

from optimize import make_constants
from Common import logged_function

hole = open('/dev/null','w')

class klass(object):
    def write(*args):
	for a in args: print >>hole, a

obj = klass()

@logged_function(when='post')
def slow():
    for i in range(10000):
	obj.write('hello world')

@logged_function(when='post')
@make_constants
def fast():
    for i in range(10000):
	obj.write('hello world')

def main():
    slow()
    fast()

import profile,pstats
profile.run('main()','optimize_results')
s = pstats.Stats('optimize_results')
s.sort_stats('time','cumulative')
s.print_stats()

import dis
print 'slow() disassebly:'
print dis.dis(slow)
print
print 'fast() disassembly:'
print dis.dis(fast)

