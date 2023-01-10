"""Check that django DEBUG = True in settings.py. Used by pre-commit."""

import argparse
import ast
import sys
from typing import List, Union


def main(argv: Union[List[str], None] = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to modify",
    )
    args = parser.parse_args(argv)
    offending_files = set()
    for file_name in args.filenames:
        if "settings.py" not in file_name:
            continue
        try:
            with open(file_name, encoding="utf8") as f:
                content = ast.parse(f.read(), filename=file_name)
            if not _check_ast(content):
                offending_files.add(file_name)
        except UnicodeDecodeError:
            pass
    if offending_files:
        print(
            f"Please change DEBUG to False in '{', '.join(offending_files)}',",
            file=sys.stderr,
        )
        sys.exit(-1)
    sys.exit(0)


def _check_ast(content: ast.Module) -> bool:
    for node in content.body:
        if not isinstance(node, ast.Assign):
            continue
        for name in node.targets:
            if name.id != "DEBUG" or not node.value.value:
                continue
            return False
    return True


if __name__ == "__main__":
    main()
