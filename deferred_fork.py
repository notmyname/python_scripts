#!/usr/bin/env python2.4

from Common import *

import time

@deferred_fork
def long():
    print 'starting long()'
    time.sleep(10)
    print 'long() finished'
    return 'some important value'

@deferred_fork
def long2():
    print 'starting long2()'
    time.sleep(5)
    raise Exception,'some error'
    print 'long2() finished'
    return 'long2() result'

print 'before calls'
x = long()
y = long2()
print 'after calls'
print 'something else'
time.sleep(2)
print 'done sleeping in main thread'
print 'waiting for long to finish'
x.end_now()
try:
    print x()
except Exception,e:
    print 'error: %s' % `e`
print 'waiting for long2 to finish'
try:
    print y()
except Exception,e:
    print 'error: %s' % e
print 'Done'

