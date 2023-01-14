
import argparse
import configparser
import json
import os
import sys
from hash import errors

from hash.core import main_action
from hash.store import get_store


def __read_config(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    sections = config.sections()
    if sections == []:
        sys.exit(9)
    return config


def build(args):
    configs = __read_config(args)
    try:
        config = dict(configs[args.storage])
    except KeyError:
        config = {}
    try:
        s = get_store(args.storage, config)
    except errors.StoreNotFound as e:
        print(f"Error in storage plugin {args.storage}, {e}")
        sys.exit(1)
    s.init(config)
    return main_action(args.path, "build", args.env, os.environ["PWD"], s)


def test(args):
    configs = __read_config(args)
    try:
        config = dict(configs[args.storage])
    except KeyError:
        config = {}
    try:
        s = get_store(args.storage, config)
    except errors.StoreNotFound as e:
        print(f"Error in storage plugin {args.storage}, {e}")
        sys.exit(1)
    s.init(config)
    return main_action(args.path, "test", args.env, os.environ["PWD"], s)


def publish(args):
    configs = __read_config(args)
    try:
        config = dict(configs[args.storage])
    except KeyError:
        config = {}
    try:
        s = get_store(args.storage, config)
    except errors.StoreNotFound as e:
        print(f"Error in storage plugin {args.storage}, {e}")
        sys.exit(1)
    s.init(config)
    return main_action(args.path, "publish", args.env, os.environ["PWD"], s)


def deploy(args):
    configs = __read_config(args)
    try:
        config = dict(configs[args.storage])
    except KeyError:
        config = {}
    try:
        s = get_store(args.storage, config)
    except errors.StoreNotFound as e:
        print(f"Error in storage plugin {args.storage}, {e}")
        sys.exit(1)
    s.init(config)
    return main_action(args.path, "deploy", args.env, os.environ["PWD"], s)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="hash", description="A tool to build resources based on their hash and type")
    sub_parsers = parser.add_subparsers(dest="subparser_name")
    parser.add_argument(
        "--storage", help="The storage system used default is Local File", default="LocalFile")
    parser.add_argument(
        "--config", help="The configuration file default is config.ini", default="config.ini")
    parser.add_argument(
        "--env", help="An environment to run the action in it", default=None)
    parser_build = sub_parsers.add_parser("build")
    parser_build.add_argument("path", help="path to build")
    parser_build.set_defaults(func=build)
    parser_test = sub_parsers.add_parser("test")
    parser_test.add_argument("path", help="path to test")
    parser_test.set_defaults(func=test)
    parser_publish = sub_parsers.add_parser("publish")
    parser_publish.add_argument("path", help="path to publish")
    parser_publish.set_defaults(func=publish)
    parser_deploy = sub_parsers.add_parser("deploy")
    parser_deploy.add_argument("path", help="path to deploy")
    parser_deploy.set_defaults(func=deploy)

    args = parser.parse_args(argv)
    if args.subparser_name is None:
        parser.print_help()
        sys.exit(1)
    try:
        return args.func(args)
    except errors.ResourceError as e:
        return f"Error: {e}"


if __name__ == "__main__":
    output = main(sys.argv[1:])
    if output:
        print(output)
