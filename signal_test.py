#!/usr/bin/env python2.4

import signal

def nothing(sig,stack):
    print 'that doesn\'t work'

for i in range(1,signal.NSIG):
    try:
	signal.signal(i,nothing)
    except:
	pass

while True:
    try:
	text = raw_input('kill me (type exit) ')
    except EOFError:
	pass
    else:
	if text == 'exit':
	    break
