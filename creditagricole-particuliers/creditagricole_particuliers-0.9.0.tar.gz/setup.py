#!/usr/bin/python

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('credit agricole api banking banque')

setuptools.setup(
    name="creditagricole_particuliers",
    version="0.9.0",
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Python client pour la banque Crédit Agricole",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/creditagricole-particuliers",
    packages=['creditagricole_particuliers'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        "requests"
    ]
)