from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'SQLite handler package'
#LONG_DESCRIPTION = 'Package to quickly use SQLite, without having to know sql, with basic functionality.'
with open("README.md", "r", encoding = "utf-8") as fh:
    LONG_DESCRIPTION = fh.read()
    
# Setting up
setup(
    name = "sqlitehandler",
    version = "0.0.2",
    author = "daniel F.C.F. ",
    #author_email = "author@example.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Danelfcf/SQLiteHandler/tree/main",
    project_urls = {
        "Bug Tracker": "https://github.com/Danelfcf/SQLiteHandler/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["sqlitehandler"]
)