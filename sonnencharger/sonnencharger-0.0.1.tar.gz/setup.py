import os
from setuptools import setup

def get_version(file):
    for line in read_file(file).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError('Version not found!')

def read_file(file):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, file), mode='r', encoding='UTF-8') as file:
        return file.read()

setup(
    name="sonnencharger", # Replace with your own username
    version=get_version('sonnencharger/__init__.py'),
    author="Stefan Rubner",
    author_email="stefan@whocares.de",
    description="Access SonnenCharger via ModBus",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/rustydust/python_sonnencharger",
    packages=["sonnencharger"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
    install_requires=["pymodbus"],
)
