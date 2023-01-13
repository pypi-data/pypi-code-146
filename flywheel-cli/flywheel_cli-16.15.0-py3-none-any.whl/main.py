"""Main Module of CLI"""
#!/usr/bin/env python3
import argparse
import logging
import os
import platform
import sys

import flywheel

from . import monkey, util
from .commands import add_commands
from .config import Config, ConfigError

log = logging.getLogger(__name__)


def main(args=None):
    """Main function"""
    # Handle fs weirdness
    monkey.patch_fs()

    # Disable terminal colors if NO_COLOR is set
    if os.environ.get("NO_COLOR"):
        import crayons  # pylint: disable=import-outside-toplevel

        crayons.disable()

    # Global exception handler for KeyboardInterrupt
    sys.excepthook = ctrlc_excepthook

    # Create base parser and subparsers
    parser = argparse.ArgumentParser(
        prog="fw", description="Flywheel command-line interface"
    )

    # Add commands from commands module
    add_commands(parser)

    # Parse arguments
    args = parser.parse_args(args)

    # Read duplicate option from config file. FLYW-10930
    Config.load_duplicates(args)

    # Additional configuration
    try:
        config_fn = getattr(args, "config", None)
        if callable(config_fn):
            config_fn(args)  # pylint: disable=not-callable
    except ConfigError as err:
        util.perror(err)
        sys.exit(1)

    log.debug(f"CLI Version: {util.get_cli_version()}")
    log.debug(f"CLI Args: {sys.argv}")
    log.debug(f"Platform: {platform.platform()}")
    log.debug(f"System Encoding: {sys.stdout.encoding}")
    log.debug(f"Python Version: {sys.version}")

    func = getattr(args, "func", None)
    if func is not None:
        # Invoke command
        try:

            rc = args.func(args)
            if rc is None:
                rc = 0
        except flywheel.ApiException as exc:
            log.debug("Uncaught ApiException", exc_info=True)
            if exc.status == 401:
                util.perror(f'You are not authorized: {exc.detail or "unknown reason"}')
                util.perror("Maybe you need to refresh your API key and login again?")
            else:
                util.perror(f"Request failed: {exc.detail or exc}")
            rc = 1
        except Exception as exc:  # pylint: disable=broad-except
            log.debug("Uncaught Exception", exc_info=True)
            util.perror(f"Error: {exc}")
            rc = 1
    else:
        parser.print_help()
        rc = 1

    sys.exit(rc)


def ctrlc_excepthook(exctype, value, traceback):
    """Exit CLI with Ctrl+C"""
    if exctype == KeyboardInterrupt:
        util.perror("\nUser cancelled execution (Ctrl+C)")
        logging.getLogger().setLevel(100)  # Supress any further log output
        os._exit(1)  # pylint: disable=protected-access
    else:
        sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    main()
