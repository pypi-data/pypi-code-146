from setuptools import setup, find_packages

setup(
    name='pycryptools',
    version='1.4.3',
    packages=find_packages(),
    url='https://github.com/14wual/pycryptools',
    license='Apache License 2.0',
    author='Carlos Padilla',
    author_email='cpadlab@gmail.com',
    description='PyCrypTools is a python library that brings us a series of algorithms to encrypt and decrypt inputs.',
    install_requires=[],
    project_urls={
        "Bug Tracker": "https://github.com/14wual/pycryptools/issues",
        "Documentation": "https://github.com/14wual/pycryptools/tree/main/about",
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='encrypt decrypt',
    
)