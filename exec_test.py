#!/usr/bin/env python2.4

code = """x = 4
print x,a
"""

code_obj = compile(code,'<code string>','exec')

x = 2
d = {'a':2}
exec code_obj in d
print d['x']
print x
