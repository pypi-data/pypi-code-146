#!/usr/bin/env python

import setuptools
# Workaround for https://github.com/pypa/pip/issues/7953
import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

if __name__ == "__main__":
    setuptools.setup()
