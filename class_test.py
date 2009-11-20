class Foo(object):
    def bar(self):
        print self.baz
        print isinstance(self, SubFoo)

class SubFoo(Foo):
    def __init__(self):
        self.baz = 'test'
    def bar(self):
        super(SubFoo,self).bar()

x = SubFoo()
x.bar()
