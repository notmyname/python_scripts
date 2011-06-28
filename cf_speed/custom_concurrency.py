#!/usr/bin/env python

import eventlet
eventlet.monkey_patch()

import sys
import httplib
import os

from cf_auth import username, apikey

container_name = sys.argv[1]

# auth
conn = httplib.HTTPSConnection('auth.api.rackspacecloud.com')
conn.request('GET', '/auth',
             headers={'x-auth-user': username, 'x-auth-key': apikey})
resp = conn.getresponse()
AUTH_TOKEN = resp.getheader('x-auth-token')
URL = resp.getheader('x-storage-url')
CONNECTION_ENDPOINT = URL.split('/')[2]
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
        with open(filename, 'rb') as f:
            conn.request('PUT', CONTAINER_PATH + '/' + filename, body=f,
                     headers=SEND_HEADERS)
        resp = conn.getresponse()
        resp.read()
    conn.close()

data_list = ['test_data/%s' % x for x in os.listdir('test_data')
             if x.endswith('.dat')]
concurrency = 20
pool = eventlet.GreenPool(size=concurrency)
[pool.spawn(run, data_list[concurrency*i:concurrency*(i+1)])
    for i in xrange(len(data_list)/concurrency)]
pool.waitall()
