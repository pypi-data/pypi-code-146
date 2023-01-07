#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name = 'hashfish',
	version = '1.0.0',
	author = 'Pigeon Nation',
	description = 'Salty HMACs!',
	long_description = long_description,
	long_description_content_type="text/markdown",
	packages = setuptools.find_packages(),
	license = 'MIT',
	classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Topic :: Security :: Cryptography"
	]
)