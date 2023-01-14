# python setup.py build_ext --inplace

from setuptools import setup, find_packages  # type:ignore

with open("travers/version.py", "r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="travers",
    version=__version__,
    description="Python Graph Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joocer",
    author="joocer",
    author_email="justin.joyce@joocer.com",
    packages=find_packages(include=["travers", "travers.*"]),
    url="https://github.com/joocer/travers",
    install_requires=required,
)
