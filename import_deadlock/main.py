import threading
import sys
sys.setcheckinterval(sys.maxint)

def func():
    import my_module
    print 'imported'

t = threading.Thread(target=func)
t.start()

import my_module
my_module.foo()
