"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import versioneer
from setuptools import setup

setup(version=versioneer.get_version(), cmdclass=versioneer.get_cmdclass())
