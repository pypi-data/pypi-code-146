# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
CWD = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(CWD, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="ocellus",
    version="0.1.42",
    description="Ocellus API Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.ocellus.io/",
    author="Byte Motion AB",
    author_email="python@bytemotion.se",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=[
        'ocellus',
        'ocellus.api.v1',
        'ocellus.google.api',
        'ocellus.protoc_gen_swagger.options'
    ],
    include_package_data=True,
    install_requires=[
        "grpcio == 1.43.0",
        "protobuf == 3.19.3"
    ]
)