#! /usr/bin/env python
#
# Copyright (c) 2022 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.


import copy
import logging
import os.path
import sys

from .parser import Parser
from . import generators

log = logging.getLogger("main")


class Config(object):
    def __init__(self, args):
        self.cmdline_args = ' '.join(
                [os.path.basename(sys.argv[0])] + sys.argv[1:])
        self.files = args.files
        self.directory = args.directory
        self.name = args.name
        self.input_directory = None
        self.format = args.format
        self.args = args


def process_obj(filepath, config):
    log.debug(f'processing {filepath}')
    if not config.name:
        config.name = os.path.splitext(os.path.basename(filepath))[0]
    config.input_directory = os.path.dirname(os.path.abspath(filepath))
    with open(filepath, "r") as f:
        parser = Parser(config)
        parser.load(f)
        generator = generators.get_by_name(config.format, config)
        generator.generate(parser)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', action='store',
                        help="Path for output files")
    parser.add_argument(
        '-n', '--name', action='store',
        help="""Name of the generated object. By default, use basename of
        the input file""")
    gens = generators.all_generators()
    parser.add_argument(
        '-f', '--format', action='store',
        choices=[x.name for x in gens],
        help="""Output format""")
    parser.add_argument(
        '--debug', action='store_true',
        help="""Print debug output""")

    for g in gens:
        g.add_options(parser)

    parser.add_argument(
        'files', action='append',
        help="""The Wavefront .obj files to transform.""")
    args = parser.parse_args()

    debug_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=debug_level)

    config = Config(args)
    for input_file in config.files:
        process_obj(input_file, copy.copy(config))


if __name__ == "__main__":
    sys.exit(main())
