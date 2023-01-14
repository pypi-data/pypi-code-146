import codecs
import os
from pathlib import Path

from setuptools import setup

ECHAD_VERSION = "0.5.1"
DOWNLOAD_URL = ""


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [str(path.parent) for path in Path(package).glob("**/__init__.py")]


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, "r", "utf8") as f:
        return f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files("echad/assets")

setup(
    name="echad",
    packages=get_packages("echad"),
    version=ECHAD_VERSION,
    description="A rapid python ehcarts tool",
    long_description="",
    license="MIT",
    author="Hou",
    author_email="hhhoujue@gmail.com",
    package_data={"echad": extra_files},
    url="",
    download_url=DOWNLOAD_URL,
    keywords=["ehcarts", "html"],
    install_requires=[
        "domonic >= 0.9.7",
        "pydantic",
        "bottle",
        "pydash",
        "path",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
    ],
    python_requires=">=3.8.10",
)
