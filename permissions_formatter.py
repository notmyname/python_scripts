#!/usr/bin/env python

def formatter(permission_bits):
    u,g,a = (permission_bits & 0700) >> 6, (permission_bits & 0070) >> 3, permission_bits & 0007
    out = ['-']
    perms = {2:'r',1:'w',0:'x'}
    for part in [u,g,a]:
        for i in xrange(2,-1,-1):
            if part & (1 << i): out.append(perms[i])
            else: out.append('-')
    return ''.join(out)

def formatter_new(permission_bits):
    out = ['-']
    perms = {2:'r',1:'w',0:'x'}
    for j in xrange(2,-1,-1):
        for i in xrange(2,-1,-1):
            print (permission_bits & (0700>>(2-j))) >> (j*3)
            if ((permission_bits & (0700>>(2-j))) >> (j*3)) & (1 << i): out.append(perms[i])
            else: out.append('-')
    return ''.join(out)

print formatter(0777), '-rwxrwxrwx'
print formatter(0666), '-rw-rw-rw-'
print formatter(0755), '-rwxr-xr-x'
print formatter(0600), '-rw-------'
print formatter(0644), '-rw-r--r--'
