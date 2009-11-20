'''
stats.py

Author: John Dickinson
'''

import math # for square root
import collections # for default dict

def mean(data):
    return float(sum(data)) / float(len(data))

def median(data):
    count = len(data)
    if count % 2:
        return data[count / 2]
    else:
        middle = count // 2
        return sum(data[middle-1:middle+1]) / 2.0

def mode(data):
    d = collections.defaultdict(int)
    for item in data:
        d[item] += 1
    return max((count,key) for key,count in d.items())[1]

def std_deviation(data):
    avg = mean(data)
    avg_squared_deviation = mean([(avg-x)**2 for x in data])
    return math.sqrt(avg_squared_deviation)

def min_max_difference(data):
    data = data[:]
    data.sort()
    return data[-1] - data[0]

def stats(data):
    return (mean(data),
            median(data),
            mode(data),
            std_deviation(data),
            min_max_difference(data),
           )

if __name__ == '__main__':
    import random
    data = [100*random.random() for _ in xrange(10000)]
    print stats(sorted(data))
    
    data = [random.uniform(1,100) for _ in xrange(10000)]
    print stats(sorted(data))
    
    data = [1,2,3,4,5,5,6,7,8,9]
    print stats(data)
    
    data = [1,1,1,1,1,1,1,1,1,9]
    print stats(data)
    
    import hashlib
    data = [sum(ord(y) for y in hashlib.md5(''.join(chr(random.randint(ord('A'),ord('z'))) for _ in xrange(x))).hexdigest()) for x in xrange(100)]
    print stats(sorted(data))
