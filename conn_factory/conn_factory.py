#!/usr/bin/env python

from contextlib import contextmanager
from eventlet.pools import Pool

from uuid import uuid4

class StaleConnectionError(Exception):
    '''raised when something goes wrong with a Connection'''

class ProcessingError(Exception):
    '''raised when something goes wrong with a Connection'''


class Connection(object):
    def __init__(self):
        self.value = uuid4().hex
        print 'new connection %s created' % self.value

    def __call__(self, err=False, stale=False):
        if not stale:
            if err:
                raise ProcessingError('error on connection %s' % self.value)
            return 'connection %s' % self.value
        else:
            raise StaleConnectionError('connection %s not active' % self.value)


def new_connection():
    return Connection()

@contextmanager
def PoolManager(pool):
    """
    Given a pool, handle item management (like stale items in the pool)
    while passing other errors to the calling method.
    """
    i = pool.get()
    try:
        yield i
    except StaleConnectionError, err:
        print err
    else:
        print i(), 'returned to pool'
        pool.put(i)

if __name__ == '__main__':
    pool_size = 5
    p = Pool(min_size=1, max_size=pool_size, create=new_connection)
    attempts = 1
    max_attempts = 5
    stale = True
    while attempts < max_attempts:
        with PoolManager(p) as i:
            try:
                attempts += 1
                print 'starting attempt %s' % attempts
                print i()
                print i(stale=stale)
                #print i(err=True)
            except ProcessingError, err:
                print err, 'as expected'
            else:
                break
        stale = False
