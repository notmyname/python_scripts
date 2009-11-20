#!/usr/bin/env python2.4

import time

count_list = [1,
	      10,
	      100,
	      1000,
	      10000,
	      100000,
	      1000000,
	     ]

for num in count_list:
    r = range(num)
    start = time.time()
    obj = r
    if 'b' in obj:
	print 'found b'
    count1 = time.time() - start
    print '%.6f seconds to seach %d item list' % (count1,len(obj))
    start = time.time()
    obj = set(r)
    if 'b' in obj:
	print 'found b'
    count1 = time.time() - start
    print '%.6f seconds to seach %d item set' % (count1,len(obj))
    start = time.time()
    obj = frozenset(r)
    if 'b' in obj:
	print 'found b'
    count1 = time.time() - start
    print '%.6f seconds to seach %d item frozenset' % (count1,len(obj))
    start = time.time()
    obj = dict.fromkeys(r)
    if 'b' in obj:
	print 'found b'
    count1 = time.time() - start
    print '%.6f seconds to seach %d item dict' % (count1,len(obj))
    start = time.time()
    obj = tuple(r)
    if 'b' in obj:
	print 'found b'
    count1 = time.time() - start
    print '%.6f seconds to seach %d item tuple' % (count1,len(obj))
    print
