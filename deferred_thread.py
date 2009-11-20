#!/usr/bin/env python2.4

from Common import *

import time

@deferred_thread
def long():
    print 'starting long()'
    time.sleep(2)
    print 'long() finished'
    return 'long() value'

@deferred_thread
def long2():
    print 'starting long2()'
    time.sleep(10)
    print 'long2() finished'
    return 'long2() result'

print 'before calls'
x = long()
y = long2()
print 'after calls'
print 'something else'
time.sleep(5)
print 'done sleeping in main thread'
print x()
print y()

