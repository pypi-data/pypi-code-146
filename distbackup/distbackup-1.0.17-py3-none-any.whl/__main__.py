#!/usr/bin/python3
import sys
import os
import logging
from pathlib import Path

try:
    import argcomplete
except ImportError:
    argcomplete = None

from .errors import ArgumentError
from .logger import FormatDelegator, FilePatternLogger
from .cli import open_db, arg_parser
from .utils import Progress, ProgressBar

def init_arguments():
    root_parser = arg_parser.root_parser

    db_path = os.getenv('DISTBACKUP_PATH')
    if db_path is not None:
        default_db_path = Path(db_path)
    else:
        configdir = os.getenv('XDG_CONFIG_HOME')
        if configdir:
            configdir = Path(configdir)
        else:
            configdir = Path.home() / '.config'

        default_db_path = configdir / 'distbackup'

    root_parser.set_defaults(
        sync=False,
        nocopy=False,
        no_hashcopy=False,
    )

    root_parser.add_argument(
        '-d', '--db', type=Path, metavar='PATH',
        default=default_db_path,
        help='Location of primary database (default: %(default)s)')

    root_parser.add_argument(
        '-l', '--log', action='store',
        help='Write logs to a file. If the pattern contains "@@", it is replaced '
        'with the current date. (default: <dbpath>/log/log-@@.txt)'
    )

    root_parser.add_argument(
        '-L', '--nolog', action='store_true',
        help='Do not write to log file.'
    )

    root_parser.add_argument(
        '-v', '--verbose', action='count',
        default=0,
        help='Verbose logging'
    )

    root_parser.add_argument(
        '-e', '--explain', action='store_true',
        help='Explain queries as they are executed'
    )

    root_parser.add_argument(
        '-n', '--noaction', action='store_true',
        help='Do not actually perform any actions'
    )

    if argcomplete:
        argcomplete.autocomplete(root_parser, validator=lambda current_input, keyword_to_check_against: True)

    return root_parser


def main():
    parser = init_arguments()
    args = parser.parse_args()

    Progress.set_global(ProgressBar())

    if args.no_hashcopy:
        from .sourcefile import SourceFile
        SourceFile.ENABLE_HASHCOPY = False


    root = logging.getLogger()
    root.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    console_formatter = FormatDelegator('%(levelname)s: %(message)s')
    console_formatter.set_level_format(logging.INFO, '%(message)s')

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)

    if args.nolog or args.log == '':
        logpath = None
    elif not args.log:
        dbpath = args.db
        if dbpath.is_dir():
            dbdir = dbpath
        else:
            dbdir = dbpath.parent
        logpath = dbdir / 'log' / 'log-@@.txt'
    else:
        logpath = args.log

    if logpath:
        logfile_handler = FilePatternLogger(logpath)
        logfile_handler.setFormatter(log_formatter)
        root.addHandler(logfile_handler)

    log = logging.getLogger('main')

    if args.verbose:
        log.info(f'distbackup starting: {sys.argv[1:]!r}')

    db = open_db(args)

    cmd = arg_parser.get_command_for_args(args)
    try:
        cmd.func(db, cmd.parser, args)
    except ArgumentError as e:
        log.error(str(e))
        return
    except KeyboardInterrupt:
        log.info('Interrupted')
    except Exception:
        log.exception(f'Exception running {" ".join(args.command_name)}')

if __name__ == '__main__':
    main()
