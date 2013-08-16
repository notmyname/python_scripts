#!/usr/bin/env python

import eventlet
eventlet.monkey_patch(all=False, socket=True)

import sys
import os
import time

import swiftclient
from cf_auth import username, apikey

auth_endpoint = 'https://auth.api.rackspacecloud.com/v1.0'
container_name = sys.argv[1]


conn = swiftclient.Connection(
   authurl=auth_endpoint, user=username, key=apikey)
conn.put_container(container_name)


def run(filename_list):
    conn = swiftclient.Connection(
        authurl=auth_endpoint, user=username, key=apikey)
    for filename in filename_list:
        start = time.time()
        with open(filename, 'rb') as f:
            conn.put_object(
                container_name, filename, f, content_type='text/plain',
                chunk_size=65535)
        print '%s uploaded in %.4f seconds' % (filename, (time.time()-start))
        sys.stdout.flush()

data_list = ['test_data/%s' % x for x in os.listdir('test_data')
             if x.endswith('.dat')]
len_data_list = len(data_list)
concurrency = min(len_data_list, 20)
print 'uploading %d files with a concurrency of %d' % (len_data_list, concurrency)
pool = eventlet.GreenPool(size=concurrency)
for i in xrange(len_data_list / concurrency):
    pool.spawn(run, data_list[concurrency*i:concurrency*(i+1)])
pool.waitall()
