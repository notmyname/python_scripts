#!/usr/bin/env python2.4

import os

class Provider(object):
    def __init__(self, plugin_location='./plugins'):
	self.__plugins = {}
	if os.path.isdir(plugin_location):
	    print 'Loading plugins'
	    possible = os.listdir(plugin_location)
	    count = 0
	    for plugin_file in (filename[:-3] for filename in possible if filename != '__init__.py' and filename.endswith('.py')):
		print '\tLoading %s:' % plugin_file,
		#f = open(plugin_file,'rb')
		#data = f.read()
		#f.close()
		try:
		    #plugin = eval(data).root
		    plugin = __import__('plugins.%s'%plugin_file,globals(),locals(),['plugins']).root
		except AttributeError:
		    print 'Plugin has no root attribute'
		    continue
		except:
		    print 'Error importing plugin'
		    raise
		    continue
		else:
		    print 'Done'
		    self.register(plugin)
		    count += 1
	    print 'Done (%d plugins loaded)\n' % count

    def register(self,plugin):
	try:
	    plugin.onRegister()
	except AttributeError:
	    pass
	name = plugin.__class__.__name__
	self.__plugins[name] = plugin

    def API(self):
	api = {}
	for i,j in self.__plugins.items():
	    api[i] = dir(j)
	return api

    def __getattr__(self,name):
	if name in self.__plugins:
	    return self.__plugins[name]
	else:
	    return super(Provider,self).__getattr__(name)

plugin_engine = Provider()
