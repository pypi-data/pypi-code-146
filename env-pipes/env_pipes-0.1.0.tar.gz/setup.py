#!python
"""A setuptools based setup module.

ToDo:
- Everything
"""

import setuptools

import simplifiedapp

import env_pipes

setuptools.setup(
	url = 'https://github.com/irvingleonard/env-pipes',
	author = 'Irving Leonard',
	author_email = 'irvingleonard@gmail.com',
	license='BSD 2-Clause "Simplified" License',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Text Processing',
		'Topic :: Utilities',
	],
	keywords = 'env environ environmental_variables',
	python_requires = '>=3.7',
	packages = setuptools.find_packages(),
	
	**simplifiedapp.object_metadata(env_pipes)
)
