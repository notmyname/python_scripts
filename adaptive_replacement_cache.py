#!/usr/bin/env python

import time # for determining least recently used (LRU)

class ARC(object):
    def __init__(self,max_size):
        self._max_size = max_size // 2
        self._p = 0
        self._single_access_top = {}
        self._single_access_bottom = {}
        self._multi_access_top = {}
        self._multi_access_bottom = {}
    
    def __str__(self):
        out = []
        #out.append(str(self._single_access_top))
        #out.append(str(self._single_access_bottom))
        #out.append(str(self._multi_access_top))
        #out.append(str(self._multi_access_bottom))
        total_len = (len(self._single_access_top) + 
                     len(self._single_access_bottom) + 
                     len(self._multi_access_top) +
                     len(self._multi_access_bottom))
        out.append(str(total_len))
        keys = (self._single_access_top.keys(),
                self._single_access_bottom.keys(),
                self._multi_access_top.keys(),
                self._multi_access_bottom.keys())
        out.append('\n'.join(str(x) for x in keys))
        out.append('')
        return '\n'.join(out)
    
    def _smallest(self, d):
        v,k = min((val,key) for key,val in d.items())
        return k,v

    def _replace(self,p,item):
        if self._single_access_top and ((item in self._multi_access_bottom and len(self._single_access_top) == p) or len(self._single_access_top) > p):
            # move LRU of _single_access_top to top of _single_access_bottom
            k,v = self._smallest(self._single_access_top)
            del self._single_access_top[k]
            self._single_access_bottom[k] = v
        else:
            # move LRU of _multi_access_top to top of _multi_access_bottom
            k,v = self._smallest(self._multi_access_top)
            del self._multi_access_top[k]
            self._multi_access_bottom[k] = v

    def add(self,key,value):
        decorated = key
        now = time.time()

        # get lengths for speed
        len_t1 = len(self._single_access_top)
        len_b1 = len(self._single_access_bottom)
        len_t2 = len(self._multi_access_top)
        len_b2 = len(self._multi_access_bottom)
        len_L1 = len_t1 + len_b1
        len_L2 = len_t2 + len_b2

        if decorated in self._single_access_top or decorated in self._multi_access_top:
            # move decorated to top of _multi_access_top
            try:
                del self._single_access_top[decorated]
            except KeyError:
                del self._multi_access_top[decorated]
            self._multi_access_top[decorated] = (now, value)

        elif decorated in self._single_access_bottom:
            # adapt p
            self._p = min(self._max_size,self._p+max(float(len_b2)/float(len_b1),1))
            self._replace(self._p,decorated)
            # move decorated to top of _multi_access_top and place in cache
            del self._single_access_bottom[decorated]
            self._multi_access_top[decorated] = (now, value)

        elif decorated in self._multi_access_bottom:
            # adapt p
            self._p = max(0,self._p-max(float(len_b1)/float(len_b2),1))
            self._replace(self._p,decorated)
            # move decorated to top of _multi_access_top and place in cache
            del self._multi_access_bottom[decorated]
            self._multi_access_top[decorated] = (now, value)

        else:
            if len_L1 == self._max_size:
                if len_t1 < self._max_size:
                    # delete LRU if _single_access_bottom
                    k,v = self._smallest(self._single_access_bottom)
                    del self._single_access_bottom[k]
                    self._replace(self._p,decorated)
                else:
                    # delete LRU if _single_access_top
                    k,v = self._smallest(self._single_access_top)
                    del self._single_access_top[k]
            elif len_L1 < self._max_size <= (len_L1+len_L2):
                if (len_L1+len_L2) == 2*self._max_size:
                    # delete LRU if _multi_access_bottom
                    k,v = self._smallest(self._multi_access_bottom)
                    del self._multi_access_bottom[k]
                self._replace(self._p,decorated)
            # put decorated at top of _single_access_top and place it in the cache
            self._single_access_top[decorated] = (now, value)

    def get(self,key):
        return self._multi_access_top.get(key, 
               self._multi_access_bottom.get(key,
               self._single_access_top.get(key,
               self._single_access_bottom.get(key, (None,None)))))[1]

if __name__ == '__main__':
    max_size = 10
    print 'cache size: %s' % max_size
    c = ARC(max_size)

    limit = max_size
    lst = range(limit)
    print 'adding %d..%d' % (limit/2, limit-1)
    for i in range(limit/2,limit):
        c.add(i,None)
    print c
    print 'adding %d..%d' % (limit-1, limit/2)
    for i in range(limit-1,limit/2+1,-1):
        c.add(i,None)
    print c
    print 'adding %s..%s' % (limit, limit+limit/2-1)
    for i in range(limit, limit+limit/2):
        c.add(i,None)
    print c
    import random
    print c.get(random.choice(range(limit)))