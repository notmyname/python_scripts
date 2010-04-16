#!/usr/bin/env python

'''in which I show how to pass a file object pointing to uncompressed data
to a function and have it read compressed data--without reading it all into memory'''

import os
import zlib
import gzip
import struct

filename = 'test'

test_data = 'test data\nline two\nline three'*50

class CompressedFileReader(object):
    '''
    Wraps a file object and provides a read method that returns gzip'd data.
    
    One warning: if read is called with a small value, the data returned may
    be bigger than the value. In this case, the "compressed" data will be
    bigger than the original data. To solve this, use a bigger read buffer.
    
    An example use case:
    Given an uncompressed file on disk, provide a way to read compressed data
    without buffering the entire file data in memory. Using this class, an
    uncompressed log file could be uploaded as compressed data with chunked 
    transfer encoding.
    
    gzip header and footer code taken from the python stdlib gzip module
    '''
    def __init__(self, file_obj, compresslevel=9):
        self._f = file_obj
        self._compressor = zlib.compressobj(compresslevel,
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
            crc32 = struct.pack("<L", self.crc32 & 0xffffffffL)
            size = struct.pack("<L", self.total_size & 0xffffffffL)
            footer = crc32 + size
            compressed += footer
            self.done = True
        if self.first:
            self.first = False
            header = '\037\213\010\000\000\000\000\000\002\377'
            compressed = header + compressed
        return compressed


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
    print 'data matches:', test_data == zlib.decompress(buff, 16+zlib.MAX_WBITS)
    return buff


# make a test file
f = open(filename, 'wb')
f.write(test_data)
f.close()

# using the uncompressed file, test the compressor wrapper
f = open(filename, 'rb')
compressed_f = CompressedFileReader(f)
compressed_data = do_something(compressed_f)
f.close()

# write the compressed data out (for the next test)
f = open(filename, 'wb')
f.write(compressed_data)
f.close()

# make sure the compressed data can be read by gzip (ensures tools like gunzip will work)
f = gzip.GzipFile(filename, 'rb')
d = f.read()
assert test_data == d
print 'Passed: compressed data was successfully read by gzip'
f.close()

# clean up
os.unlink(filename)