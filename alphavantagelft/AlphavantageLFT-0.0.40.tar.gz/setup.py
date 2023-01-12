from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.40'
DESCRIPTION = 'An Alphavantage API wrapper that was initially built as a subcomponent for the Laurier Fintech Discord Bot.'

setup(
    name="AlphavantageLFT",
    version=VERSION,
    author="Laurier Financial Technology",
    author_email="<team@wlufintech.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'Alphavantage', 'Laurier', 'Laurier Fintech', 'Stock Market', 'Crypto'],
)