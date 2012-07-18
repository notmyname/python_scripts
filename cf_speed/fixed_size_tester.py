#!/usr/bin/python

import sys
import os
import httplib
import time

from cf_auth import username, apikey

container_name = sys.argv[1]
bytes_to_upload = int(sys.argv[2])
use_service_net = os.environ.get('USECFSERVICENET', False)

# auth
conn = httplib.HTTPSConnection('auth.api.rackspacecloud.com')
conn.request('GET', '/auth',
             headers={'x-auth-user': username, 'x-auth-key': apikey})
resp = conn.getresponse()
auth_token = resp.getheader('x-auth-token')
url = resp.getheader('x-storage-url')
conn.close()
# send data
send_headers = {'X-Auth-Token': auth_token, 'Content-Type': 'text/plain'}
container_path = '/' + '/'.join(url.split('/')[3:]) + '/' + container_name
storage_url = url.split('/')[2]
if use_service_net:
    storage_url = 'snet-' + storage_url
conn = httplib.HTTPSConnection(storage_url)
conn.request('PUT', container_path, headers=send_headers)
conn.getresponse().read()
body = 'x' * bytes_to_upload
filename = '%d_bytes' % bytes_to_upload
start = time.time()
conn.request('PUT', container_path + '/' + filename, body=body, headers=send_headers)
resp = conn.getresponse()
resp.read()
dur = time.time() - start
if resp.status >= 300:
    print resp.status, resp.reason, container_path + '/' + filename
else:
    print 'uploaded %d bytes in %.4f seconds' % (bytes_to_upload, dur)
start = time.time()
conn.request('GET', container_path + '/' + filename, headers=send_headers)
resp = conn.getresponse()
resp.read()
dur = time.time() - start
if resp.status >= 300:
    print resp.status, resp.reason, container_path + '/' + filename
else:
    print 'downloaded %d bytes in %.4f seconds' % (bytes_to_upload, dur)
conn.close()
