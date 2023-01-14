##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

"""
optumi-core setup
"""
import json
from pathlib import Path

import setuptools

# Get the version
exec(open("optumi_core/_version.py").read())

HERE = Path(__file__).parent.resolve()
long_description = (HERE / "README.md").read_text()

setup_args = dict(
    name="optumi-core",
    version=__version__,
    url="https://optumi.com",
    author="Optumi Inc Authors",
    author_email="cs@optumi.com",
    description="Optumi core library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=["requests-toolbelt"],
    platforms="Linux, Mac OS X, Windows",
    keywords=["Optumi"],
    classifiers=[
        "License :: Other/Proprietary License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
