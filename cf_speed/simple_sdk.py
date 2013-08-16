#!/usr/bin/env python

# import eventlet
# eventlet.monkey_patch()

import sys
import os
import time

import swiftclient
from cf_auth import username, apikey

auth_endpoint = 'https://auth.api.rackspacecloud.com/v1.0'
container_name = sys.argv[1]

conn = swiftclient.Connection(
   authurl=auth_endpoint, user=username, key=apikey, ssl_compression=False)
conn.put_container(container_name)

body = 'x' * 16384

for i in xrange(1):
    conn.put_object(
        container_name, 'test_%d' % i, body, content_type='text/plain')
