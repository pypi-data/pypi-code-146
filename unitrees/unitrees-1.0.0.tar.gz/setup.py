#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name = 'unitrees',
	version = '1.0.0',
	author = 'Pigeon Nation',
	description = 'Prints lists out as unicode trees.',
	long_description = long_description,
	long_description_content_type="text/markdown",
	packages = setuptools.find_packages(),
	license = 'MIT',
	classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Topic :: Other/Nonlisted Topic"
	]
)