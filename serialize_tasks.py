#!/usr/bin/env python2.4

import threading, Queue, inspect
class Serializer(threading.Thread):
    def __init__(self,*a,**kw):
	threading.Thread.__init__(self,*a,**kw)
	self.setDaemon(True)
	self.workRequestQueue = Queue.Queue()
	self.resultQueue = Queue.Queue()
	self.messageQueue = Queue.Queue()
	self.start()

    def apply(self,callable,*a,**kw):
	self.workRequestQueue.put((callable,a,kw))

    def kill(self):
	self.workRequestQueue.put((None,None,None))
	self.join()

    def run(self):
	while True:
	    callable,passed_args,passed_kwds = self.workRequestQueue.get()

	    if callable is None and \
	       passed_args is None and \
	       passed_kwds is None:
		# we received the kill signal
		break

	    # find argument names
	    avail_args,varargs,varkw,locals = inspect.getargspec(callable)

	    if 'response' in avail_args or \
	       (isinstance(locals,tuple) and 'response' in locals):
		# callable has an argument called response,
		# so pass in the message queue to that variable
		res = callable(response=self.messageQueue,
			       *passed_args,
			       **passed_kwds
			      )
	    else:
		# callable does not have a response argument,
		# so call the function as normal
		res = callable(*passed_args,
			       **passed_kwds
			      )

	    self.resultQueue.put(res)

import time

def first(response):
    # report here
    response.put('at start of first()')
    time.sleep(1)
    # report here
    response.put('in middle of first()')
    time.sleep(1)
    return 'first done'

def second():
    time.sleep(2)
    return 'second done'

def main():
    ser = Serializer()
    print 'calling first()'
    ser.apply(first)

    print 'calling second()'
    ser.apply(second)

    while True:
	try:
	    res = ser.resultQueue.get(block=False)
	except Queue.Empty:
	    pass
	else:
	    print 'result: %s' % res
	try:
	    msg = ser.messageQueue.get(block=False)
	except Queue.Empty:
	    pass
	else:
	    print 'message: %s' % msg

    print 'done'

main()
