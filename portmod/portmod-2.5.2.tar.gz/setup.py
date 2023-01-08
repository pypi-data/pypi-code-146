#!/usr/bin/env python

# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3


import os
import subprocess
import sys

from setuptools import Command, find_packages, setup
from setuptools_rust import Binding, RustExtension, Strip

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as file:
    long_description = file.read()


def get_manpages():
    pages = []
    path = "doc/_build/man"
    if os.path.exists(path):
        for directory in os.listdir(path):
            pages.append(
                (
                    os.path.join("share/man", directory),
                    [
                        os.path.join(path, directory, file)
                        for file in os.listdir(os.path.join(path, directory))
                    ],
                )
            )

    return pages


class BuildMan(Command):
    """Command to generate man pages"""

    description = "build man pages"
    user_options = []  # type: ignore

    def initialize_options(self):
        ...

    def finalize_options(self):
        ...

    def run(self):
        if sys.platform != "win32":
            # Don't build docs if sphinx isn't available
            try:
                import sphinx  # noqa
                import sphinxarg  # noqa

                subprocess.check_call(["make", "-C", "doc", "man"])
            except ImportError:
                pass


setup(
    name="portmod",
    author="Portmod Authors",
    author_email="incoming+portmod-portmod-9660349-issue-@incoming.gitlab.com",
    description="A CLI package manager for mods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://gitlab.com/portmod/portmod",
    download_url="https://gitlab.com/portmod/portmod/-/releases",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    rust_extensions=[
        RustExtension("portmodlib.portmod", binding=Binding.PyO3, strip=Strip.Debug)
    ],
    zip_safe=False,
    entry_points=(
        {
            "console_scripts": [
                "inquisitor = portmod._cli.inquisitor:main",
                "portmod= portmod._cli.main:main",
            ]
        }
    ),
    cmdclass={"build_man": BuildMan},
    data_files=get_manpages(),
    python_requires=">=3.7",
    install_requires=[
        "colorama",
        "GitPython",
        "progressbar2>=3.2",
        'pywin32; platform_system == "Windows"',
        "RestrictedPython>=4.0",
        "redbaron",
        'python-sat; platform_system != "Windows"',
        'python-sat>=0.1.5.dev12; platform_system == "Windows"',
        "requests",
        'importlib_metadata; python_version < "3.8"',
        "packaging",
        "fasteners>=0.16",
        # Deprecated. Only needed by Pybuild1
        "chardet",
        "patool",
    ],
    setup_requires=["setuptools_scm", 'wheel; platform_system == "Windows"'],
    use_scm_version={"write_to": "portmod/_version.py"},
    extras_require={
        "dev": ["black", "flake8", "pylint", "isort", "mypy"],
        "test": ["pytest", "pytest-cov", "setuptools_scm"],
        "benchmark": ["pytest-benchmark"],
        # Bash completion support
        "bash": ["argcomplete"],
        # For building manpages
        "man": ["sphinx", "sphinx-argparse"],
        # For building html documentation
        "doc": [
            "sphinx",
            "sphinx-argparse",
            "sphinx-autodoc-typehints",
            "sphinx_rtd_theme",
            "sphinxcontrib-apidoc",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Software Distribution",
    ],
)
