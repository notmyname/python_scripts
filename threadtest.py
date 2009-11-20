#!/usr/bin/env python2.4

import threading
import sys
import time
import random
import traceback

sys.path.insert(0,'/usr/local/WebApp/New/Context/')
from BenefitSystem2.storage import storage_mod
sys.path.pop(0)

generic = 0

usePause = 0

c = {}

MAXID = 300

class Hammer(threading.Thread):
    def __init__(self, name=-1, **kwds):
	global generic

	threading.Thread.__init__(self, **kwds)

	if name == -1:
	    generic += 1;
	    self.setName(str(generic))
	else:
	    self.setName(name)

	self.start()

    def run(self):
	global c
	# the main function of the thread

	name = self.getName()

	group_date = 'test_20040314'

	s = storage_mod.storage_mod(group_date)
	print name, "-> starting"
	for id in range(1,MAXID+1):
	    while len(str(id)) < 3:
		id = '0' + str(id)
	    n = s.getData(s._CENSUS_TYPE,str(id))._employee._name
	    if n != c[id]:
		print 'ids don\'t match: %s' % id
	    if usePause:
		time.sleep(random.randrange(3))

	print name, "-> done"

def main():
    global c

    if len(sys.argv) > 2:
	print "Usage: %s [numThreads]"
	return 1

    #################################
    # Create the appropriate number #
    # of threads and start them     #
    #################################

    if len(sys.argv) < 2:
	numThreads = 3
    else:
	numThreads = int(sys.argv[1])

    group_date = 'test_20040314'

    s = storage_mod.storage_mod(group_date)
    for id in range(1,MAXID+1):
	while len(str(id)) < 3:
	    id = '0' + str(id)
	c[id] = s.getData(s._CENSUS_TYPE,str(id))._employee._name

    t = {}
    for x in range(1,numThreads+1):
	#time.sleep(random.randrange(0,3))
	t[x] = Hammer()


    for x in range(1,numThreads+1):
	t[x].join()

    print
    print "All threads done"
    print

    return 0


if __name__ == '__main__':
    sys.exit(main())
