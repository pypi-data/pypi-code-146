import argparse

import frida_definitions_generator


def get_arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate TypeScript definition files for use with Frida")
    parser.add_argument(
        "--type", choices=["Java"], default="Java", help="The type of package to expect in the given paths"
    )
    parser.add_argument(
        "-E",
        "--exclude",
        metavar="PATH",
        dest="exclusions",
        action="append",
        default=[],
        help="Exclude the given package/class path from the generated definitions file",
    )
    parser.add_argument(
        "paths", metavar="FILE", nargs="+", help="a file or directory containing the program to generate from"
    )
    return parser


def main() -> None:
    args = get_arguments_parser().parse_args()
    frida_definitions_generator.generate(args)


if __name__ == "__main__":
    main()
