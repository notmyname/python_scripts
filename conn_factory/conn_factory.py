#!/usr/bin/env python

from contextlib import contextmanager
from eventlet.pools import Pool

counter = 0

class StaleConnectionError(Exception):
    '''raised when something goes wrong with a Connection'''

class ProcessingError(Exception):
    '''raised when something goes wrong with a Connection'''


class Connection(object):
    def __init__(self):
        global counter
        counter += 1
        self.active = True
        self.value = counter
        print 'new connection created'

    def __call__(self, err=False):
        if self.active:
            if err:
                raise ProcessingError('blargh')
            return 'connection %d' % self.value
        else:
            raise StaleConnectionError('not an active connection')


def new_connection():
    return Connection()

@contextmanager
def PoolManager(pool):
    """
    Given a pool, handle item management (like stale items in the pool)
    while passing other errors to the calling method.
    """
    try:
        with pool.item() as i:
            yield i
    except StaleConnectionError:
        # what happens here?
        pass

if __name__ == '__main__':
    pool_size = 5
    p = Pool(min_size=1, max_size=pool_size, create=new_connection)
    with PoolManager(p) as i:
        print i()  # should be fine
        i.active = False
        print i()  # should be a new connection
        try:
            i(err=True)
        except ProcessingError:
            print 'some processing error caught here, as expected'
