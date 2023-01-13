from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='pycryptools',
    version='1.7.5',
    packages=find_packages(),
    url='https://pypi.org/project/pycryptools/',
    license='CC0-1.0 License',
    author='Carlos Padilla',
    author_email='cpadlab@gmail.com',
    description='PyCrypTools is a python library that brings us a series of algorithms to encrypt and decrypt inputs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    project_urls={
        "Source Code": "https://github.com/14wual/pycryptools/",
        "Bug Tracker": "https://github.com/14wual/pycryptools/issues",
        "Documentation": "https://pycryptools.readthedocs.io/",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='encrypt decrypt',
    
)