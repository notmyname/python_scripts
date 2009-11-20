#!/usr/bin/env python2.4

def count_bits(str):
    total = 0
    for c in str:
	num = ord(c)
	count = 0
	while num:
	    count += 1
	    num &= (num-1)
	total += count
    return total

def sum_bits(str):
    total = 0
    for c in str:
	total += ord(c)
    return total

def hash(str,max_disks):
    #return str((sum_bits(emp_id) % max_disks)+1)
    return str((count_bits(emp_id) % max_disks)+1)

import time
import sys
sys.path.insert(0,'/usr/local/WebApp/New/Context')
from BenefitSystem2.logic import BS2_logic

try:
    max_disks = int(sys.argv[1])
except:
    max_disks = 3

logic = BS2_logic.BS2_logic()

total_dist = 0.0
total_count = 0
for group_date in (x[0] for x in logic.getAvailableCaseList()):
    emp_id_list = logic.getEmployeeList(group_date)
    if not emp_id_list or len(emp_id_list) == 1:
	continue
    total_count += 1
    print group_date

    disk_totals = {}

    start = time.clock()
    for emp_id in emp_id_list:
	disk_num = hash(str,max_disks)
	if not disk_totals.has_key(disk_num):
	    disk_totals[disk_num] = 1
	else:
	    disk_totals[disk_num] += 1
    dur = time.clock()-start

    min = 100000
    max = -100000
    for d in sorted(disk_totals.iterkeys()):
	if disk_totals[d] > max:
	    max = disk_totals[d]
	if disk_totals[d] < min:
	    min = disk_totals[d]
	#print '%2s:\t%s' % (d,disk_totals[d])
    dist = max - min
    print 'max distribution: %s (min: %s, max: %s)' % (dist,min,max)
    per = (float(dist)/len(emp_id_list))*100
    total_dist += per
    print 'as a percentage of the total: %.4f%%' % per
    print '%.4f seconds to hash %s ids' % (dur,len(emp_id_list))
    print

print 'avg dist: %.4f%%' % (total_dist/total_count)
