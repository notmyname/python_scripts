'''evil with the import statement'''


import sys

def foo_func(x):
    return x * x


sys.modules['foobar'] = foo_func
import foobar
print foobar(10)


class Klass(object):
    '''a classy class'''
    def bar(self, x):
        return x * x * x


sys.modules['classy'] = Klass
import classy
print classy().bar(10)


sys.modules['yarr'] = Klass()
import yarr
print yarr.bar(10)


sys.modules['argh'] = Klass().bar
import argh
print argh(10)


sys.modules['blargh'] = 10
import blargh
print argh(blargh)
