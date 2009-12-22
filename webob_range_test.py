#!/usr/bin/env python

from webob import Request, Response
import os
class App(object):
    def __call__(self, environ, start_response):
        res = Response(conditional_response=True)
        res.body = ''.join(str(i) for i in xrange(10))
        res.content_length = 10
        return res(environ, start_response)

req = Request.blank('/')
req.range = (9,20)
print req
print '-'*30
print req.get_response(App())


class App2(object):
    def __call__(self, environ, start_response):
        res = Response(conditional_response=True)
        def x():
            for i in xrange(10):
                yield str(i)
        res.app_iter = x()
        res.content_length = 10
        return res(environ, start_response)

req = Request.blank('/')
req.range = (9,20)
print req
print '-'*30
print req.get_response(App2())