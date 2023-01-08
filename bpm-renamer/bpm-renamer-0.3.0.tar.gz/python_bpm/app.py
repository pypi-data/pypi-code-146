from python_bpm.bpm_detection import get_bpm

import argparse
import glob
import os
import os.path
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description='Batch rename .wav files to include their BPM')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory',
                       help='Root directory containing .wav files to rename')
    group.add_argument('-f', '--file', help='Single .wav file to rename')

    parser.add_argument('--dry-run', help='Print renamings but don\'t execute them',
                        action='store_true', default=False)

    return parser.parse_args()


def get_all_files(args):
    if args.file is not None:
        return [os.path.realpath(args.file)]
    elif args.directory is not None:
        real_dir = os.path.realpath(args.directory)
        return list(map(os.path.realpath, glob.glob("**/*.wav",
                                                    root_dir=real_dir,
                                                    recursive=True)))
    else:
        raise "Bad options"


def bpm_filename(filename):
    if not os.path.isabs(filename):
        raise "Must be absolute"

    base = os.path.basename(filename)
    dirn = os.path.dirname(filename)
    bpm = get_bpm(filename)

    new_base = f"{bpm:.0f}BPM - {base}"
    new_full = os.path.join(dirn, new_base)

    return new_full


def do_rename(filename):
    os.rename(filename, bpm_filename(filename))


def do_dry_run(filename):
    print(f"mv '{filename}' '{bpm_filename(filename)}'")


def main():
    args = parse_args()
    inputs = get_all_files(args)

    action = do_dry_run if args.dry_run else do_rename

    for f in inputs:
        action(f)
