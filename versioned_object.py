import time
import copy

class VersionedObject(object):
    class VersionDelta(object):
        def __init__(self, key, value, msg, meta=None):
            self.key = key
            self.value = value
            self.msg = msg
            if meta is None:
                meta = {}
            if not meta.get('timestamp'):
                meta['timestamp'] = time.ctime()
            self.meta = meta
        def __str__(self):
            return '%s: %s (meta: %s) -> %s' % (self.key, self.value, self.meta, self.msg)
        def __repr__(self):
            return str(self)
    
    def __init__(self, *a, **kw):
        super(VersionedObject, self).__init__()
        self.history = []
    
    def __setattr__(self, name, value):
        if name != 'history':
            delta = VersionedObject.VersionDelta(name, value, 'updated value of %s to %s' % (name, value))
            self.history.append(delta)
        super(VersionedObject, self).__setattr__(name, value)
    
    def set_meta(self, new_meta):
        tmp = copy.deepcopy(self.history[-1].meta)
        tmp.update(new_meta)
        new_meta = tmp
        delta = VersionedObject.VersionDelta('meta', new_meta, 'updated metadata', new_meta)
        self.history.append(delta)
    
    def set_history(self, new_history):
        self.history = new_history
        for delta in self.history:
            super(VersionedObject, self).__setattr__(delta.key, delta.value)

if __name__ == '__main__':
    class Klass(VersionedObject):
        def __init__(self, a, b):
            super(Klass, self).__init__()
            self.a = a
            self.b = b
        def __str__(self):
            return 'Klass(%s, %s)' % (self.a, self.b)

    k = Klass(1,2)
    print k
    k.b = 3
    print k
    print '\n'.join(str(x) for x in k.history)
    h = k.history
    y = Klass(3,4)
    print y
    print '\n'.join(str(x) for x in y.history)
    y.set_history(h)
    print 'changed history'
    print '\n'.join(str(x) for x in y.history)
    print y
    y.set_meta({'timestamp':'foobar', 'baz':3})
    print 'changed meta'
    print y
    print '\n'.join(str(x) for x in y.history)
