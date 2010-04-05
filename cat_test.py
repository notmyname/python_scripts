import time

print '+='
for limit in (10000,100000,1000000,10000000):
    start_time = time.time()
    x = ''
    for i in xrange(limit):
        x += 'x'
    print limit, '%.4f' % (time.time()-start_time)

print 'join'
for limit in (10000,100000,1000000,10000000):
    start_time = time.time()
    x = []
    for i in xrange(limit):
        x.append('x')
    x = ''.join(x)
    print limit, '%.4f' % (time.time()-start_time)