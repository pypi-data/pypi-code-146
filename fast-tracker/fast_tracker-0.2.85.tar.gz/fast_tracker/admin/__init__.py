#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
from __future__ import print_function

import sys
import logging

_builtin_plugins = [
    'run_program',
    'run_python',
]

_commands = {}


def command(name, options='', description='', hidden=False,
            log_intercept=True, deprecated=False):
    def wrapper(callback):
        callback.name = name
        callback.options = options
        callback.description = description
        callback.hidden = hidden
        callback.log_intercept = log_intercept
        callback.deprecated = deprecated
        _commands[name] = callback
        return callback

    return wrapper


def usage(name):
    details = _commands[name]
    if details.deprecated:
        print("[WARNING] This command is deprecated and will be removed")
    print('Usage: fast-boot %s %s' % (name, details.options))


@command('help', '[command]', hidden=True)
def help(args):
    if not args:
        print('Usage: fast-boot command [options]')
        print()
        print("Type 'fast-boot help <command>'", end='')
        print("for help on a specific command.")
        print()
        print("Available commands are:")

        commands = sorted(_commands.keys())
        for name in commands:
            details = _commands[name]
            if not details.hidden:
                print(' ', name)

    else:
        name = args[0]

        if name not in _commands:
            print("Unknown command '%s'." % name, end=' ')
            print("Type 'fast-boot help' for usage.")

        else:
            details = _commands[name]

            print('Usage: fast-boot %s %s' % (name, details.options))
            if details.description:
                print()
                description = details.description
                if details.deprecated:
                    description = '[DEPRECATED] ' + description
                print(description)


def setup_log_intercept():
    # setup logger handler

    class FilteredStreamHandler(logging.StreamHandler):
        def emit(self, record):
            if len(logging.root.handlers) != 0:
                return

            if record.name.startswith('packages'):
                return

            if record.levelno < logging.WARNING:
                return

            return logging.StreamHandler.emit(self, record)

    _stdout_logger = logging.getLogger('fast_tracker')
    _stdout_handler = FilteredStreamHandler(sys.stdout)
    _stdout_format = '%(levelname)s - %(message)s\n'
    _stdout_formatter = logging.Formatter(_stdout_format)
    _stdout_handler.setFormatter(_stdout_formatter)
    _stdout_logger.addHandler(_stdout_handler)


def load_internal_plugins():
    for name in _builtin_plugins:
        module_name = '%s.%s' % (__name__, name)
        __import__(module_name)


def load_external_plugins():
    try:
        import pkg_resources
    except ImportError:
        return

    group = 'admin'

    for entrypoint in pkg_resources.iter_entry_points(group=group):
        __import__(entrypoint.module_name)


def main():
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
        else:
            command = 'help'

        callback = _commands[command]  # run_program function

    except Exception:
        print("Unknown command '%s'." % command, end='')
        print("Type 'fast-boot help' for usage.")
        sys.exit(1)

    if callback.log_intercept:
        # 设置输入日志处理器
        setup_log_intercept()

    # 从第三个参数开始后续参数都传给callback，也就是run_program，eg：['fast-boot', 'run-program', 'hug', '-f', 'app.py']
    callback(sys.argv[2:])


load_internal_plugins()
load_external_plugins()

if __name__ == '__main__':
    main()
