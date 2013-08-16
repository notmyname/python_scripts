#!/usr/bin/env python

# import eventlet
# eventlet.monkey_patch()

import sys
import httplib
import os
import time

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

body = 'x' * 16384

for i in xrange(1):
    conn.request(
        'PUT', CONTAINER_PATH + '/test_%d' % i, body=body,
        headers=SEND_HEADERS)
    resp = conn.getresponse()
    print resp.read()
conn.close()
