#!/usr/bin/env python3
import setuptools


def scripts():
    import os

    scripts_list = os.listdir(os.curdir + "/scripts/")
    result = []
    for file in scripts_list:
        result = result + ["scripts/" + file]
    return result


setuptools.setup(
    name="qecore",
    version="3.15",
    author="Michal Odehnal",
    author_email="modehnal@redhat.com",
    license="GPLv3",
    url="https://gitlab.com/dogtail/qecore",
    description="DesktopQE Tool for unified test execution",
    packages=setuptools.find_packages(),
    scripts=scripts(),
    install_requires=[
        "behave",
        "behave-html-formatter",
        "behave-html-pretty-formatter",
        "dasbus",
        "termcolor",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.6",
    options={
        "build_scripts": {
            "executable": "/usr/bin/python3",
        }
    },
)
