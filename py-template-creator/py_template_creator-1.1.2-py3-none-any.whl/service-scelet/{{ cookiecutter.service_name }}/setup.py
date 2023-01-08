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
    name="{{ cookiecutter.service_name }}",
    version=getenv("APP_VERSION", "0.0.0"),
    description="Service python application",
    long_description=long_description,
    packages=find_packages(exclude=["doc"]),
    # source code layout
    namespace_packages=["package"],
    # Generating the command-line tool
    entry_points={
        "console_scripts": [
            "{{ cookiecutter.service_name }}=package.run:main"
        ]
    },
    # author and license
    author="Nebojsa Mrkic",
    author_email="mrkic.nebojsa@gmail.com",
    license="Apache License 2.0",
    # dependencies, a list of rules
    install_requires=[],
    # add links to repositories if modules are not on pypi
    dependency_links=[
    ],
    #  PyTest integration
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "mock", "requests"]
)
