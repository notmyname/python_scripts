import time
import datetime
import subprocess
import os

def get_result(cmd):
    x = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    ret = x.stdout.read().strip()
    x.stdout.close()
    return ret

def get_available():
    raw = int(get_result('/usr/sbin/zfs get -H -o value -p available tank').strip())
    return raw

def get_used():
    raw = int(get_result('/usr/sbin/zfs get -H -o value -p used tank').strip())
    return raw

def get_uptime():
    raw = get_result('/usr/gnu/bin/uptime')
    if 'day' in raw:
        parts = raw.split()[2:5]
        days = int(parts[0])
        hours, minutes = parts[2][:-1].split(':')
    else:
        parts = raw.split()
        days = 0
        hours, minutes = parts[2][:-1].split(':')
    hours = int(hours)
    minutes = int(minutes)
    return '%d days, %d hours, %s minutes' % (days, hours, minutes)

stats = {}
start_time = time.time()

rpool_status = 'Not Healthy' # assume the worst
if get_result('/usr/sbin/zpool status -x rpool').endswith('is healthy'):
    rpool_status = 'Healthy'
stats['rpool_healthy'] = rpool_status

tank_status = 'Not Healthy' # assume the worst
if get_result('/usr/sbin/zpool status -x tank').endswith('is healthy'):
    tank_status = 'Healthy'
stats['tank_healthy'] = tank_status

stats['file_server_uptime'] = get_uptime()

try:
    t = os.stat('/tank/backups/imac_sync_file').st_mtime
    stats['imac_last_backup_age'] = datetime.timedelta(seconds=(time.time()-t))
    t = time.strftime('%X %m/%d/%Y', time.localtime(t))
    stats['imac_last_backup'] = t
except OSError:
    stats['imac_last_backup'] = None

try:
    t = os.stat('/tank/backups/karen_laptop_sync_file').st_mtime
    stats['karen_last_backup_age'] = datetime.timedelta(seconds=(time.time()-t))
    t = time.strftime('%X %m/%d/%Y', time.localtime(t))
    stats['karen_last_backup'] = t
except OSError:
    stats['karen_last_backup'] = None

try:
    t = os.stat('/tank/backups/work_backup_sync_file').st_mtime
    stats['work_last_backup_age'] = datetime.timedelta(seconds=(time.time()-t))
    t = time.strftime('%X %m/%d/%Y', time.localtime(t))
    stats['work_last_backup'] = t
except OSError:
    stats['work_last_backup'] = None

free = get_available()
used = get_used()
total = float(free + used)
free = free / total * 100.0
used = used / total * 100.0
stats['space_available'] = '%.2f %%' % free
stats['space_used'] = '%.2f %%' % used

stats['current_time'] = time.strftime('%X %m/%d/%Y')

stats['run_time'] = time.time() - start_time

template = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Dashboard</title>
<link href="styles.css" rel="stylesheet" type="text/css" />
<meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
<meta name="format-detection" content="telephone=no" />
</head>
<body>
<h1>Dashboard</h1>
%s
<div id="current_time">
    Stats at <span>%s</span>
</div>
</body>
</html>
'''

disk_stats = '<div id="disk_space"><h3>Disk Space</h3><div id="space_used"><span>Used</span><span>%(space_used)s</span></div><div id="space_available"'
if stats['space_available'] < (50 * 2**30):
    disk_stats += ' class="warning"'
disk_stats += '><span>Available</span><span>%(space_available)s</span></div></div>'

uptime = '''
<div id="uptime">
    <h3>Uptime</h3>
    <div id="uptime_data">%(file_server_uptime)s</div>
</div>
'''

pools = '<div id="pools"><h3>Filesystem Status</h3><div id="rpool_status"'
if stats['rpool_healthy'] == 'Not Healthy':
    pools += ' class="warning"'
pools += '><span>rpool</span><span>%(rpool_healthy)s</span></div><div id="tank_status"'
if stats['tank_healthy'] == 'Not Healthy':
    pools += ' class="warning"'
pools += '><span>tank</span><span>%(tank_healthy)s</span></div></div>'

backups = '''
<div id="last_backups">
    <h3>Last Backups</h3>
    <div id="imac"'''
warning_cutoff = datetime.timedelta(days=1) # warn if backups are more that this age
if stats['imac_last_backup'] is None or stats['imac_last_backup_age'] > warning_cutoff:
    backups += ' class="warning"'
backups += '><span>imac</span><span>%(imac_last_backup)s</span></div><div id="work_laptop"'
if stats['work_last_backup'] is None or stats['work_last_backup_age'] > warning_cutoff:
    backups += ' class="warning"'
backups += '><span>work laptop</span><span>%(work_last_backup)s</span></div><div id="karen_laptop"'
if stats['karen_last_backup'] is None or stats['karen_last_backup_age'] > warning_cutoff:
    backups += ' class="warning"'
backups += '><span>karen&apos;s laptop</span><span>%(karen_last_backup)s</span></div></div>'

server_stats = '''
<div id="server_stats"><h2>File Server Stats</h2>%s%s%s%s</div>
''' % (disk_stats, uptime, pools, backups)

server_stats = server_stats % stats

website_stats = '<div id="website_stats"><h2>Website Stats</h2></div>'

content = server_stats + website_stats

print template % (content, stats['current_time'])