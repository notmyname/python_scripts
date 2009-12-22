#!/usr/bin/env python

import os
import cloudfiles

username = 'xxxx'
apikey = 'xxxx'

conn = cloudfiles.get_connection(username, apikey)

container = conn.create_container('api_speed_test3')
data_list = ('test_data/%s'%x for x in os.listdir('test_data') if x.endswith('.dat'))
for filename in data_list:
    try:
        obj = container.create_object(filename)
        obj.load_from_filename(filename)
    except cloudfiles.errors.ResponseError, err:
        print err
print len(container.list_objects())