#!/usr/bin/env python3


from setuptools import (find_packages, setup)


with open(".github/README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "watch_path",
    version = "0.1.1",
    author = "S0AndS0",
    author_email = "StrangerThanBland@gmail.com",
    description = "Simple wrapper for `os.stat`, calls callback function time-stamp changes",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/python-utilities/watch_path",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'watch_path = watch_path.cli:main'
        ],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
    ],
)
