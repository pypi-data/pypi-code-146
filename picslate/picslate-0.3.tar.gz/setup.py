import codecs
import logging
import os.path

from setuptools import Extension, dist, find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


logging.basicConfig()
logger = logging.getLogger()
try:
    import numpy
except ImportError:
    dist.Distribution().fetch_build_eggs(["numpy>=1.19.4"])
    import numpy


setup(
    setup_requires=[
        "setuptools>=18.0",
        "numpy>=1.19.4",
    ],
    entry_points={"console_scripts": ["piclsate = picslate.__main__:script"]},
    name="picslate",
    version=get_version("picslate/__init__.py"),
    author="Thomas Portier",
    description="Picture ocr & translation",
    packages=find_packages(),
    package_dir={"picslate": "picslate"},
    package_data={"picslate": ["font/*", "tesseract/*", "font/*/*"]},
    install_requires=["numpy>=1.19.4", "tesserocr"],
    extra_requires={
        "translate": ["translate"],
        "argostranslate": ["argostranslate"],
        "corrector": ["enchant"],
    },
)
