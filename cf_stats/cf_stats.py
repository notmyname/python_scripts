#!/usr/bin/env python

import sys
import collections
import gzip
import cStringIO
import re

import cloudfiles

import cf_auth

conn = cloudfiles.get_connection(username=cf_auth.username, api_key=cf_auth.apikey)
log_container_name = '.CDN_ACCESS_LOGS'
try:
    log_container = conn.get_container(log_container_name)
except NameError:
    print >>sys.stderr, 'No CDN logs found'
    sys.exit(1)

class LogLine(object):
    def __init__(self, ip, ident, http_user, date, request_line, response_code, response_size, referrer, user_agent):
        self.ip = ip
        self.ident = ident
        self.http_user = http_user
        self.date = date.split(':', 1)[0]
        self.request_line = request_line
        self.method, self.obj_url = request_line.split(' ', 1)
        obj_url, _ = self.obj_url.rsplit(' ', 1)
        _, self.obj_name = obj_url[7:].split('/', 1)
        self.response_code = response_code
        self.response_size = response_size
        self.referrer = referrer
        self.user_agent = user_agent

class LogStats(object):
    def __init__(self, group_on='obj_name'):
        self.objs = collections.defaultdict(dict)
        self.group_on = group_on
    
    def add(self, log_line):
        d = self.objs[getattr(log_line, self.group_on)]
        if 'count' not in d:
            d['count'] = 0
        d['count'] += 1
        for key in 'obj_name ip ident http_user date request_line response_code response_size referrer user_agent'.split():
            val = getattr(log_line, key)
            if key in d:
                d[key].add(val)
            else:
                d[key] = set([val])
    
    def __str__(self):
        ret = []
        for k in self.objs:
            d = self.objs[k]
            ret.append('Object Name: %s' % ' '.join(d['obj_name']))
            ret.append('Count: %d' % d['count'])
            ret.append('User Agents: "%s"' % '" "'.join(d['user_agent']))
            ret.append('Response: %s' % ' '.join(d['response_code']))
            ret.append('Referrers: %s' % ' '.join(d['referrer']))
            ret.append('IPs: %s' % ' '.join(d['ip']))
            ret.append('Dates: %s' % ' '.join(d['date']))
            ret.append('')
        return '\n'.join(ret)

log_files = log_container.list_objects()
aggregate_stats = LogStats()
log_line_regex = re.compile(r'(\d+\.\d+\.\d+\.\d+) (.*) (.*) \[(.*)\] "(.*)" (\d+) (.*) "(.*)" "(.*)"')
for filename in log_files[:20]:
    container_name, date = filename[:-23], filename[-22:]
    log_obj = log_container.get_object(filename)
    buf = cStringIO.StringIO(log_obj.read())
    plain = gzip.GzipFile(fileobj=buf).read()
    for line in plain.split('\n'):
        if not line:
            continue
        m = log_line_regex.match(line)
        log_line = LogLine(*m.groups())
        aggregate_stats.add(log_line)
    
print aggregate_stats
