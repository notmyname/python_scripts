#!/usr/bin/env python

import eventlet
eventlet.monkey_patch(all=False, socket=True)

import sys
import httplib
import os
import time

from cf_auth import username, apikey

container_name = sys.argv[1]

use_service_net = os.environ.get('USECFSERVICENET', False)

# auth
conn = httplib.HTTPSConnection('auth.api.rackspacecloud.com')
conn.request('GET', '/auth',
             headers={'x-auth-user': username, 'x-auth-key': apikey})
resp = conn.getresponse()
AUTH_TOKEN = resp.getheader('x-auth-token')
URL = resp.getheader('x-storage-url')
CONNECTION_ENDPOINT = URL.split('/')[2]
if use_service_net:
    CONNECTION_ENDPOINT = 'snet-' + CONNECTION_ENDPOINT
conn.close()

SEND_HEADERS = {'X-Auth-Token': AUTH_TOKEN, 'Content-Type': 'text/plain'}
CONTAINER_PATH = '/' + '/'.join(URL.split('/')[3:]) + '/' + container_name

# create the container
conn = httplib.HTTPSConnection(CONNECTION_ENDPOINT)
conn.request('PUT', CONTAINER_PATH, headers=SEND_HEADERS)
conn.getresponse().read()
conn.close()


def run(filename_list):
    conn = httplib.HTTPSConnection(CONNECTION_ENDPOINT)
    for filename in filename_list:
        start = time.time()
        with open(filename, 'rb') as f:
            conn.request('PUT', CONTAINER_PATH + '/' + filename, body=f,
                     headers=SEND_HEADERS)
        resp = conn.getresponse()
        resp.read()
        print '%s uploaded in %.4f seconds' % (filename, (time.time()-start))
        sys.stdout.flush()
    conn.close()

data_list = ['test_data/%s' % x for x in os.listdir('test_data')
             if x.endswith('.dat')]
len_data_list = len(data_list)
concurrency = min(len_data_list, 20)
print 'uploading %d files with a concurrency of %d' % (len_data_list, concurrency)
pool = eventlet.GreenPool(size=concurrency)
for i in xrange(len_data_list / concurrency):
    pool.spawn(run, data_list[concurrency*i:concurrency*(i+1)])
pool.waitall()
