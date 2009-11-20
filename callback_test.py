#!/usr/bin/env python2.4

import time
from Common import add_callback,deferred_thread

# first argument is terminating function, second is its result
def my_callback(proc,res,x,y=6):
    print 'in my_callback',x,y
    print '%s finished with %s result' % (proc,res)

@deferred_thread
@add_callback(my_callback,3,4) # 3 and 4 will be passed to my_callback
def long_running(a,b):
    time.sleep(5)
    print 'in long_running',a,b

print 'start'
long_running(1,b=2)
print 'end'
