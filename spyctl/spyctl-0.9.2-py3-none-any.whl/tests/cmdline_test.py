#! /home/brhaub/spyctl_demo/bin/python3

import os
import sys
from pathlib import Path

from click.testing import CliRunner

os.chdir(str(Path.cwd().parent.parent))

import spyctl.spyctl as spyctl


def main_test():
    runner = CliRunner()
    result = runner.invoke(spyctl.main, sys.argv[1:])
    print(result.output)


if __name__ == "__main__":
    main_test()
