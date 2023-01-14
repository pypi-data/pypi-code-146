import argparse
import os
import sys

##
## Process arguments

parser = argparse.ArgumentParser()
parser.add_argument(
    'path',
    type=str,
    help='Path containing files to rename'
)
parser.add_argument(
    'name',
    type=str,
    help='Name to apply to files (Increment will be appended at end)'
)

args = parser.parse_args()
target_path = args.path
name = args.name


##
## Validate path existence
if not os.path.exists(target_path) or not os.path.isdir(target_path):
    print('Provied path seems to be invalid: {}'.format(target_path))
    sys.exit('Verify that provided path is a valid directory')


##
## Get and rename files

target_files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]

increment = 0
for file in target_files:
    increment += 1
    new_name = name + ' ' + str(increment) + '.png'
    os.rename(
        os.path.join(target_path, file),
        os.path.join(target_path, new_name)
    )
    
    print('"{}" renamed to "{}"'.format(file, new_name))
