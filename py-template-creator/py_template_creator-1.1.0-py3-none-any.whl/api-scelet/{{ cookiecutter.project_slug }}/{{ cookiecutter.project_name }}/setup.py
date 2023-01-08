"""A setuptools based setup module.
Authoritative references:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path, getenv

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="{{cookiecutter.app_name}}",
    version=getenv("APP_VERSION", "0.0.0"),

    description="{{cookiecutter.app_description}}",
    long_description=long_description,
    url="",

    packages=find_packages(exclude=["doc"]),

    # source code layout
    namespace_packages=["{{cookiecutter.app_name}}"],

    # Generating the command-line tool
    entry_points={
        "console_scripts": [
            "{{cookiecutter.app_name}}={{cookiecutter.app_name}}.run:prod"
        ]
    },

    # author and license
    author="{{cookiecutter.author_name}}",
    author_email="{{cookiecutter.author_email}}",
    # license="",

    # dependencies, a list of rules
    install_requires=["overrides>=1.8"],
    # add links to repositories if modules are not on pypi
    dependency_links=[
    ],

    #  PyTest integration
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "mock"]
)
