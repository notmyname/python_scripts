#!/usr/bin/env python

from webob import Request, Response
import os
class App(object):
    def __call__(self, environ, start_response):
        res = Response(conditional_response=True)
        res.body = ''.join(str(i) for i in xrange(10))
        res.content_length = 10
        return res(environ, start_response)

for d in ['Wed, 31 Dec 1970 09:59:59 GMT',
        'Wed, 31 Dec 1970 08:59:59 GMT',
        'Wed, 31 Dec 1970 07:59:59 GMT',
        'Wed, 31 Dec 1970 06:59:59 GMT',
        'Wed, 31 Dec 1970 05:59:59 GMT',
        'Wed, 31 Dec 1970 04:59:59 GMT',
        'Wed, 31 Dec 1970 03:59:59 GMT',
        'Wed, 31 Dec 1970 02:59:59 GMT',
        'Wed, 31 Dec 1970 01:59:59 GMT',
        'Wed, 31 Dec 1970 00:59:59 GMT',
        'Wed, 31 Dec 1969 23:59:59 GMT',
        'Wed, 31 Dec 1969 22:59:59 GMT',
        'Wed, 31 Dec 1969 21:59:59 GMT',
        'Wed, 31 Dec 1969 20:59:59 GMT',
        'Wed, 31 Dec 1969 19:59:59 GMT',
        'Wed, 31 Dec 1969 18:59:59 GMT',
        'Wed, 31 Dec 1969 17:59:59 GMT',
        'Wed, 31 Dec 1969 16:59:59 GMT',
        'Wed, 31 Dec 1969 15:59:59 GMT',
        'Wed, 31 Dec 1969 14:59:59 GMT']:
    req = Request.blank('/')
    req.headers['If-Unmodified-Since'] = d
    print req
    print '-'*30
    print req.get_response(App())