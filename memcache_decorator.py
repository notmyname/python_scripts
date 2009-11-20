import hashlib
import memcache
import functools

memcache_servers = ['localhost:11211','localhost:11212','localhost:11213','localhost:11214']

def use_memcache(func):
    cache = memcache.Client(memcache_servers)
    func.get_stats = cache.get_stats
    @functools.wraps(func)
    def wrapped(*a, **kw):
        h = hashlib.sha1()
        h.update(func.__name__)
        h.update(repr(a))
        # go throught kw in an orderly manner to ensure
        # that the hash stays the same for every call
        for k in sorted(kw.iterkeys()):
            h.update(k)
            h.update(repr(kw[k])) # of course, if this is a dict, our clever scheme may not work
        key = h.hexdigest()
        ret = cache.get(key)
        if ret is None:
            ret = func(*a, **kw)
            cache.set(key, ret)
        return ret
    return wrapped
