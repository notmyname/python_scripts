# Common.py
#
# requires Python 2.4 or later
#
# a collection of useful tools
#
# writen by John Dickinson
#    with help from a few other sources (the Internet and books)

import sys                   # for logged_function, handle_exception
import time                  # for deferred_thread,logged_function
import os                    # for deferred_fork
import cPickle               # for deferred_fork
import signal                # for deferred_fork
from threading import Thread # for deferred_thread
import copy                  # for deep_update
import traceback             # for handle_exception
import logging               # for handle_exception

#########################
# example usage:
#
# @deferred_thread
# def foo():
#    ...long running task...
#
# ...in your code...
# x = foo()
# ...some time passes...
# print x() <-- prints result from foo

class DeferredThread(object):
    def __init__(self,f,*a,**kw):
        self.__f = f
        self.__exception = None
        self.__thread = Thread(target=self.runfunc,args=a,kwargs=kw)
        time.sleep(0) # give other threads a chance to run
        self.__thread.start()
        
    def __call__(self, *a, **kw):
        self.__thread.join()
        if self.__exception is not None:
            raise self.__exception
        return self.__val

    def runfunc(self,*a,**kw):
        try:
            self.__val = self.__f(*a,**kw)
        except Exception, e:
            self.__exception = e

def deferred_thread(f):
    def wrapper(*a,**kw):
        return DeferredThread(f,*a,**kw)
    wrapper.__name__ = f.__name__
    return wrapper

#########################
# example usage:
#
# @deferred_fork
# def foo():
#    ...long running task...
#
# ...in your code...
# x = foo()
# ...some time passes...
# print x() <-- prints result from foo
#
# Caveat: The function you wrap must return pickle'able objects.

class DeferredForkError(Exception):
    pass

class DeferredFork(object):
    def __init__(self,f,*a,**kw):
        self.__result = None
        self.__called_before = False
        self.__exit_status = 0
        self.__r,w = os.pipe()
        self.__pid = os.fork()
        if self.__pid:
            # we are the parent
            os.close(w)
        else:
            # we are the child
            os.close(self.__r)
            ret_code = 0
            out_msg = None
            try:
                out_msg = f(*a,**kw)
            except:
                ret_code = 1
                import traceback, StringIO
                err = StringIO.StringIO()
                traceback.print_exc(file=err)
                out_msg = err.getvalue()
                err.close()
            w = os.fdopen(w,'wb')
            w.write(cPickle.dumps(out_msg))
            w.close()
            os._exit(ret_code)
            #sys.exit(ret_code)

    def __call__(self, *a, **kw):
        if not self.__called_before:
            r = os.fdopen(self.__r, 'rb')
            self.__result = cPickle.loads(r.read())
            r.close()
            self.__exit_status = os.waitpid(self.__pid,0)[1] >> 8
            self.__called_before = True
        if self.__exit_status:
            raise DeferredForkError,self.__result
        return self.__result

def deferred_fork(f):
    def wrapper(*a, **kw):
        return DeferredFork(f,*a,**kw)
    wrapper.__name__ = f.__name__
    return wrapper

##########################
# example usage:
#
# times2 = curry(operator.mul,2)
# print times2(4) <-- prints 8

def curry(f, *a, **kw):
    def curried(*more_a, **more_kw):
        return f(*(a+more_a), **dict(kw, **more_kw))
    return curried


##########################
# example usage:
#
# @logged_function
# def foo():
#   pass
#
# @logged_funtion('post',open('/tmp/log'))
# def bar():
#   pass
#
# @logged_funtion(when='post',out=open('/tmp/log'))
# def bar():
#   pass

