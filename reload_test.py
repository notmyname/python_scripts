#!/usr/bin/env python

import os
import sys

module_code = '''
import autoreloader
print 'in module'
class Klass(autoreloader.AutoReloader):
    def foo(self, *a, **kw):
        print 'in foo(%s, %s)' % (a, kw)
'''

f = open('testmodule.py', 'wb')
f.write(module_code)
f.close()

import testmodule

x = testmodule.Klass()
x.foo('hello','world')

new_module_code = module_code.replace('foo','bar').replace('in module','in edited module')
f = open('testmodule.py', 'wb')
f.write(new_module_code)
f.close()
print 'testmodule.py modified'

os.remove('testmodule.pyc') # <--- this is the key
reload(testmodule)
#x.__class__ = testmodule.Klass # <--- the AutoReloader class handles this automatically

try:
    x.bar('test')
except AttributeError:
    print 'ERROR: bar not found'
    x.foo('should not be here')

os.remove('testmodule.py')
os.remove('testmodule.pyc')
