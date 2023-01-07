#!/usr/bin/env python3
import subprocess
import os.path
import difflib

SOURCE_FILE_STR = "./translate/source_en.ts"

with open(SOURCE_FILE_STR) as old_source_file:
    old_contents_str = old_source_file.read()

python_files_list = []

for root, dirs, files in os.walk("."):
    for file_name in files:
        if file_name.endswith(".py"):
            python_files_list.append(os.path.join(root, file_name))

command_list = ["pylupdate5"] + python_files_list + ["-ts", SOURCE_FILE_STR]
# -please note that "-ts" has to be separate from the file that comes after, otherwise subprocess.run won't work

subprocess.run(command_list)

with open(SOURCE_FILE_STR) as new_source_file:
    new_contents_str = new_source_file.read()

# TBD: Add a diff with the old file contents
"""
for line_str in difflib.unified_diff(old_contents_str, new_contents_str, lineterm=''):
    print(line_str)
"""
