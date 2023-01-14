import argparse
import os
import sys

##
## Process arguments

parser = argparse.ArgumentParser()
parser.add_argument(
    'path',
    type=str,
    help='Path containing files to prefix'
)
parser.add_argument(
    'prefix',
    type=str,
    help='Prefix to add to filenames'
)

args = parser.parse_args()
target_path = args.path
prefix = args.prefix


##
## Validate path existence
if not os.path.exists(target_path) or not os.path.isdir(target_path):
    print('Provied path seems to be invalid: {}'.format(target_path))
    sys.exit('Verify that provided path is a valid directory')


##
## Get files
target_files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
for file in target_files:
    new_name = prefix + ' - ' + file.capitalize()
    os.rename(
        os.path.join(target_path, file),
        os.path.join(target_path, new_name)
    )
    
    print('"{}" renamed to "{}"'.format(file, new_name))
