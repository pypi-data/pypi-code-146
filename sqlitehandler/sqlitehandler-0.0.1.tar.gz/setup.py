from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'SQLite handler package'
LONG_DESCRIPTION = 'Package to quickly use SQLite, without having to know sql, with basic functionality.'

# Setting up
setup(
    name="sqlitehandler",
    version=VERSION,
    author="kaki8b (Daniel F.C. F.)",
    author_email="<mail@kaki8b.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['sqlite', 'sys', 'itertools', 'os'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)