#!/usr/bin/env python3


from argparse import ArgumentParser
from os.path import basename
from subprocess import (Popen, PIPE)
from sys import argv
from time import sleep


from watch_path import Watch_Path


__license__ = """
Inject JavaScript within PDF document body
Copyright (C) 2023 S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def subprocess_callback(**kwargs):
    """
    """
    if kwargs.get('verbose') > 0:
        print("commands -> {}".format(kwargs['commands']))

    process = Popen(kwargs['commands'], stdout = PIPE, stderr = PIPE, shell = True)
    stdout, stderr = process.communicate()
    if stderr:
        if kwargs.get('decode'):
            raise Exception(stderr.decode(kwargs['decode']))

        raise Exception(stderr)

    if stdout:
        return {"stdout": stdout, "returncode": process.returncode}

    return {"returncode": process.returncode}


arg_parser = ArgumentParser(
    prog = basename(argv[0]),
    usage = '%(prog)s --file "file.txt" --command "cat file.txt"',
    epilog = 'For more projects see: https://github.com/S0AndS0')

arg_parser.add_argument('--path', '--file', '--file-path',
                        help = 'File or directory path to watch for modify time changes',
                        required = True)

arg_parser.add_argument('--commands', '--command',
                        help = 'Command to run when file changes are detected',
                        required = True)

arg_parser.add_argument('--sleep',
                        help = 'Seconds to sleep between checking modify time of `--file`',
                        required = False,
                        default = 1.0,
                        type = float)

arg_parser.add_argument('--decode',
                        help = 'Type of decoding to preform on stdout, eg. "utf-8"',
                        required = False,
                        type = str)

arg_parser.add_argument('--verbose', '-v',
                        help = 'Loudness of this script',
                        action = 'count',
                        default = 0)


args = vars(arg_parser.parse_args())
args.update(callback = subprocess_callback)

path_watcher = Watch_Path(**args)

decode = args.get('decode')


def main():
    try:
        for callback_results in path_watcher:
            if callback_results:
                if args.get('verbose') > 0:
                    print("callback_results['returncode'] ->", callback_results['returncode'])
                    print("callback_results['stdout']...")

                if decode:
                    print(callback_results['stdout'].decode(decode))
                else:
                    print(callback_results['stdout'])

            sleep(args.get('sleep', 1.0))

    except KeyboardInterrupt:
        print('Stopping watcher and exiting...')
