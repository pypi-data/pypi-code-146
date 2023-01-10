# File: setup.py
# Date: 9-Mar-2018
#
# Update:
#   3-Jul-2018  jdw update CLI entry points and dependencies
#  21-Aug-2018  jdw version adjustments
#  22-Aug-2018  jdw adjust for namespace packaging
#   3-Oct-2018  jdw add 'ruamel.yaml' dependency
#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = "rcsb.utils.config"

with open("rcsb/utils/config/__init__.py", "r", encoding="utf-8") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)


# Load packages from requirements*.txt
with open("requirements.txt", "r", encoding="utf-8") as ifh:
    packagesRequired = [ln.strip() for ln in ifh.readlines()]

with open("README.md", "r", encoding="utf-8") as ifh:
    longDescription = ifh.read()

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="RCSB Python Configuration Utilities",
    long_description_content_type="text/markdown",
    long_description=longDescription,
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="https://github.com/rcsb/py-rcsb_utils_config",
    #
    license="Apache 2.0",
    classifiers=(
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ),
    entry_points={},
    #
    install_requires=packagesRequired,
    packages=find_packages(exclude=["rcsb.utils.tests-config", "rcsb.utils.tests-*", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.cfg"]
    },
    #
    # These basic tests require no database services -
    test_suite="rcsb.utils.config.tests-config",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={"dev": ["check-manifest"], "test": ["coverage"]},
    # Added for
    command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    # This setting for namespace package support -
    zip_safe=False,
)
