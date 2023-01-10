from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="py-endway-api",
    version="0.1.0",
    description="Library for convenient work with the EndWay forum",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://endway.su/members/366/",
    author="life",
    author_email="I-will-tell-you@everything.com",
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
    packages=["py-endway-api"],
    include_package_data=True,
    install_requires=["requests", "bs4"]
)
