#!/usr/bin/env python2.4

hex_values = ['%X'%x for x in range(16)]

hex_data = ''.join(hex_values) * 16 * 256

len_hex_data = len(hex_data)

def compress_hex_str(data):
    res = []
    for i in range(0,len(data),2):
	a = int(data[i],16)
	b = int(data[i+1],16)
	blob = (a << 4L) | b
	res.append(chr(blob))
    return ''.join(res)

def expand_hex_str(data):
    res = []
    for i in range(len(data)):
	blob = ord(data[i])
	top = blob >> 4L
	bottom = blob & 15L
	res.append('%X'%top)
	res.append('%X'%bottom)
    return ''.join(res)

c_data = compress_hex_str(hex_data)
len_c_data = len(c_data)
print len_hex_data
print len_c_data
#print hex_data
#print `c_data`
#print expand_hex_str(c_data)

print '%.4f%% compression' % (100.0 - 100.0*float(len_c_data)/float(len_hex_data))

assert hex_data == expand_hex_str(c_data)
