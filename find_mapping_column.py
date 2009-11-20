#!/usr/bin/env python2.4

import sys,csv

DELIMITER = ','

data_files = [open(f,'rb') for f in sys.argv[1:]]

all_lines_by_file = {}
common_columns = []
unique_key = None
file_count = 0
for file_obj in data_files:
    file_count += 1
    all_lines_by_file[file_count] = []
    reader = csv.DictReader(file_obj,delimiter=DELIMITER)
    for line in reader:
	all_lines_by_file[file_count].append(line)
	common_columns.extend(key for key in line.keys() if key not in common_columns)
        
all_lines = []
for file_count in all_lines_by_file:
    all_lines.extend(all_lines_by_file[file_count])
    for line in all_lines:
	for key in common_columns[:]:
	    if key not in line.keys():
		common_columns.pop(common_columns.index(key))
                
if len(common_columns) > 1 or True:
    commonality = dict.fromkeys(common_columns,0)
            
    unique_values = {}
    for file_num in all_lines_by_file:
	unique_values[file_num] = {}
	for col in common_columns:
	    unique_values[file_num][col] = []
	    for line in all_lines_by_file[file_num]:
		if line[col] and line[col] not in unique_values[file_num][col]:
		    unique_values[file_num][col].append(line[col])
                            
    for file_num in unique_values:
	for col in common_columns:
	    for val in unique_values[file_num][col]:
		found = True
		for file_num_2 in unique_values:
		    if file_num_2 == file_num: continue
		    if val not in unique_values[file_num_2][col]:
			found = False
			break
		if found:
		    commonality[col] += 1
                            
    biggest = 0
    for col in commonality:
	new_biggest = max(biggest,commonality[col])
	if new_biggest != biggest:
	    unique_key = col
	    biggest = new_biggest
elif common_columns:
    unique_key = common_columns[0]

print 'Mapping column:',unique_key
