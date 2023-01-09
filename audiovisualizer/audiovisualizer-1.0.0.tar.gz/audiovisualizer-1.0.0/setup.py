import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(long_description=long_description,
      packages=find_packages(include="audiovisualizer", exclude="audiovisualizer.tests"),
      test_suite="audiovisualizer.tests")
