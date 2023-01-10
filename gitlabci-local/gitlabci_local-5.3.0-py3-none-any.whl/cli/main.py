#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, _MutuallyExclusiveGroup, ArgumentParser, Namespace,
                      RawTextHelpFormatter, SUPPRESS)
from os import environ
from pathlib import Path
from subprocess import check_output, DEVNULL, Popen
from sys import argv, exit as sys_exit
from typing import Optional

# Components
from ..engines.engine import supported as engine_supported
from ..features.configurations import ConfigurationsFeature
from ..features.images import ImagesFeature
from ..features.menus import MenusFeature
from ..features.pipelines import PipelinesFeature
from ..package.bundle import Bundle
from ..package.settings import Settings
from ..package.updates import Updates
from ..package.version import Version
from ..parsers.gitlab import GitLab
from ..parsers.parsers import Parsers
from ..prints.colors import Colors
from ..system.platform import Platform

# Main, pylint: disable=too-many-branches,too-many-locals,too-many-statements
def main() -> None:

    # Variables
    group: _ArgumentGroup
    hint: str = ''
    interactive: bool = Platform.IS_TTY_STDIN and Platform.IS_TTY_STDOUT
    result: bool = False
    subgroup: _MutuallyExclusiveGroup

    # Arguments creation
    parser: ArgumentParser = ArgumentParser(
        prog=Bundle.NAME, description=
        f'{Bundle.NAME}: Launch {Bundle.CONFIGURATION} jobs locally (aliases: {Bundle.ALIAS})',
        add_help=False, formatter_class=RawTextHelpFormatter)

    # Arguments internal definitions
    group = parser.add_argument_group('internal arguments')
    group.add_argument('-h', '--help', dest='help', action='store_true',
                       help='Show this help message')
    group.add_argument('--version', dest='version', action='store_true',
                       help='Show the current version')
    group.add_argument('--update-check', dest='update_check', action='store_true',
                       help='Check for newer package updates')
    group.add_argument('--settings', dest='settings', action='store_true',
                       help='Show the current settings path and contents')

    # Arguments pipeline definitions
    group = parser.add_argument_group('pipeline arguments')
    group.add_argument('-p', '--pipeline', dest='pipeline', action='store_true',
                       help='Automatically run pipeline stages rather than jobs')
    group.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                       help='Hide jobs execution context')
    group.add_argument(
        '-c', dest='configuration', action='store', default=Bundle.CONFIGURATION,
        help=f'Path to the {Bundle.CONFIGURATION} configuration file or folder')
    group.add_argument('-B', '--no-before', dest='before', action='store_false',
                       help='Disable before_script executions')
    group.add_argument('-A', '--no-after', dest='after', action='store_false',
                       help='Disable after_script executions')
    group.add_argument(
        '-n', dest='network', action='store', help=
        f'Configure the network mode used (or define {Bundle.ENV_NETWORK})\n' \
            f"Choices: {', '.join(Bundle.ARGUMENT_NETWORKS_ENUM)}. " \
            f'Default: {Bundle.ARGUMENT_NETWORKS_ENUM[0]}'
    )
    group.add_argument('-e', dest='env', action='append',
                       help='Define VARIABLE=value, pass VARIABLE or ENV file')
    group.add_argument(
        '-E', dest='engine', action='store', help=
        f'Force a specific engine (or define {Bundle.ENV_ENGINE})\n' \
            f"Default list: {','.join(engine_supported())}"
    )
    group.add_argument('-H', '--host', dest='host', action='store_true',
                       help='Run all jobs on the host rather than containers')
    group.add_argument('--notify', dest='notify', action='store_true',
                       help='Enable host notifications of pipeline and jobs results')
    group.add_argument(
        '-r', '--real-paths', dest='real_paths', action='store_true',
        help='Mount real folder paths in the container (Linux / macOS only)')
    group.add_argument(
        '-S', '--sockets', dest='sockets', action='store_true',
        help='Mount engine sockets for nested containers\n'
        '(Enabled by default with services: docker:*dind)')
    group.add_argument('--ssh', dest='ssh', action='store', metavar='SSH_USER', nargs='?',
                       const=Bundle.ARGUMENT_SSH_USER_DEFAULT,
                       help='Bind SSH credentials to a container\'s user')
    group.add_argument('-v', dest='volume', action='append',
                       help='Mount VOLUME or HOST:TARGET in containers')
    group.add_argument('-w', dest='workdir', action='store',
                       help='Override the container\'s working path')

    # Arguments debugging definitions
    group = parser.add_argument_group('debugging arguments')
    subgroup = group.add_mutually_exclusive_group()
    subgroup.add_argument('--bash', dest='bash', action='store_true',
                          help='Prepare runners for manual bash purposes')
    subgroup.add_argument('--debug', dest='debug', action='store_true',
                          help='Keep runners active for debugging purposes')
    group.add_argument('--display', dest='display', action='store_true',
                       help='Enable host DISPLAY forwarding features')
    group.add_argument('--shell', dest='shell', action='store',
                       help='Configure the default bash/debug shell entrypoint')

    # Arguments jobs definitions
    group = parser.add_argument_group('jobs arguments')
    group.add_argument('--all', dest='all', action='store_true',
                       help='Enable all jobs by default in selections')
    group.add_argument(
        '--defaults', dest='defaults', action='store_true',
        help=f'Use default variables for {GitLab.LOCAL_NODE}:configurations')
    group.add_argument('-f', '--force', dest='force', action='store_true',
                       help='Force the action (use with --pull)')
    group.add_argument('-i', '--ignore-case', dest='ignore_case', action='store_true',
                       help='Ignore case when searching for names')
    group.add_argument('-m', '--manual', dest='manual', action='store_true',
                       help='Allow manual jobs to be used')
    group.add_argument(
        '--no-git-safeties', dest='no_git_safeties', action='store_true',
        help='Disable automated Git safeties configuration\n'
        f'(or define {Bundle.ENV_NO_GIT_SAFETIES})')
    group.add_argument(
        '--no-script-fail', dest='no_script_fail', action='store_true',
        help='Fail on missing \'script\' nodes of jobs\n'
        f'(or define {Bundle.ENV_NO_SCRIPT_FAIL})')
    group.add_argument('-R', '--no-regex', dest='no_regex', action='store_true',
                       help='Disable regex search of names')
    group.add_argument('--scripts', dest='scripts', action='store_true',
                       help='Dump parsed jobs entrypoint scripts')
    group.add_argument(
        '-t', dest='tags', action='store', help=
        f"Handle listed tags as manual jobs\nDefault list: {','.join(Bundle.ARGUMENT_TAGS_DEFAULT)}"
    )

    # Arguments features definitions
    group = parser.add_argument_group('features arguments')
    subgroup = group.add_mutually_exclusive_group()
    subgroup.add_argument('-d', '--dump', dest='dump', action='store_true',
                          help=f'Dump parsed {Bundle.CONFIGURATION} configuration')
    subgroup.add_argument('-s', '--select', dest='select', action='store_true',
                          help='Force jobs selection from enumerated names')
    subgroup.add_argument('-l', '--list', dest='list', action='store_true',
                          help='Select one job to run (implies --manual)')
    subgroup.add_argument('--pull', dest='pull', action='store_true',
                          help='Pull container images from all jobs')
    subgroup.add_argument('--rmi', dest='rmi', action='store_true',
                          help='Delete container images from all jobs')

    # Arguments hidden definitions
    group = parser.add_argument_group('hidden arguments')
    group.add_argument('--engine-default', dest='engine_default', action='store_true',
                       help=SUPPRESS)
    group.add_argument('--image', dest='image', action='store', help=SUPPRESS)
    group.add_argument('--tags-default', dest='tags_default', action='store_true',
                       help=SUPPRESS)

    # Arguments positional definitions
    group = parser.add_argument_group('positional arguments')
    group.add_argument(
        'names', nargs='*', help='Names of specific jobs (or stages with --pipeline)\n'
        'Regex names is supported unless --no-regex is used')

    # Arguments parser
    options: Namespace = parser.parse_args()

    # Help informations
    if options.help:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        sys_exit(0)

    # Instantiate settings
    settings: Settings = Settings(name=Bundle.NAME)

    # Settings informations
    if options.settings:
        settings.show()
        sys_exit(0)

    # Instantiate updates
    updates: Updates = Updates(name=Bundle.NAME, settings=settings)

    # Version informations
    if options.version:
        print(
            f'{Bundle.NAME} {Version.get()} from {Version.path()} (python {Version.python()})'
        )
        Platform.flush()
        sys_exit(0)

    # Check for current updates
    if options.update_check:
        if not updates.check():
            updates.check(older=True)
        sys_exit(0)

    # Prepare configuration
    if Path(options.configuration).is_dir():
        options.configuration = Path(options.configuration) / Bundle.CONFIGURATION

    # Prepare engine
    if options.engine is None and Bundle.ENV_ENGINE in environ:
        options.engine = environ[Bundle.ENV_ENGINE]
        options.engine_default = True
    elif options.engine is not None:
        environ[Bundle.ENV_ENGINE] = options.engine
        options.engine_default = False
    else:
        options.engine = settings.get(group='engines', key='engine')
        options.engine_default = True
        if not options.engine:
            options.engine = ','.join(engine_supported())
            settings.set(group='engines', key='engine', value=options.engine)

    # Prepare no_git_safeties
    if not options.no_git_safeties and Bundle.ENV_NO_GIT_SAFETIES in environ:
        options.no_git_safeties = True

    # Prepare no_script_fail
    if not options.no_script_fail:
        if Bundle.ENV_NO_SCRIPT_FAIL in environ:
            options.no_script_fail = True
        else:
            no_script_fail = settings.get('parsers', 'no_script_fail')
            if no_script_fail is None:
                no_script_fail = 0
                settings.set('parsers', 'no_script_fail', no_script_fail)
            options.no_script_fail = int(no_script_fail) == 1

    # Prepare network
    if options.network is None and Bundle.ENV_NETWORK in environ:
        options.network = environ[Bundle.ENV_NETWORK]

    # Prepare paths
    options.configuration = Path(options.configuration).resolve()
    options.path = options.configuration.parent

    # Prepare tags
    if options.tags:
        options.tags = options.tags.split(',')
    else:
        options.tags = Bundle.ARGUMENT_TAGS_DEFAULT
        options.tags_default = True

    # Read configuration
    jobs = Parsers(options).read()
    if not jobs:
        sys_exit(1)

    # Header
    print(' ')
    Platform.flush()

    # Dump configuration
    if options.dump:
        result = ConfigurationsFeature(jobs=jobs, options=options).dump()

    # Pull jobs images
    elif options.pull:
        result = ImagesFeature(jobs=jobs, options=options).pull()

    # Remove jobs images
    elif options.rmi:
        result = ImagesFeature(jobs=jobs, options=options).rmi()

    # Select job
    elif options.list and interactive:
        options.manual = True
        options.no_regex = True
        result = MenusFeature(jobs=jobs, options=options).select()

    # Select jobs
    elif options.select and interactive:
        options.no_regex = True
        result = MenusFeature(jobs=jobs, options=options).select()

    # Launch pipeline
    elif options.pipeline:
        result = PipelinesFeature(jobs=jobs, options=options).launch()

    # Launch jobs
    elif options.names:
        result = PipelinesFeature(jobs=jobs, options=options).launch()

    # Select jobs
    elif interactive:
        options.no_regex = True
        result = MenusFeature(jobs=jobs, options=options).select()

    # Launch all jobs
    elif options.all:
        options.pipeline = True
        result = PipelinesFeature(jobs=jobs, options=options).launch()

    # Unsupported case
    else:

        # Windows WinPTY compatibility
        if Platform.IS_WINDOWS and Bundle.ENV_WINPTY not in environ:

            # Prepare WinPTY variables
            hint = ' (on Windows, winpty is required)'
            winpty: Optional[str] = None
            if Bundle.ENV_WINPTY_PATH in environ:
                winpty = environ[Bundle.ENV_WINPTY_PATH]

            # Acquire WinPTY path
            try:
                if not winpty:
                    winpty = str(
                        check_output(args=['where', 'winpty.exe'],
                                     stderr=DEVNULL).strip())
            except FileNotFoundError: # pragma: no cover
                pass
            else:

                # Nested WinPTY launch
                _environ = environ.copy()
                _environ[Bundle.ENV_WINPTY] = 'true'
                try:
                    with Popen(args=[winpty] + argv if winpty else argv,
                               env=_environ) as process:
                        process.wait()
                        sys_exit(process.returncode)
                except OSError: # pragma: no cover
                    pass

        # Unsupported interactive terminal
        print(
            f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR: ' \
                f'{Colors.BOLD}Unsupported non-interactive context{hint}...{Colors.RESET}'
        )
        print(' ')
        Platform.flush()

    # Check for daily updates
    if updates.enabled and updates.daily:
        updates.check()

    # Result
    if result:
        sys_exit(0)
    else:
        sys_exit(1)

# Entrypoint
if __name__ == '__main__': # pragma: no cover
    main()
