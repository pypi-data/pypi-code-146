#!/usr/bin/env python

"""The setup script."""
import fnmatch
import os
from distutils.command.clean import clean as _clean
from glob import glob
from os.path import basename, exists, splitext
from shutil import rmtree

from setuptools import find_packages, setup

try:
    from sphinx.setup_command import BuildDoc

    CMDCLASS = {"build_sphinx": BuildDoc}
except ImportError:
    # sphinx not installed - do not provide build_sphinx cmd
    CMDCLASS = {}


class CleanUp(_clean, object):
    """
    Custom implementation of ``clean`` distutils/setuptools command.
    Overriding clean in order to get rid if "dist" folder and etc
    """

    CLEANFOLDERS = (
        "TMP",
        "__pycache__",
        "pip-wheel-metadata",
        ".eggs",
        "dist",
        "sdist",
        "wheel",
        ".pytest_cache",
        "docs/apiref",
        "docs/_build",
        "htmlcov",
    )

    CLEANFOLDERSRECURSIVE = ["__pycache__", "_tmp_*", "*.egg-info"]
    CLEANFILESRECURSIVE = ["*.pyc", "*.pyo", ".coverage", "coverage.xml"]

    @staticmethod
    def ffind(pattern, path):
        result = []
        for root, _dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    @staticmethod
    def dfind(pattern, path):
        result = []
        for root, dirs, _files in os.walk(path):
            for name in dirs:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def run(self):
        """After calling the super class implementation, this function removes
        the directories/files specific above"""
        super(CleanUp, self).run()

        for dir_ in CleanUp.CLEANFOLDERS:
            if exists(dir_):
                print("Removing: {}".format(dir_))
            if not self.dry_run and exists(dir_):
                rmtree(dir_)

        for dir_ in CleanUp.CLEANFOLDERSRECURSIVE:
            for pdir in self.dfind(dir_, "."):
                print("Remove folder {}".format(pdir))
                rmtree(pdir)

        for fil_ in CleanUp.CLEANFILESRECURSIVE:
            for pfil in self.ffind(fil_, "."):
                print("Remove file {}".format(pfil))
                os.unlink(pfil)


def parse_requirements(filename):
    """Load requirements from a pip requirements file"""
    try:
        lineiter = (line.strip() for line in open(filename))
        return [line for line in lineiter if line and not line.startswith("#")]
    except IOError:
        return []


def src(fil):
    """Getting src path"""
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, fil))


with open("README.md", encoding="utf-8") as readme_file:
    README = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = parse_requirements("requirements.txt")

# for 'python setup.py test' to work; need pytest runner:
SETUP_REQUIREMENTS = [
    "pytest-runner",
    "setuptools_scm<7.0; python_version < '3.7'",
    "setuptools_scm; python_version >= '3.7'",
    "wheel",
]

TEST_REQUIREMENTS = ["pytest"]

# entry points setting
FMUCONFIG_RUNNER = "fmuconfig=" "fmu.config.fmuconfigrunner:main"

CMDCLASS.update({"clean": CleanUp})

setup(
    name="fmu_config",
    cmdclass={"clean": CleanUp},
    use_scm_version={"root": src(""), "write_to": src("src/fmu/config/_theversion.py")},
    description="Library for various config scripts in FMU scope",
    long_description=README + "\n\n" + HISTORY,
    author="Jan C. Rivenaes",
    author_email="jriv@equinor.com",
    url="https://github.com/equinor/fmu-config",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    entry_points={"console_scripts": [FMUCONFIG_RUNNER]},
    keywords="fmu, config",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
)
