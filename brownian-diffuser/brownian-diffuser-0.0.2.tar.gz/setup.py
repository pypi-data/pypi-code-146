import setuptools
import re
import os
import sys

setuptools.setup(
    name="brownian-diffuser",
    version="0.0.2",
    python_requires=">3.7.0",
    author="Michael E. Vinyard - Harvard University - Broad Institute of MIT and Harvard - Massachussetts General Hospital",
    author_email="mvinyard@broadinstitute.org",
    url="https://github.com/mvinyard/brownian-diffuser",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="Brownian diffuser",
    packages=setuptools.find_packages(),
    install_requires=[
        "torch>=1.12.0",
        "autodevice>=0.0.2",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
