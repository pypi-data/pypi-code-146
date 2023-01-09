from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Pyspark Dataframe Analyzer - Smartest DataFrame Analysis'
LONG_DESCRIPTION = 'A package that allows pyspark community to analyze thier datafrane before making any kind of business, technical or logical decisions.'

# Setting up
setup(
    name="dfanalyzer",
    version=VERSION,
    author="Neetish Singh(AAYS Anaytics)",
    author_email="<neetishsingh97@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'pyspark','spark','ingestion','data','dataframe','analysis','schema','pandas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)