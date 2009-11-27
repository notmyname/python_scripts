#!/usr/bin/env python

import sys
import random
import string

try:
    url = sys.argv[1]
except IndexError:
    print 'Usage: %s URL' % sys.argv[0]
    sys.exit(1)

minlength = 6
alphabet = string.letters + string.digits
short = []
for _ in xrange(minlength):
    short.append(random.choice(alphabet))
short = ''.join(short)
print short

# now save short and look it up when a request comes is