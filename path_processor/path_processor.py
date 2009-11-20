# Author: John Dickinson

'''simple way to apply a function to everything in a directory'''

import logging
import logging.handlers
import glob
import os
import sys
try:
    import processing
    USE_PROCESSING = True
except ImportError:
    USE_PROCESSING = False

MAX_LOG_SIZE = 1024 * 1024 * 2 # 2MB
LOGS_TO_KEEP = 100
script_name = os.path.splitext(os.path.split(sys.argv[0])[-1])[0]
LOG_DIR = '/tmp/%s' % script_name
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_NAME = '%s/%s.log' % (LOG_DIR, script_name)
    
def _init_logger(log_file_name):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(message)s'))
    file_handler = logging.handlers.RotatingFileHandler(log_file_name, 'ab', MAX_LOG_SIZE, LOGS_TO_KEEP)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(message)s'))
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

_init_logger(LOG_NAME)

class Processor(object):
    def __init__(self, directory_path, glob_pattern='*', apply_function=None, serialize=True, fold=False):
        if not directory_path.endswith('/'):
            directory_path += '/'
        self.directory_path = directory_path
        self.glob_pattern = glob_pattern
        self.mutator = apply_function
        self.serialize = serialize
        self.fold = fold
    
    def get_processing_files(self):
        return glob.glob(self.directory_path+'*.processing')
    
    def remove_done_files(self):
        done_files = glob.glob(self.directory_path+'*.done')
        for path in done_files:
            os.remove(path)
    
    def start(self, **kwargs):
        if self.mutator is None:
            return
        logger = logging.getLogger()
        file_listing = [x for x in glob.glob(self.directory_path+self.glob_pattern) if not x.endswith('.done') and not x.endswith('.processing')]
        if not file_listing:
            logger.info('file listing for %s returned no files to process', self.directory_path)
        if self.serialize:
            result = {}
            last = None
            first_time = True
            for path in file_listing:
                if self.fold and not first_time:
                    path = last
                try:
                    old_name = path
                    new_name = os.path.splitext(path)[0] + '.processing'
                    os.rename(path, new_name)
                    path = new_name
                    logger.info('calling %s on %s', self.mutator.__name__, path)
                    result[old_name] = last = self.mutator(path, **kwargs)
                    os.rename(path, os.path.splitext(path)[0] + '.done')
                except Exception, err:
                    result[path] = last = err
                first_time = False
            return result
        elif USE_PROCESSING:
            pool = processing.Pool()
            result_proxies = []
            for path in file_listing:
                old_name = path
                new_name = os.path.splitext(path)[0] + '.processing'
                os.rename(path, new_name)
                path = new_name
                logger.info('calling %s on %s', self.mutator.__name__, path)
                result_proxies.append((old_name, path, pool.apply_async(self.mutator, args=(path,), kwds=kwargs)))
            results = {}
            for old_name, path, result in result_proxies:
                try:
                    os.rename(path, os.path.splitext(path)[0] + '.done')
                    path = old_name
                    results[path] = result.get()
                except Exception, err:
                    results[path] = err
            return results

if __name__ == '__main__':
    
    def test(path, **kwargs):
        #print kwargs
        #raise Exception('hello')
        return path*2
    
    print 'Example 1: async:'
    p = Processor('test', apply_function=test, serialize=False)
    print p.start(test='some kwarg')
    
    #print
    #print 'Example 2: syncronous with fold:'
    #p = Processor('test', apply_function=test, fold=True)
    #print p.start(test='some kwarg')
    
    print
    print 'Example 3: syncronous without folding:'
    p = Processor('test', apply_function=test)
    print p.start(test='some kwarg')
