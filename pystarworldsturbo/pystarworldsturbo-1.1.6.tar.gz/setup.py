from setuptools import setup, find_packages


# All the metadata that are expected to be reused should go here.

name: str = "pystarworldsturbo"
version: str = "1.1.6"
description: str = "PyStarWorldsTurbo, an agent library."
author: str = "Emanuele Uliana"
author_email: str = "pystarworldsturbo@dicelab-rhul.org"
license: str = "GNU3"
classifiers: list = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

url: str = "https://github.com/dicelab-rhul/pystarworldsturbo"
issues: str = url + "/issues"
dependencies: list = ["wheel", "ipython", "pyjoptional>=1.0.5"]

# End of metadata


setup(
    name=name,
    version=version,
    description=description,
    url=url,
    issues=issues,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    classifiers=classifiers
)
