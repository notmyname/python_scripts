#!/usr/bin/env python

'''in which I show how to pass a file object pointing to uncompressed data
to a function and have it read compressed data--without reading it all into memory'''

import os
import zlib
import gzip
import struct

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
    return buff

class CompressedFileReader(object):
    '''gzip header and footer code taken from the python stdlib gzip module'''
    def __init__(self, file_obj):
        self._f = file_obj
        self._compressor = zlib.compressobj(9,
                                            zlib.DEFLATED,
                                            -zlib.MAX_WBITS,
                                            zlib.DEF_MEM_LEVEL,
                                            0)
        self.done = False
        self.first = True
        self.crc32 = 0
        self.total_size = 0
    
    def read(self, *a, **kw):
        if self.done:
            return ''
        x = self._f.read(*a, **kw)
        if x:
            self.crc32 = zlib.crc32(x, self.crc32) & 0xffffffffL
            self.total_size += len(x)
            compressed = self._compressor.compress(x)
            if not compressed:
                compressed = self._compressor.flush(zlib.Z_SYNC_FLUSH)
        else:
            compressed = self._compressor.flush(zlib.Z_FINISH)
            i = self.crc32 & 0xffffffffL
            crc32 = struct.pack("<L", i)
            i = self.total_size & 0xffffffffL
            size = struct.pack("<L", i)
            footer = crc32 + size
            compressed += footer
            self.done = True
        if self.first:
            self.first = False
            header = '\037\213\010\000\000\000\000\000\002\377'
            compressed = header + compressed
        return compressed

f = open(filename, 'rb')
compressed_f = CompressedFileReader(f)
compressed_data = do_something(compressed_f)
f.close()

f = open(filename, 'wb')
f.write(compressed_data)
f.close()

f = gzip.GzipFile(filename, 'rb')
d = f.read()
assert test_data == d
f.close()

os.unlink(filename)