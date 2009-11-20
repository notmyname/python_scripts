#!/usr/bin/env python2.4

import heapq,time # for determining least recently used (LRU)

class ARC(object):
    _single_access_top = []
    _single_access_bottom = []
    _multi_access_top = []
    _multi_access_bottom = []

    _cache = {}

    def __init__(self,max_size):
	self._max_size = max_size
	self._p = 0

    def _replace(self,p,item):
	if self._single_access_top and ((item in self._multi_access_bottom and len(self._single_access_top) == p) or len(self._single_access_top) > p):
	    # move LRU of _single_access_top to top of _single_access_bottom
	    i = heapq.heappop(self._single_access_top)
	    heapq.heappush(self._single_access_bottom,i)
	    # remove it from the cache
	    del self._cache[i[1]]
	else:
	    # move LRU of _multi_access_top to top of _multi_access_bottom
	    i = heapq.heappop(self._multi_access_top)
	    heapq.heappush(self._multi_access_bottom,i)
	    # remoe it from the cache
	    del self._cache[i[1]]

    def add(self,key,value):
	decorated = (time.time(),key)

	# get lengths for speed
	len_t1 = len(self._single_access_top)
	len_b1 = len(self._single_access_bottom)
	len_t2 = len(self._multi_access_top)
	len_b2 = len(self._multi_access_bottom)
	len_L1 = len_t1 + len_b1
	len_L2 = len_t2 + len_b2

	if decorated in self._single_access_top or decorated in self._multi_access_top:
	    # move decorated to to of _multi_access_top
	    try:
		i = self._single_access_top.index(decorated)
		del self._single_access_top[i]
		heapq.heapify(self._single_access_top)
	    except ValueError:
		i = self._multi_access_top.index(decorated)
		del self._multi_access_top[i]
		heapq.heapify(self._multi_access_top)
	    heapq.heappush(self._multi_access_top,decorated)

	elif decorated in self._single_access_bottom:
	    # adapt p
	    self._p = min(self._max_size,self._p+max(float(len_b2)/float(len_b1),1))
	    self._replace(self._p,decorated)
	    # move decorated to top of _multi_access_top and place in cache
	    i = self._single_access_bottom.index(decorated)
	    del self._single_access_bottom[i]
	    heapq.heapify(self._single_access_bottom)
	    heapq.heappush(self._multi_access_top,decorated)
	    self._cache[key] = value

	elif decorated in self._multi_access_bottom:
	    # adapt p
	    self._p = max(0,self._p-max(float(len_b1)/float(len_b2),1))
	    self._replace(self._p,decorated)
	    # move decorated to top of _multi_access_top and place in cache
	    i = self._multi_access_bottom.index(decorated)
	    del self._multi_access_bottom[i]
	    heapq.heapify(self._multi_access_bottom)
	    heapq.heappush(self._multi_access_top,decorated)
	    self._cache[key] = value

	else:
	    if len_L1 == self._max_size:
		if len_t1 < self._max_size:
		    # delete LRU if _single_access_bottom
		    heapq.heappop(self._single_access_bottom)
		    self._replace(self._p,decorated)
		else:
		    # delete LRU if _single_access_top
		    item = heapq.heappop(self._single_access_top)
		    # remove it from the cache
		    del self._cache[item[1]]
	    elif len_L1 < self._max_size and (len_L1+len_L2) >= self._max_size:
		if (len_L1+len_L2) == 2*self._max_size:
		    # delete LRU if _multi_access_bottom
		    heapq.heappop(self._multi_access_bottom)
		self._replace(self._p,decorated)
	    # put decorated at top of _single_access_top and place it in the cache
	    heapq.heappush(self._single_access_top,decorated)
	    self._cache[key] = value

    def get(self,key):
	return self._cache[key]

if __name__ == '__main__':
    max_size = 1000
    c = ARC(max_size)

    lst = range(10000)
    import random, time
    #random.shuffle(lst)
    start = time.time()
    for i in lst:
	#time.sleep(.1)
	c.add(i,None)
	#print c._cache.keys()
    print 'Done in %.4f seconds' % (time.time() - start)
