#!/usr/bin/env python2.4

import sys

try:
    plain_text = sys.argv[1]
except:
    print >>sys.stderr, 'Usage: %s text' % sys.argv[0]
    sys.exit(1)

import crypt

print 'block size: %d' % crypt.coder.block_size
print 'key size: %d' % crypt.coder.key_size

key = crypt.hasher.new('x').hexdigest()[:32]
print 'key: %s' % key

print 'plain text: %s' % plain_text
print 'len(plain_text): %d' % len(plain_text)


c = crypt.crypt(key)
print
sys.stdout.write(c.encrypt(plain_text))
