
import sys

from typing import List

from ..helper.tasks.address import AddressExtractor


def main(args: List[str] = None):
    if args is None:
        args = sys.argv[1:]

    if len(args) < 2:
        print("Usage: address <lang> <textfile>")
        sys.exit(1)

    extractor = AddressExtractor(args[0])

    with open(args[1], encoding='utf-8') as f:
        text = f.read()
    for r in extractor(text):
        print(r)


if __name__ == "__main__":
    main()
