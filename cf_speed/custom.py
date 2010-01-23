#!/usr/bin/python

import os
import httplib

from cf_auth import username, apikey

# auth
conn = httplib.HTTPSConnection('api.mosso.com')
conn.request('GET', '/auth', headers={'x-auth-user': username, 'x-auth-key': apikey})
resp = conn.getresponse()
auth_token = resp.getheader('x-auth-token')
url = resp.getheader('x-storage-url')
conn.close()
# send data
send_headers = {'X-Auth-Token': auth_token, 'Content-Type': 'text/plain'}
container_path = '/'+'/'.join(url.split('/')[3:])+'/api_speed_test2'
conn = httplib.HTTPSConnection(url.split('/')[2])
conn.request('PUT', container_path, headers=send_headers)
conn.getresponse().read()
data_list = ('test_data/%s'%x for x in os.listdir('test_data') if x.endswith('.dat'))
for filename in data_list:
    f = open(filename)
    conn.request('PUT', container_path+'/'+filename, body=f, headers=send_headers)
    f.close()
    resp = conn.getresponse()
    resp.read()
    if resp.status >= 300:
        print resp.status, resp.reason, container_path+'/'+filename
conn.close()