def logged_function(*args,**kw):
    # handle variations of calls for decorators
    try:
        callit = args[0]
    except IndexError:
        callit = lambda func: logged_function(func,*args,**kw)
    if not callable(callit):
        return lambda func: logged_function(func,*args,**kw)

    # set parameters (or use defaults)
    when = 'pre'
    out = sys.stderr
    try:
        when = kw.get('when') or args[1]
    except:
        pass
    try:
        out = kw.get('out') or args[2]
    except:
        pass

    # now, the work
    def pre_logged(f):
        def wrapper(*a, **kw):
            a_list = ','.join(`i` for i in a)
            kw_list = ','.join('%s=%s'%(k,`v`) for k,v in kw.items())
            params = ','.join([a_list,kw_list]).strip(',')
            print >>out, 'Log: %s(%s) called' % (f.__name__,params)
            out.flush()
            return f(*a, **kw)
        wrapper.__name__ = f.__name__
        return wrapper
    def post_logged(f):
        def wrapper(*a, **kw):
            try:
                start = time.time()
                return f(*a, **kw)
            finally:
                stop = time.time()
                a_list = ','.join(`i` for i in a)
                kw_list = ','.join('%s=%s'%(k,`v`) for k,v in kw.items())
                params = ','.join([a_list,kw_list]).strip(',')
                print >>out, 'Log: %s(%s) called (duration : %.4f)' % (f.__name__,params, stop-start)
                out.flush()
        wrapper.__name__ = f.__name__
        return wrapper
    return {'pre':pre_logged,'post':post_logged}[when](callit)


##########################
# like a typical dictionary update, but if for a key
# both values are a dict, merge those recursively

def deep_update(d1,d2):
    if type(d1) is not type({}) or type(d2) is not type({}):
        return None

    res = copy.deepcopy(d1)
    for key in d2:
        if not d1.has_key(key):
            res[key] = None
        t1 = type(d1.get(key))
        t2 = type(d2.get(key))
        if t1 is t2 and t1 is type({}):
            res[key] = deep_update(d1[key],d2[key])
        else:
            res[key] = d2[key]

    return res


##########################
# arbitrary infix notation
#
# example usage:
#
# @infix
# def foo(left,right):
#     return left+right
# print 2 |foo| 2 # prints 4
# print 2 <<foo>> 2 # prints 4
# print 2 >>foo<< 2 # prints 4

class Infix(object):
    def __init__(self,func):
        self._func = func

    # |foo|
    def __or__(self,other):
        return self._func(other)
    def __ror__(self,other):
        return Infix(lambda x: self._func(other,x))

    # <<foo>>
    def __rshift__(self,other):
        return self._func(other)
    def __rlshift__(self,other):
        return Infix(lambda x: self._func(other,x))

    # >>foo<<
    def __lshift__(self,other):
        return self._func(other)
    def __rrshift__(self,other):
        return Infix(lambda x: self._func(other,x))

    def __call__(self,a,b):
        return self._func(a,b)
def infix(f):
    return Infix(f)


##########################
# callback decorator
#
# example usage:
#
# def my_callback(called_proc,called_proc_result):
#   pass
#
# @add_callback(my_callback) # addl args will be passed to callback funtion
# def long_running():
#   pass

def add_callback(callback_proc,*args,**kw):
    def executor(f):
        def wrapped(*wrapped_a,**wrapped_kw):
            try:
                res = f(*wrapped_a,**wrapped_kw)
            finally:
                callback_proc(f,res,*args,**kw)
        wrapped.__name__ = f.__name__
        return wrapped
    return executor

##########################
# handle_exception decorator
#
# example usage:
#
# @handle_exception
# def foo(a,b,c):
#   raise Exception, 'Oh no!'
#
# @handle_exception(open('/tmp/error.log','ab'))
# def foo(a,b,c):
#   raise Exception, 'Oh no!'

def handle_exception(out_file=None):
    '''wraps a function and catches errors in it
    if out is given, it is an open file object
    if out is None (default), messages will be logged with logging.getLogger().error(...)
    '''
    def wrapper(f):
        def wrapped(*a, **kw):
            try:
                ret = f(*a, **kw)
            except:
                try:
                    t, v, _tb = sys.exc_info()
                    tb = traceback.format_exc(_tb)
                finally: # see http://docs.python.org/lib/module-sys.html
                    del _tb
                msg = '%s caught in %s:\n%s' % (t, f.__name__, tb)
                if out_file is None:
                    logging.getLogger().error(msg)
                else:
                    out_file.write('%s\n' % msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        return wrapped
    if callable(out_file):
        f = out_file
        out_file = None
        return wrapper(f)
    else:
        return wrapper
