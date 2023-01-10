# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()


VERSION = "0.0.0"


setup(
    name="correos-preregistro",
    version=VERSION,
    author="Coopdevs, Som Connexio",
    author_email="info@coopdevs.org",
    maintainer="Daniel Palomar, Gerard Funosas",
    url="https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-preregistro",
    description="Python wrapper for Correos PreRegistro SOAP API",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests == 2.28.1",
        "lxml == 4.9.2",
        "zeep == 4.2.1",
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
)
