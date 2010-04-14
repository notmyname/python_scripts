#!/usr/bin/env python

'''in which I show how to pass a file object pointing to uncompressed data
to a function and have it read compressed data--without reading it all into memory'''

import os
import zlib

filename = 'test'

f = open(filename, 'wb')
test_data = 'test data\nline two\nline three'*50
f.write(test_data)
f.close()

def do_something(f):
    size = 256
    buff = []
    x = f.read(size)
    while x:
        buff.append(x)
        x = f.read(size)
    buff = ''.join(buff)
    print test_data == zlib.decompress(buff)

class Enc(object):
    def __init__(self, file_obj):
        self._f = file_obj
        self.compressor = zlib.compressobj(9)
        self.done = False
    
    def read(self, *a, **kw):
        if self.done:
            return ''
        x = self._f.read(*a, **kw)
        if not x:
            compressed = self.compressor.flush(zlib.Z_FINISH)
            self.done = True
        else:
            compressed = self.compressor.compress(x)
            if not compressed:
                compressed = self.compressor.flush(zlib.Z_SYNC_FLUSH)
        return compressed

f = open(filename, 'rb')
enc = Enc(f)
do_something(enc)
f.close()

os.unlink(filename)