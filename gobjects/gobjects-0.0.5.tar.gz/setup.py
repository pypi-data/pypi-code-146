# File Name: setup.py
# Created By: ZW
# Created On: 2022-11-02
# Puropse: defines package information and
# requirements for the gobjects package

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gobjects",
    version="0.0.5",
    author="Zach Weber",
    author_email="zach.weber.813@gmail.com",
    description="Python3 genetics objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zwebbs/gobjects",
    project_urls={
        "Bug Tracker": "https://github.com/zwebbs/gobjects/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        'Operating System :: POSIX',
        'Operating System :: MacOS',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        'dev': ['build==0.9.0', 'twine==4.0.1']
    }
)
