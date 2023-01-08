from setuptools import setup, find_packages
from jikan4.__version__ import __version__


with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="jikan4",
    version=__version__,
    author="Matheus Bessa",
    description="A Python wrapper for the Jikan API",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdabessa/jikan4",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
    keywords=[
        "jikan",
        "jikan4",
        "jikan-api",
        "jikan4-api",
        "jikan-wrapper",
        "jikan4-wrapper",
        "jikan4-python",
        "jikan-python",
    ],
)
