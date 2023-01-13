"""Ocient Database Python API
"""

import os
import pathlib
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py

here = pathlib.Path(__file__).parent.absolute()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

version = {}
if os.path.exists(os.path.join(here, "version.py")):
    with open(os.path.join(here, "version.py")) as version_file:
        exec(version_file.read(), version)
        version = version["__version__"]
else:
    version = "1.0.0"

setup(
    name="pyocient",
    version=version,
    description="Ocient Database Python API",
    author="Ocient Inc",
    author_email="info@ocient.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ocient.com/",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="database, sql, development",
    setup_requires=[
        "wheel",
    ],
    install_requires=[
        "dsnparse",
        "prompt-toolkit",
        "pygments",
        "tabulate",
        "cryptography<=36.0",
        "cffi<=1.15.0",
        "google-auth<=2.6",  # because google-api-python-client doesn't provide an upper bound for this dep
        "protobuf<=3.19.1",  # because google-api-python-client doesn't provide an upper bound for this dep
        "google-api-python-client",
        "google-api-core<2.9",  # because google-api-core 2.9+ needs protobuf >=3.20.1
        "googleapis-common-protos<1.57.0",  # because greater requires protobuf!=3.20.0,!=3.20.1,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.19.5
    ],
    py_modules=["pyocient", "version", "ClientWireProtocol_pb2"],
    entry_points={
        "console_scripts": [
            "pyocient=pyocient:main",
        ],
    },
    python_requires=">=3.5, <4",
)
