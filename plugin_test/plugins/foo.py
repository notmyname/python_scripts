# test plugin

class Foo(object):
    def hello(self):
	return 'hello world'
    hello.exposed = True

root = Foo()
