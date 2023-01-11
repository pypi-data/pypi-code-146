from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup (
    name = 'awsctx',
    description = 'A command line tool to change active AWS profiles and add/replace profiles.',
    version = '1.0.1',
    packages = find_packages(), # list of all packages
    python_requires='>=3.6', # any python greater than 3.6
    entry_points='''
        [console_scripts]
        awsctx=awsctx.__main__:main
    ''',
    author="Aniket Paul",
    keyword="aws, context switch, aws profiles, aws profile switch, profile switch, cli, aws cli switch",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/aurphillus/awsctx',
    author_email='aniketpaul446@gmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
