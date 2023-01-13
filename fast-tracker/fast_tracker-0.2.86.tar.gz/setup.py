#!/usr/local/bin python3
# -*- coding: utf-8 -*-

import os
import sys
import shlex
from subprocess import check_output
from setuptools import find_packages

python_version = sys.version_info[:2]

assert python_version in ((2, 7),) or python_version >= (
    3,
    5,
), "天眼Python探针只支持 Python 2.7 and 3.5+."

with_setuptools = False

try:
    from setuptools import setup

    with_setuptools = True
except ImportError:
    from distutils.core import setup

script_directory = os.path.dirname(__file__)
if not script_directory:
    script_directory = os.getcwd()

readme_file = os.path.join(script_directory, "README.rst")


def get_latest_git_hash():
    commit = check_output(shlex.split("git rev-parse --short HEAD")).strip()
    commit = commit.decode() if commit and isinstance(commit, bytes) else commit
    return commit


classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: System :: Monitoring",
]

kwargs = dict(
    name="fast_tracker",
    version="0.2.86",
    description=f"FAST Python Agent\n. latest git commit id: {get_latest_git_hash()}",
    long_description=open(readme_file).read(),
    url="http://doc.mypaas.com.cn/fast/03_%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8E%A2%E9%92%88%E9%9B%86%E6%88%90/%E7%AE%80%E4%BB%8B.html",
    author="FAST",
    author_email="duanyy03@mingyuanyun.com",
    maintainer="FAST",
    maintainer_email="duanyy03@mingyuanyun.com",
    license="Apache-2.0",
    # zip_safe=False,
    # classifiers=classifiers,
    # include_package_data=True,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "packaging",
        "gevent",
    ],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    package_data={
        "fast_tracker": ["FastTracker.json"],
    },
    license_files=("apache-skywalking-LICENSE",),
    scripts=["scripts/fast-boot"],
    extras_require={
        "test": [
            "testcontainers",
            "pyyaml",
            "pytest",
        ],
        "http": [
            "requests",
        ],
        "kafka": [
            "kafka",
        ],
    },
)

if with_setuptools:
    kwargs["entry_points"] = {
        "console_scripts": ["fast-boot = fast_tracker.admin:main"],
    }


def with_librt():
    try:
        if sys.platform.startswith("linux"):
            import ctypes.util

            return ctypes.util.find_library("rt")
    except Exception:
        pass


def run_setup():
    kwargs_tmp = dict(kwargs)

    setup(**kwargs_tmp)


run_setup()

print(75 * "*")

print("INFO: Pure Python agent was installed.")
