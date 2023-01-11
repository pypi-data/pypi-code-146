import argparse
import logging
import os

from inspector_commons.config import Config  # type: ignore
from inspector import __version__
from inspector.app import App, PYWEBVIEW_GUI

DESC = """\
Command-line entrypoint for Robocorp Inspector, which is
used to create and manage UI locators
"""


def get_args():
    parser = argparse.ArgumentParser(
        description=DESC, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d",
        "--database",
        metavar="PATH",
        help="path to locators database",
    )
    parser.add_argument(
        "-r",
        "--remote",
        help="remote server for browser management",
    )
    parser.add_argument(
        "-g",
        "--gui",
        choices=PYWEBVIEW_GUI,
        help="used GUI framework",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="be more talkative",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="print version and exit",
    )

    subparsers = parser.add_subparsers(
        title="actions",
        dest="action",
        description="run an action or subset of inspector directly",
        help="name of action",
    )

    add = subparsers.add_parser("open")
    add.add_argument(
        "type",
        choices=["browser", "web-recorder", "image", "windows"],
        help="create locator of given type",
    )

    edit = subparsers.add_parser("edit")
    edit.add_argument(
        "name",
        metavar="NAME",
        help="name of locator to edit",
    )

    return parser.parse_args()


def run():
    """Main entrypoint for CLI."""
    args = get_args()

    if args.version:
        print(__version__)
        return

    config = Config()
    config.set("database", args.database)
    config.set("remote", args.remote)
    config.set("gui", args.gui)
    config.set("debug", args.verbose > 0)

    home = config.get("home")
    os.makedirs(home, exist_ok=True)

    logger = logging.getLogger("pywebview")
    for handler in logger.handlers:
        logger.removeHandler(handler)

    log_level = logging.DEBUG if config.get("debug") else logging.INFO
    log_datefmt = "%Y/%m/%d %H:%M:%S"
    log_format = "%(asctime)s.%(msecs)03d › %(levelname)s › %(name)s › %(message)s"
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=log_datefmt,
        handlers=[
            logging.FileHandler(home / "inspector.log", "w"),
            logging.StreamHandler(),
        ],
    )

    if args.verbose < 2:
        logging.getLogger("PIL").setLevel(logging.INFO)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
        logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
            logging.INFO
        )

    try:
        # Prevent incompatible Qt plugins from affecting linux + conda
        os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
    except KeyError:
        pass

    app = App(config)
    try:
        if args.action == "open":
            app.open(args.type)
        elif args.action == "edit":
            app.edit(args.name)
        else:
            app.start("manager")
    except KeyboardInterrupt:
        print("User interrupt")
    except KeyError:
        print("Window not found")
    finally:
        app.stop()


if __name__ == "__main__":
    run()
