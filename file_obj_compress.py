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
    size = 1024 # compression gets better as this goes up (don't set it too small)
    buff = []
    x = f.read(size)
    while x:
        buff.append(x)
        x = f.read(size)
    buff = ''.join(buff)
    print 'original size:', len(test_data)
    print 'compressed size:', len(buff)
    print 'do they match: ', test_data == zlib.decompress(buff)

class CompressedFileReader(object):
    def __init__(self, file_obj):
        self._f = file_obj
        self._compressor = zlib.compressobj(9)
        self.done = False
    
    def read(self, *a, **kw):
        if self.done:
            return ''
        x = self._f.read(*a, **kw)
        if x:
            compressed = self._compressor.compress(x)
            if not compressed:
                compressed = self._compressor.flush(zlib.Z_SYNC_FLUSH)
        else:
            compressed = self._compressor.flush(zlib.Z_FINISH)
            self.done = True
        return compressed

f = open(filename, 'rb')
compressed_f = CompressedFileReader(f)
do_something(compressed_f)
f.close()

os.unlink(filename)