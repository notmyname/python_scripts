#!/usr/bin/env python

import sys
import os
import cloudfiles

from cf_auth import username, apikey

container_name = sys.argv[1]

conn = cloudfiles.get_connection(username, apikey)

container = conn.create_container(container_name)
data_list = ('test_data/%s' % x for x in os.listdir('test_data')
             if x.endswith('.dat'))
for filename in data_list:
    try:
        obj = container.create_object(filename)
        obj.load_from_filename(filename)
    except cloudfiles.errors.ResponseError, err:
        print err
