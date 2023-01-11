"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import argparse
import os
import sys

from .sungai import DirectoryRater

__version__ = "0.1.0"


def run_sungai():
    """Run sungai."""
    parser = argparse.ArgumentParser(
        description="Sungai"
    )
    parser.add_argument(
        "target",
        type=str,
        help="The path to the target directory.",
    )
    parser.add_argument(
        "--min_score",
        type=float,
        help="The minimum score to pass.",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Add if you want verbose output.",
        required=False,
        default=False,
    )
    args = parser.parse_args()

    try:
        print(f"Sungai ({__version__})")
        target = os.path.normpath(args.target)
        if os.path.isdir(target):
            directory_rater = DirectoryRater(
                target,
            )
            sys.exit(directory_rater.run(args.verbose, args.min_score))
        else:
            print("[sungai] Error: Target not found")
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
