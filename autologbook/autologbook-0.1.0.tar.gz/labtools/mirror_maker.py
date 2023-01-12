# -*- coding: utf-8 -*-

#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#  and associated documentation files (the "Software"), to deal in the Software without restriction, including without
#  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Log file system event

@author: Antonio Bulgheroni
@email: antonio.bulgheroni@ec.europa.eu

"""
import logging
import sys
import time
from argparse import ArgumentParser
from pathlib import Path

from watchdog.observers import Observer

from autologbook import autoconfig
from autologbook.autowatchdog import MirrorEventHandler

program_name = 'mirror-maker'
program_version = 'v0.0.1'
autologbook_version = autoconfig.VERSION

log = logging.getLogger(__name__)


def argument_parser() -> ArgumentParser:
    """
    Return the argument parser object.
    """
    parser = ArgumentParser(description='Tool for mirroring two directories',
                            prog=program_name)

    # global parameters and options.
    parser.add_argument('-v', '--version', action='version',
                        version=(f'{program_name} is {program_version}. - '
                                 f'autologbook package is version {autologbook_version}.'),
                        help='Print the version number and exit.')
    parser.add_argument('-r', '--recursive', default=False, action='store_true',
                        help='Monitor all path subdirectories recursively.')

    parser.add_argument('-i', '--input-path', type=Path, help='The input path to be mirrored',
                        default=Path.cwd(), dest='original_path', metavar='PATH')
    parser.add_argument('-o', '--output-path', type=Path, dest='destination_path', metavar='PATH',
                        help='The destination path where the input has to be mirrored',
                        default=Path.cwd() / Path('../mirror_output'))

    return parser


def are_paths_ok(args) -> bool:
    paths = {'input path': args.original_path,
             'destination path': args.destination_path}

    for key, path in paths.items():
        if not path.exists():
            log.warning('The %s path was not existing. Automatically created.' % key)
            path.mkdir(parents=True)

        if not path.is_dir():
            log.error('Problem with the %s: it is not a directory' % key)
            return False

    return True


def main():
    cli_args = sys.argv[1:]
    parser = argument_parser()
    args = parser.parse_args(cli_args)

    log.setLevel(logging.INFO)
    fs = '[%(asctime)s]  %(levelname)-8s %(message)s'
    formatter = logging.Formatter(fs, datefmt='%Y%m%d-%H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

    file_handler = logging.FileHandler(filename='c:/temp/mirror_maker.log', mode='w')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    if not are_paths_ok(args):
        log.error('Unrecoverable error with the provided path information.')
        return

    event_handler = MirrorEventHandler(args.original_path, args.destination_path)
    event_handler.process_all_existing()
    observer = Observer()
    observer.schedule(event_handler, args.original_path, recursive=args.recursive)
    observer.start()
    log.info('Mirroring of directory %s into %s started' % (args.original_path, args.destination_path))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
