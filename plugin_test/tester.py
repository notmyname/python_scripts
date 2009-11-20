#!/usr/bin/env python2.4

from plugin_engine import plugin_engine

print 'API: %s' % plugin_engine.API()
print
print plugin_engine.Foo.hello()
print plugin_engine.Bar.where()
print plugin_engine.Another.x.Y()
