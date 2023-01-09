# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='panther_sdk',
    url="https://panther.com",
    author="Panther Labs Inc.",
    author_email="support@panther.io",
    version='0.0.21',
    packages=find_packages(),
    package_data={"panther_sdk": ["py.typed"]},
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='security detection',
    install_requires=[
        'panther_core>=0.3.3,<0.4.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Typing :: Typed',
        'Programming Language :: Python :: 3',
    ]
)
