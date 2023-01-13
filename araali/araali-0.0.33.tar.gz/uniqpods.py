#!/usr/bin/env python

import sys

count_dict = {}
line_type = "unique"
for line in sys.stdin:
    line = line.strip()
    if "# unique" in line:
        continue
    if not line:
        line_type = "new"
        continue
    if line_type == "unique":
        count_dict[line] = 1
        continue
    if line_type == "new":
        line_type = line
        count_dict[line] = 0
    count_dict[line_type] += 1

keys = list(count_dict.keys())
keys.sort(key=lambda x: -count_dict[x])
for k in keys:
    print("%-70s %s" % (k, count_dict[k]))
    
