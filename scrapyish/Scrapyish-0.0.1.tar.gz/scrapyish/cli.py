import sys
import argparse
from scrapyish.commands import crawl_command, build_project

def execute(args: dict=None) -> None:
    """Entry point and cli for the project."""
    if args is None:
        args = sys.argv[1:]
    if len(args) == 0:
        args = ["-h"]
    parser = argparse.ArgumentParser("scrapyish", prefix_chars="-")
    subparsers = parser.add_subparsers()
    crawl_parser = subparsers.add_parser("crawl")
    project_parser = subparsers.add_parser("startproject")
    crawl_parser.add_argument("spidername", help="name of the spider to run")
    crawl_parser.add_argument("-o", action="store", help="output file path")
    project_parser.add_argument(
        "project_name", help="name of project and directory to create")
    crawl_parser.set_defaults(func=crawl_command)
    project_parser.setdefaults(func=build_project)
    args = parser.parse_args()
    args.func()
