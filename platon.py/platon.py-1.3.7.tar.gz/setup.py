#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)

extras_require = {
    'tester': [
        "platon-tester[py-evm]>=1.2.0",
        # "py-node>=3.2.0,<4",
    ],
    'linter': [
        "flake8==3.8.3",
        "isort>=4.2.15,<4.3.5",
        "mypy==0.812",
    ],
    'docs': [
        "mock",
        "sphinx-better-theme>=0.1.4",
        "click>=5.1",
        "configparser==3.5.0",
        "contextlib2>=0.5.4",
        "py-node>=3.2.0,<4",
        "py-solc>=0.4.0",
        "pytest>=4.4.0,<5.0.0",
        "sphinx>=3.0,<4",
        "sphinx_rtd_theme>=0.1.9",
        "toposort>=1.4",
        "towncrier>=19.2.0,<20",
        "urllib3",
        "wheel"
    ],
    'dev': [
        "bumpversion",
        "flaky>=3.7.0,<4",
        "hypothesis>=3.31.2,<6",
        "pytest>=4.4.0,<5.0.0",
        "pytest-asyncio>=0.10.0,<0.11",
        "pytest-mock>=1.10,<2",
        "pytest-pythonpath>=0.3",
        "pytest-watch>=4.2,<5",
        "pytest-xdist>=1.29,<2",
        "setuptools>=38.6.0",
        "tox>=1.8.0",
        "tqdm>4.32,<5",
        "twine>=1.13,<2",
        "when-changed>=0.3.0,<0.4"
    ]
}

extras_require['dev'] = (
    extras_require['tester']
    + extras_require['linter']
    + extras_require['docs']
    + extras_require['dev']
)

with open('./README.md') as readme:
    long_description = readme.read()

setup(
    name='platon.py',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='1.3.7',
    description="""platon.py""",
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Shinnng',
    author_email='shinnng@outlook.com',
    url='https://github.com/platonnetwork/platon.py',
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.7.4.post0,<4",
        "platon-abi>=1.2.0",
        "platon-account>=1.2.0",
        "platon-hash[pycryptodome]>=1.2.0",
        "platon-typing>=1.2.0",
        "platon-utils>=1.2.0",
        "hexbytes>=0.1.0,<1.0.0",
        "ipfshttpclient==0.7.0",
        "jsonschema>=3.2.0,<4.0.0",
        "lru-dict>=1.1.6,<2.0.0",
        "protobuf>=3.10.0,<4",
        "pywin32>=223;platform_system=='Windows'",
        "requests>=2.16.0,<3.0.0",
        # remove typing_extensions after python_requires>=3.8, see platon._utils.compat
        "typing-extensions>=3.7.4.1,<4;python_version<'3.8'",
        "websockets>=9.1,<10",
    ],
    python_requires='>=3.6,<4',
    extras_require=extras_require,
    py_modules=['web3', 'ens', 'platonpm'],
    entry_points={"pytest11": ["pytest_platon = platon.tools.pytest_platon.plugins"]},
    license="MIT",
    zip_safe=False,
    keywords='platon',
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"platon": ["py.typed"]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
